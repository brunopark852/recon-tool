import requests
import sys

# LEGENDA:
# [+] = Sucesso
# [!] = Alerta
# [$] = Vulnerabilidade Encontrada (Novo!)

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[96m" # Cor nova para infos da API
RESET = "\033[0m"

def buscar_cve(tecnologia):
    """
    Consulta a API do NIST para ver se a tecnologia tem CVEs recentes.
    """
    if "Não identificado" in tecnologia or len(tecnologia) < 3:
        return

    # Limpa a string para busca (Ex: "Apache/2.4.49 (Unix)" vira "Apache 2.4.49")
    termo_busca = tecnologia.split(' ')[0].replace('/', ' ')
    
    print(f"    {AZUL}[*] Buscando vulnerabilidades para: {termo_busca}...{RESET}")
    
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {'keywordSearch': termo_busca, 'resultsPerPage': 3}
    
    try:
        req = requests.get(api_url, params=params, timeout=10)
        
        if req.status_code == 200:
            dados = req.json()
            total = dados.get('totalResults', 0)
            
            if total > 0:
                print(f"    {VERMELHO}[$] ALERTA! Foram encontradas {total} possíveis vulnerabilidades (CVEs)!{RESET}")
                print(f"    {VERMELHO}[$] Última registrada: {dados['vulnerabilities'][0]['cve']['id']}{RESET}")
                print(f"    {AZUL}[i] Link: https://nvd.nist.gov/vuln/search?results_type=overview&query={termo_busca}{RESET}")
            else:
                print(f"    {VERDE}[+] Nenhuma CVE crítica encontrada rapidamente.{RESET}")
        else:
            print(f"    {AMARELO}[!] Erro na API do NIST (Status: {req.status_code}){RESET}")

    except Exception as e:
        print(f"    {AMARELO}[!] Time-out ou erro na conexão com a API.{RESET}")

def verificar_servidor(url):
    if not url.startswith("http"):
        url = "http://" + url

    print(f"{AMARELO}[*] Conectando em: {url}...{RESET}")

    headers_fake = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.head(url, headers=headers_fake, timeout=5, allow_redirects=True)
        print(f"\n{VERDE}[+] Conexão Estabelecida! (Status: {response.status_code}){RESET}")
        print("-" * 50)

        servidor = response.headers.get('Server', 'Não identificado')
        tecnologia = response.headers.get('X-Powered-By', 'Não identificado')
        
        print(f"    Servidor Web:  {VERDE}{servidor}{RESET}")
        # Chama a função de busca de vulnerabilidade para o servidor
        buscar_cve(servidor)
        
        print(f"\n    Tecnologia:    {AMARELO}{tecnologia}{RESET}")
        # Chama a função de busca de vulnerabilidade para a tecnologia (PHP, etc)
        buscar_cve(tecnologia)
        
        print("-" * 50)

    except Exception as e:
        print(f"{VERMELHO}[!] Erro ao conectar: {e}{RESET}")

if __name__ == "__main__":
    target = input("Digite a URL ou IP do alvo: ")
    verificar_servidor(target)
