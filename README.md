# 🕵️‍♂️ Recon Tool - Banner Grabbing

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Functional-brightgreen?style=for-the-badge)
![Hacking](https://img.shields.io/badge/Focus-Recon-red?style=for-the-badge)

Ferramenta desenvolvida em Python para automatizar a fase de **Reconhecimento (Recon)** em testes de segurança. O script realiza *Banner Grabbing* e identifica tecnologias do servidor alvo, simulando um navegador real para evitar bloqueios básicos.

## 🚀 Funcionalidades

* **[+] Identificação de Servidor:** Captura o header `Server` (Apache, Nginx, IIS).
* **[+] Detecção de Stack:** Lê o header `X-Powered-By` para descobrir tecnologias (PHP, ASP.NET, etc).
* **[+] User-Agent Spoofing:** Mascara as requisições como **Google Chrome** (Bypass de filtros simples).
* **[+] Feedback Visual:** Interface limpa com status codes e tratamento de erros.

## 🛠️ Instalação

```bash
# 1. Clone o repositório
git clone [https://github.com/brunopark852/recon-tool.git](https://github.com/brunopark852/recon-tool.git)

# 2. Entre na pasta
cd recon-tool

# 3. Instale as dependências
pip install requests
