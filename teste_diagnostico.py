# teste_diagnostico.py
import requests
import ssl
import socket

print("=" * 60)
print("DIAGNÓSTICO DE CONEXÃO QDRANT")
print("=" * 60)

# SUAS INFORMAÇÕES (COLE AQUI)
URL = "https://d74c00fa-fb24-45b2-93a5-298800dd09ff.europe-west3-0.gcp.cloud.qdrant.io:6333"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.rzzw2c74ERdIeygJ449xMaA8Tm7Fq1b_P9hQmbwRNgE."  # ← SUA API KEY AQUI!

print(f"\nURL: {URL}")
print(f"API Key: {API_KEY[:10]}...[oculto]")

# Teste 1: Conexão TCP básica
print("\n1. Testando conexão TCP na porta 6333...")
try:
    sock = socket.create_connection(("d74c00fa-fb24-45b2-93a5-299800dd09ff.europe-west3-0-gcp.cloud.qdrant.cloud", 6333), timeout=10)
    print("   ✅ Porta 6333 acessível")
    sock.close()
except Exception as e:
    print(f"   ❌ Falha TCP: {e}")

# Teste 2: SSL/TLS
print("\n2. Testando certificado SSL...")
try:
    context = ssl.create_default_context()
    with socket.create_connection(("d74c00fa-fb24-45b2-93a5-299800dd09ff.europe-west3-0-gcp.cloud.qdrant.cloud", 6333), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname="d74c00fa-fb24-45b2-93a5-299800dd09ff.europe-west3-0-gcp.cloud.qdrant.cloud") as ssock:
            print(f"   ✅ SSL OK. Certificado para: {ssock.version()}")
except Exception as e:
    print(f"   ❌ SSL falhou: {e}")

# Teste 3: HTTP básico (sem API key)
print("\n3. Testando HTTP básico...")
try:
    response = requests.get(f"{URL}:6333", timeout=10, verify=False)
    print(f"   ✅ Servidor responde. Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ HTTP falhou: {e}")

# Teste 4: Com API Key
print("\n4. Testando com API Key...")
headers = {"api-key": API_KEY}
try:
    response = requests.get(
        f"{URL}:6333/collections",
        headers=headers,
        timeout=15,
        verify=False  # ← TENTE COM verify=False
    )
    
    print(f"   Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ API Key VÁLIDA!")
        print(f"   Resposta: {response.text[:200]}")
    elif response.status_code == 403:
        print("   ❌ API Key INVÁLIDA ou expirada")
        print("   ➡️ Gere uma NOVA API Key no Qdrant Cloud")
    elif response.status_code == 401:
        print("   ❌ Não autorizado - API Key incorreta")
    else:
        print(f"   ⚠️ Status inesperado: {response.text}")
        
except Exception as e:
    print(f"   ❌ Erro na requisição: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("SOLUÇÕES COMUNS:")
print("1. API Key incorreta → Crie nova no Qdrant Cloud")
print("2. Firewall bloqueando → Tente com verify=False")
print("3. URL errado → Verifique no painel do Qdrant")
print("=" * 60)
