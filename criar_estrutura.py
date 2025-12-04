# criar_estrutura.py
import os

def criar_estrutura():
    """Cria toda a estrutura de pastas do projeto"""
    
    estrutura = {
        'workflow': [],
        'src': ['popular_qdrant.py', 'gerar_embeddings.py'],
        'docs': ['relatorio.md'],
        'data': ['receitas.json'],
        '.': ['.env', 'requirements.txt', 'README.md']
    }
    
    print("📁 Criando estrutura do projeto...")
    
    for pasta, arquivos in estrutura.items():
        # Criar pasta
        if pasta != '.':
            os.makedirs(pasta, exist_ok=True)
            print(f"✅ Pasta criada: {pasta}/")
        
        # Criar arquivos
        for arquivo in arquivos:
            caminho = os.path.join(pasta, arquivo)
            with open(caminho, 'w', encoding='utf-8') as f:
                if arquivo == '.env':
                    f.write("""# Configurações do Projeto
QDRANT_URL=https://d74c00fa-fb24-45b2-93a5-299800dd09ff.europe-west3-0-gcp.cloud.qdrant.cloud:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.rzzw2c74ERdIeygJ449xMaA8Tm7Fq1b_P9hQmbwRNgE
QDRANT_COLLECTION=receitas_fitness

# HuggingFace (opcional)
HF_API_TOKEN=

# n8n
N8N_WEBHOOK_URL=http://localhost:5678/webhook/receitas
""")
                elif arquivo == 'requirements.txt':
                    f.write("""qdrant-client>=1.6.0
requests>=2.31.0
sentence-transformers>=2.2.2
python-dotenv>=1.0.0
numpy>=1.24.0
pandas>=2.0.0
""")
                elif arquivo == 'receitas.json':
                    f.write("""{
  "receitas": [
    {
      "id": 1,
      "nome": "Omelete de Espinafre Protein",
      "ingredientes": "2 ovos, 50g espinafre, 30g queijo cottage, sal, azeite",
      "categoria": "low-carb",
      "calorias": 280,
      "tags": ["café da manhã", "proteico", "rápido"]
    }
  ]
}
""")
            print(f"   📄 {caminho}")
    
    print("\n🎉 Estrutura criada com sucesso!")
    print("\n📝 Próximos passos:")
    print("   1. Edite o arquivo .env com suas credenciais")
    print("   2. Adicione mais receitas em data/receitas.json")
    print("   3. Execute: pip install -r requirements.txt")
    print("   4. Execute: python src/popular_qdrant.py")

if __name__ == "__main__":
    criar_estrutura()
