"""
chromadb_simples.py
Configuração SIMPLES do ChromaDB para o trabalho
Banco de dados vetorial LOCAL - funciona offline
"""

import chromadb
from sentence_transformers import SentenceTransformer
import json
import os

print("=" * 60)
print("CONFIGURANDO BANCO DE DADOS VETORIAL - CHROMADB")
print("Recomendador de Receitas Fitness")
print("=" * 60)

# 1. Criar pasta para o banco de dados
db_path = "./chroma_db"
os.makedirs(db_path, exist_ok=True)
print(f"\n1. Banco de dados criado em: {db_path}")

# 2. Conectar ao ChromaDB
client = chromadb.PersistentClient(path=db_path)

# 3. Criar coleção
collection_name = "receitas_fitness"

# Remover coleção existente se necessário (evitar duplicação)
try:
    client.delete_collection(collection_name)
    print(f"   Coleção existente removida")
except:
    pass

collection = client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "Receitas fitness para sistema de recomendação vetorial"}
)
print(f"2. Coleção '{collection_name}' criada")

# 4. Carregar modelo de embeddings
print("\n3. Carregando modelo de embeddings...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("   Modelo carregado com sucesso")

# 5. Criar receitas de exemplo
print("\n4. Criando receitas de exemplo...")

receitas = [
    {
        "id": "1",
        "texto": "Omelete de Espinafre ovos espinafre queijo cottage low-carb",
        "nome": "Omelete de Espinafre",
        "ingredientes": "2 ovos, 50g espinafre, 30g queijo cottage, sal, azeite",
        "categoria": "low-carb",
        "calorias": 280,
        "tags": ["cafe da manha", "proteico", "rapido"]
    },
    {
        "id": "2",
        "texto": "Frango Grelhado com Brócolis frango brocolis alho limao high-protein",
        "nome": "Frango Grelhado com Brócolis",
        "ingredientes": "200g peito de frango, 150g brócolis, 1 dente de alho, suco de limao",
        "categoria": "high-protein",
        "calorias": 320,
        "tags": ["jantar", "proteico", "saudavel"]
    },
    {
        "id": "3",
        "texto": "Smoothie de Banana e Aveia banana aveia leite de amendoas energetico",
        "nome": "Smoothie de Banana e Aveia",
        "ingredientes": "1 banana, 2 colheres de aveia, 200ml leite de amendoas",
        "categoria": "energetico",
        "calorias": 300,
        "tags": ["cafe da manha", "rapido", "natural"]
    }
]

# 6. Preparar dados para inserção
ids = []
embeddings = []
metadatas = []
documents = []

print("   Gerando embeddings das receitas...")
for receita in receitas:
    ids.append(receita["id"])
    
    # Gerar embedding
    embedding = model.encode(receita["texto"]).tolist()
    embeddings.append(embedding)
    
    # Metadados
    metadatas.append({
        "nome": receita["nome"],
        "categoria": receita["categoria"],
        "calorias": receita["calorias"],
        "tags": ", ".join(receita["tags"])
    })
    
    # Documento (texto completo)
    documents.append(f"{receita['nome']} - {receita['ingredientes']}")

# 7. Inserir no ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    metadatas=metadatas,
    documents=documents
)

print(f"   {len(receitas)} receitas inseridas no banco")

# 8. Testar busca por similaridade
print("\n5. Testando busca por similaridade...")

# Exemplo de consulta
consultas = [
    "receita proteica para cafe da manha",
    "comida low-carb para jantar",
    "alimento energetico rapido"
]

for i, consulta in enumerate(consultas, 1):
    print(f"\n   Consulta {i}: '{consulta}'")
    
    # Gerar embedding da consulta
    embedding_consulta = model.encode(consulta).tolist()
    
    # Buscar receitas similares
    resultados = collection.query(
        query_embeddings=[embedding_consulta],
        n_results=2,
        include=["metadatas", "distances"]
    )
    
    if resultados["ids"] and resultados["ids"][0]:
        for j in range(len(resultados["ids"][0])):
            receita_id = resultados["ids"][0][j]
            # A distância é cosseno por padrão, converter para similaridade
            distancia = resultados["distances"][0][j]
            similaridade = 1 - distancia if distancia <= 1 else 0
            metadata = resultados["metadatas"][0][j]
            
            print(f"      - {metadata['nome']} (similaridade: {similaridade:.3f})")
    else:
        print("      Nenhum resultado encontrado")

# 9. Informações finais
print("\n" + "=" * 60)
print("CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 60)

print("\n📊 ESTATÍSTICAS DO BANCO:")
print(f"   Coleção: {collection_name}")
print(f"   Receitas armazenadas: {len(receitas)}")
if embeddings:
    print(f"   Dimensões dos embeddings: {len(embeddings[0])}")
print(f"   Local do banco: {db_path}")

print("\n✅ PRÓXIMOS PASSOS:")
print("   1. Adicionar mais receitas (mínimo 20)")
print("   2. Integrar com n8n (workflow de automação)")
print("   3. Criar relatório técnico")
print("   4. Gravar vídeo demonstrativo")

print("\n💡 Para adicionar mais receitas, edite este script")
print("   ou crie um arquivo receitas.json na pasta data/")
