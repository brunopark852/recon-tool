import requests
import sys

# --- CONFIGURAÇÃO VISUAL ---
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[96m"
RESET = "\033[0m"

print(f"{AZUL}--- RECON TOOL VERSÃO 2.0 (CORRIGIDA) ---{RESET}\n")

def buscar_cve(tecnologia):
    # Se a tecnologia for vazia ou genérica, ignora
    if not tecnologia or "Não identificado" in tecnologia or len(tecnologia) < 3:
        return

    # --- LIMPEZA AGRESSIVA DO TEXTO ---
    # Transforma "PHP/5.2.4-2ubuntu5.10" em "PHP 5.2.4"
    limpo = tecnologia.replace('/', ' ')  # Troca barra por espaço
    limpo = limpo.split('-')[0]         # Corta tudo depois do traço (-)
    limpo = limpo.split('(')[0]         # Corta tudo depois de parenteses
    limpo = limpo.strip()               # Remove espaços extras

    print(f"    {AZUL}[*] Consultando API NIST para: '{limpo}'...{RESET}")
    
    # URL da API
    url_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    parametros = {'keywordSearch': limpo, 'resultsPerPage': 1}
    
    try:
        resposta = requests.get(url_api, params=parametros, timeout=5)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            total = dados.get('totalResults', 0)
            
            if total > 0:
                cve = dados['vulnerabilities'][0]['cve']['id']
                print(f"    {VERMELHO}[$] VULNERÁVEL! Encontradas {total} falhas (CVEs).{RESET}")
                print(f"    {VERMELHO}[$] Exemplo: {cve}{RESET}")
            else:
                print(f"    {VERDE}[+] Nenhuma falha registrada para '{limpo}'.{RESET}")
        else:
            print(f"    {AMARELO}[!] Erro na API (Code {resposta.status_code}){RESET}")

    except Exception:
        print(f"    {AMARELO}[!] Sem conexão com a API.{RESET}")

def verificar_servidor(url):
    if not url.startswith("http"):
        url = "http://" + url

    print(f"{AMARELO}[*] Conectando no alvo: {url}...{RESET}")
    
    try:
        # User-Agent para enganar o servidor
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.head(url, headers=headers, timeout=3)
        
        print(f"\n{VERDE}[+] Conexão OK! (Status: {resp.status_code}){RESET}")
        print("-" * 50)

        # Pega os headers
        server = resp.headers.get('Server', 'Não identificado')
        tech = resp.headers.get('X-Powered-By', 'Não identificado')

        # Mostra e Analisa
        print(f"    Servidor:   {VERDE}{server}{RESET}")
        buscar_cve(server)
        
        print("-" * 30)
        
        print(f"    Tecnologia: {AMARELO}{tech}{RESET}")
        buscar_cve(tech)
        print("-" * 50)

    except Exception as e:
        print(f"{VERMELHO}[!] O servidor alvo está desligado ou inacessível.{RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        alvo = sys.argv[1]
    else:
        alvo = input("Digite a URL/IP (ex: 127.0.0.1:8080): ")
    
    verificar_servidor(alvo)
