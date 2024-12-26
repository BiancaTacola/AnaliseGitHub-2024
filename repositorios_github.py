import requests
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime

# Nome de usuário do GitHub
username = 'BiancaTacola'

# URL base para os repositórios
base_url = f'https://api.github.com/users/{username}/repos'

# Lista para armazenar todos os repositórios
all_repos = []
page = 1

# Paginação para obter todos os repositórios
while True:
    url = f'{base_url}?per_page=100&page={page}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro ao obter repositórios. Código: {response.status_code}")
        break

    repos = response.json()
    if not repos:
        break

    all_repos.extend(repos)
    page += 1

# Verifica se há repositórios
if not all_repos:
    print(f"Nenhum repositório encontrado para o usuário {username}.")
    exit()

# Filtrar repositórios criados no primeiro semestre de 2024
languages_used = Counter()

for repo in all_repos:
    created_at = repo['created_at']
    created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

    # Filtrar repositórios criados 2024
    if created_date.year == 2024 and 1 <= created_date.month <= 6:
        languages_url = repo['languages_url']
        repo_languages = requests.get(languages_url).json()

        for language in repo_languages.keys():
            languages_used[language] += 1

# Verifica se há dados para o gráfico
if not languages_used:
    print(f"Nenhum repositório de 2024 encontrado para o usuário {username}.")
    exit()

# Gera o gráfico de barras
labels, counts = zip(*languages_used.items())

plt.bar(labels, counts)

plt.ylabel('Quantidade de Projetos')
plt.title(
    f'Linguagens utilizadas em Repositórios Criados em 2024 ({username})')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Caminho completo para o arquivo de imagem
caminho_arquivo = 'C:\\Bianca\\Bianca\\GIT\\grafico1_repositorios.png'

# Salva o gráfico como um arquivo de imagem
plt.savefig(caminho_arquivo)

# Exibe a mensagem indicando que o arquivo foi salvo com sucesso
print(f'O gráfico foi salvo em: {caminho_arquivo}')

# Exibe o gráfico
plt.show()
