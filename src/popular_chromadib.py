# src/popular_chromadib.py
import chromadb
from sentence_transformers import SentenceTransformer
import json
import os

print("-" * 50)
print("POPULANDO BANCO DE DADOS COM RECEITAS COMPLETAS")
print("Sistema: recomendador vetorial de Receitas Fitness")
print("-" * 50)

def carregar_receitas():
    """Carrega receitas do arquivo JSON"""
    print("\n1. Carregando receitas...")
    
    try:
        # Tenta encontrar o arquivo JSON
        caminho_json = "data/recettes_completes.json"
        if not os.path.exists(caminho_json):
            caminho_json = "recettes_completes.json"
            if not os.path.exists(caminho_json):
                print(f"ERRO: Arquivo JSON não encontrado!")
                print("Procurando em:", os.getcwd())
                return None
        
        with open(caminho_json, 'r', encoding='utf-8') as f:
            receitas = json.load(f)
        
        print(f"✅ {len(receitas)} receitas carregadas com sucesso!")
        return receitas
        
    except Exception as e:
        print(f"❌ Erro ao carregar receitas: {e}")
        return None

def popular_banco_dados():
    """Popula o ChromaDB com as receitas"""
    print("\n2. Inicializando ChromaDB...")
    
    try:
        # Inicializa ChromaDB
        cliente = chromadb.PersistentClient(path="./chroma_db")
        
        # Cria ou obtém a coleção
        colecao = cliente.get_or_create_collection(
            name="receitas_fitness",
            metadata={"description": "Banco de receitas fitness"}
        )
        
        # Carrega as receitas
        receitas = carregar_receitas()
        if not receitas:
            return
        
        print("\n3. Processando receitas...")
        
        # Modelo de embeddings (usando um modelo leve)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        ids = []
        documentos = []
        metadados = []
        embeddings = []
        
        for i, receita in enumerate(receitas):
            # Cria um texto único para embedding
            texto_receita = f"{receita.get('nome', '')} {receita.get('ingredientes', '')} {receita.get('modo_preparo', '')}"
            
            # Gera embedding
            embedding = model.encode(texto_receita).tolist()
            
            # Prepara dados
            ids.append(f"receita_{i+1}")
            documentos.append(texto_receita)
            metadados.append({
                "nome": receita.get('nome', 'Sem nome'),
                "categoria": receita.get('categoria', 'Geral'),
                "calorias": receita.get('calorias', 0),
                "tempo_preparo": receita.get('tempo_preparo', 0)
            })
            embeddings.append(embedding)
            
            if (i + 1) % 10 == 0:
                print(f"  Processadas {i + 1} receitas...")
        
        # Adiciona ao ChromaDB
        print("\n4. Adicionando ao banco de dados...")
        colecao.add(
            ids=ids,
            documents=documentos,
            metadatas=metadados,
            embeddings=embeddings
        )
        
        print(f"✅ Banco populado com {len(receitas)} receitas!")
        print("🎉 Processo concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    popular_banco_dados()
