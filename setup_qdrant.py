"""
setup_qdrant.py 
Configuração do Banco de Dados Vetorial Qdrant
Sistema: Recomendador de Receitas Fitness
"""

import requests
import json
from typing import Dict, Any, Optional

class ConfiguradorQdrant:
    """Classe para configurar e gerenciar o Qdrant"""
    
    def __init__(self):
        # ========== CONFIGURAÇÕES ==========
        #  COLE SUAS INFORMAÇÕES AQUI 
        self.URL_QDRANT = "https://d74c00fa-fb24-45b2-93a5-298800dd09ff.europe-west3-0.gcp.cloud.qdrant.io"
        self.CHAVE_API = "eyJN0e1o1JU021M11S1mGSCIG1KpXCJ9.eyJNY2NLC9N1Q1JUm0.rzxR2C74E8dfcygJ449svNA6Tm7Fq1b_P9hQmbwRtgE"
        # ===================================
        
        self.NOME_COLECAO = "receitas_fitness"
        self.cabecalhos = {
            "api-key": self.CHAVE_API,
            "Content-Type": "application/json"
        }
        
    def mostrar_cabecalho(self):
        """Exibe informações do projeto"""
        print("\n" + "=" * 70)
        print("RECOMENDADOR VETORIAL DE RECEITAS FITNESS")
        print("Banco de Dados Vetorial - Trabalho Final BD")
        print("=" * 70)
        print("\nConfiguração Qdrant:")
        print(f"   URL: {self.URL_QDRANT}")
        print(f"   API Key: {self.CHAVE_API[:15]}...[oculto]")
        
    def testar_conexao(self) -> bool:
        """Testa conexão com Qdrant"""
        print("\n1. Testando conexão com Qdrant Cloud...")
        
        try:
            # ADICIONE verify=False PARA EVITAR PROBLEMAS DE SSL
            response = requests.get(
                f"{self.URL_QDRANT}/collections",
                headers=self.cabecalhos,
                timeout=30,
                verify=False  # ← IMPORTANTE!
            )
            
            if response.status_code == 200:
                print("   CONEXAO ESTABELECIDA COM SUCESSO")
                
                data = response.json()
                colecoes = data.get("collections", [])
                
                if colecoes:
                    print(f"   Coleções encontradas ({len(colecoes)}):")
                    for col in colecoes:
                        print(f"      - {col['name']}")
                else:
                    print("   Nenhuma coleção encontrada")
                    
                return True
                
            else:
                print(f"   ERRO HTTP {response.status_code}")
                print(f"   Mensagem: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("   TIMEOUT: A conexão demorou muito")
            return False
        except requests.exceptions.ConnectionError:
            print("   ERRO DE CONEXAO: Verifique sua internet")
            return False
        except Exception as e:
            print(f"   ERRO INESPERADO: {e}")
            return False
    
    def criar_colecao(self) -> bool:
        """Cria a coleção para receitas"""
        print(f"\n2. Criando coleção '{self.NOME_COLECAO}'...")
        
        collection_config = {
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            }
        }
        
        try:
            response = requests.put(
                f"{self.URL_QDRANT}/collections/{self.NOME_COLECAO}",
                headers=self.cabecalhos,
                json=collection_config,
                verify=False  # ← ADICIONE TAMBÉM AQUI
            )
            
            if response.status_code == 200:
                print("   COLECAO CRIADA COM SUCESSO")
                return True
            elif response.status_code == 400:
                if "already exists" in response.text.lower():
                    print("   COLECAO JA EXISTE")
                    return True
                else:
                    print(f"   ERRO NA CRIACAO: {response.text}")
                    return False
            else:
                print(f"   STATUS {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ERRO: {e}")
            return False
    
    def verificar_colecao(self) -> Dict[str, Any]:
        """Obtém informações da coleção"""
        print(f"\n3. Verificando coleção '{self.NOME_COLECAO}'...")
        
        try:
            response = requests.get(
                f"{self.URL_QDRANT}/collections/{self.NOME_COLECAO}",
                headers=self.cabecalhos,
                verify=False
            )
            
            if response.status_code == 200:
                info = response.json()
                print("   COLECAO VERIFICADA")
                print(f"   Status: {info.get('status', 'N/A')}")
                print(f"   Dimensoes: {info.get('vectors', {}).get('size', 'N/A')}")
                print(f"   Pontos: {info.get('points_count', 0)}")
                return info
            else:
                print(f"   NAO FOI POSSIVEL VERIFICAR: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"   ERRO NA VERIFICACAO: {e}")
            return {}
    
    def inserir_dados_teste(self):
        """Insere dados de teste"""
        print("\n4. Inserindo dados de teste...")
        
        receitas_teste = [
            {
                "id": 1,
                "vector": [0.1] * 384,
                "payload": {
                    "nome": "Omelete de Espinafre",
                    "ingredientes": "ovos, espinafre, queijo cottage",
                    "categoria": "low-carb",
                    "calorias": 250
                }
            },
            {
                "id": 2,
                "vector": [0.2] * 384,
                "payload": {
                    "nome": "Smoothie de Banana",
                    "ingredientes": "banana, aveia, leite de amendoas",
                    "categoria": "energetico",
                    "calorias": 180
                }
            }
        ]
        
        try:
            response = requests.put(
                f"{self.URL_QDRANT}/collections/{self.NOME_COLECAO}/points",
                headers=self.cabecalhos,
                json={"points": receitas_teste},
                verify=False
            )
            
            if response.status_code == 200:
                print("   2 receitas de teste inseridas")
                return True
            else:
                print(f"   STATUS {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ERRO: {e}")
            return False

def main():
    """Função principal"""
    # Inicializar
    qdrant = ConfiguradorQdrant()
    qdrant.mostrar_cabecalho()
    
    # Verificar dependências
    try:
        import requests
    except ImportError:
        print("\nERRO: Biblioteca 'requests' não instalada")
        print("Execute: pip install requests")
        return
    
    # Passo 1: Testar conexão
    if not qdrant.testar_conexao():
        print("\nFALHA NA CONEXAO. Verifique:")
        print("   1. API Key correta?")
        print("   2. Internet funcionando?")
        print("   3. URL do Qdrant correto?")
        
        resposta = input("\nDeseja continuar mesmo assim? (s/n): ").lower()
        if resposta != 's':
            return
    
    # Passo 2: Criar coleção
    qdrant.criar_colecao()
    
    # Passo 3: Verificar coleção
    qdrant.verificar_colecao()
    
    # Passo 4: Inserir dados de teste
    resposta_teste = input("\nInserir dados de teste? (s/n): ").lower()
    if resposta_teste == 's':
        qdrant.inserir_dados_teste()
    
    # Finalização
    print("\n" + "=" * 70)
    print("CONFIGURACAO CONCLUIDA")
    print("\nESTRUTURA DO PROJETO:")
    print("trabalho-bd/")
    print("├── setup_qdrant.py")
    print("├── data/")
    print("├── src/")
    print("├── workflow/")
    print("├── docs/")
    print("└── .env")
    
    print("\nPROXIMOS PASSOS:")
    print("1. Editar .env com suas credenciais")
    print("2. Adicionar receitas em data/receitas.json")
    print("3. Instalar: pip install sentence-transformers")
    print("4. Popular o banco com dados reais")
    print("5. Configurar o n8n")

if __name__ == "__main__":
    main()
