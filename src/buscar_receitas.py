# src/buscar_receitas.py
import chromadb
from sentence_transformers import SentenceTransformer

print("=" * 60)
print("🔍 SISTEMA DE BUSCA DE RECEITAS FITNESS")
print("=" * 60)

# Carregar modelo
model = SentenceTransformer('all-MiniLM-L6-v2')

# Conectar ao banco
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("receitas_fitness")

print(f"📊 Banco conectado! Receitas no banco: {collection.count()}")

while True:
    print("\n" + "-" * 40)
    busca = input("O que você quer comer? (ou 'sair' para terminar): ")
    
    if busca.lower() == 'sair':
        print("Até logo! 👋")
        break
    
    if not busca.strip():
        continue
    
    # Converter busca em embedding
    query_embedding = model.encode(busca).tolist()
    
    # Buscar no banco
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    print(f"\n🔎 Resultados para: '{busca}'")
    print("-" * 40)
    
    if results['documents']:
        for i in range(len(results['documents'][0])):
            print(f"\n{i+1}. {results['metadatas'][0][i]['nome']}")
            print(f"   📍 Categoria: {results['metadatas'][0][i]['categoria']}")
            print(f"   🔥 Calorias: {results['metadatas'][0][i]['calorias']} kcal")
            print(f"   ⏱️  Tempo: {results['metadatas'][0][i]['tempo']} min")
            print(f"   📝 {results['documents'][0][i][:150]}...")
    else:
        print("😔 Nenhuma receita encontrada.")

input("\nPressione Enter para voltar ao menu...")
