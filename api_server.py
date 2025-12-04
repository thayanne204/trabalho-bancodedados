"""
api_server.py
API REST para integração com n8n
"""
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import chromadb
import uvicorn

app = FastAPI(title="API de Receitas Fitness", version="1.0")

# Carregar modelo e banco
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db_trabalho")
collection = client.get_collection("receitas_fitness_final")

@app.get("/")
def root():
    return {"message": "API de Recomendação de Receitas Fitness", "status": "online"}

@app.get("/buscar")
def buscar_receitas(q: str = Query(..., description="Consulta de busca")):
    """Busca receitas por similaridade semântica"""
    embedding = model.encode(q).tolist()
    
    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=5,
        include=["metadatas", "distances", "documents"]
    )
    
    receitas_encontradas = []
    for i in range(len(resultados["ids"][0])):
        receita = {
            "id": resultados["ids"][0][i],
            "nome": resultados["metadatas"][0][i]["nome"],
            "categoria": resultados["metadatas"][0][i]["categoria"],
            "calorias": resultados["metadatas"][0][i]["calorias"],
            "tags": resultados["metadatas"][0][i]["tags"].split(", "),
            "similaridade": float(1 - resultados["distances"][0][i]),
            "texto": resultados["documents"][0][i]
        }
        receitas_encontradas.append(receita)
    
    return {
        "consulta": q,
        "total_resultados": len(receitas_encontradas),
        "receitas": receitas_encontradas
    }

@app.get("/todas")
def todas_receitas():
    """Retorna todas as receitas do banco"""
    todos = collection.get()
    
    receitas = []
    for i in range(len(todos["ids"])):
        receita = {
            "id": todos["ids"][i],
            "nome": todos["metadatas"][i]["nome"],
            "categoria": todos["metadatas"][i]["categoria"],
            "calorias": todos["metadatas"][i]["calorias"],
            "tags": todos["metadatas"][i]["tags"].split(", ")
        }
        receitas.append(receita)
    
    return {"total": len(receitas), "receitas": receitas}

if __name__ == "__main__":
    print("🚀 Servidor API iniciando...")
    print("📡 Endpoints disponíveis:")
    print("   • GET /          - Status da API")
    print("   • GET /buscar?q= - Busca semântica")
    print("   • GET /todas     - Todas receitas")
    print("\n🔗 Para n8n, use: http://localhost:8000/buscar?q=sua_consulta")
    uvicorn.run(app, host="0.0.0.0", port=8000)
