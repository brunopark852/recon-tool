import requests
import sys

# LEGENDA:
# [+] = Sucesso (Dados encontrados)
# [*] = Processando
# [!] = Erro/Alerta

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
RESET = "\033[0m"

def verificar_servidor(url):
    if not url.startswith("http"):
        url = "http://" + url

    print(f"{AMARELO}[*] Conectando em: {url}...{RESET}")

    headers_fake = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.head(url, headers=headers_fake, timeout=5, allow_redirects=True)
        print(f"\n{VERDE}[+] Conexão Estabelecida! (Status: {response.status_code}){RESET}")
        print("-" * 40)

        servidor = response.headers.get('Server', 'Não identificado')
        tecnologia = response.headers.get('X-Powered-By', 'Não identificado')
        
        print(f"    Servidor Web:  {VERDE}{servidor}{RESET}")
        print(f"    Tecnologia:    {AMARELO}{tecnologia}{RESET}")
        
        if response.history:
            print(f"    Redirecionado de: {response.history[0].url}")

    except Exception as e:
        print(f"{VERMELHO}[!] Erro ao conectar: {e}{RESET}")

if __name__ == "__main__":
    target = input("Digite a URL ou IP do alvo: ")
    verificar_servidor(target)