import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

url = "https://api.github.com/repos/tensorflow/tensorflow/issues"

# Configuração
total_limit = 300  # Limite de issues a coletar
per_page = 100 
all_issues = []
page = 1

while len(all_issues) < total_limit:
    print(f"Buscando página {page}...")
    params = {
        "state": "closed",  # Pegar issues fechadas
        "labels": "type:bug",  # Filtrar por label "type:bug"
        "per_page": per_page,
        "page": page,
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        issues = response.json()
        if not issues: 
            break

         # Filtrar apenas as issues que têm assignee e o label "type:bug"
        issues = [issue for issue in issues if 'assignee' in issue and issue['assignee'] is not None]
        
        # Adicionar issues até atingir o limite
        remaining_slots = total_limit - len(all_issues)
        all_issues.extend(issues[:remaining_slots])
        page += 1
    else:
        print(f"Erro ao buscar dados: {response.status_code}")
        print(response.json())
        break

print(f"Total de issues coletadas: {len(all_issues)}")

# Criar DataFrame com as issues coletadas
df = pd.DataFrame(all_issues)

# Para armazenar os comentários e os labels em formato JSON ou texto
df['comments'] = None
df['labels'] = df['labels'].apply(lambda x: [label['name'] for label in x])  # Extrair apenas o nome do label

# Buscar os comentários de cada issue
def get_comments(issue_number):
    comments_url = f"https://api.github.com/repos/tensorflow/tensorflow/issues/{issue_number}/comments"
    comments_response = requests.get(comments_url, headers=headers)
    if comments_response.status_code == 200:
        comments = comments_response.json()
        return [comment['body'] for comment in comments]  # Retorna os comentários em uma lista
    else:
        print(f"Erro ao buscar comentários para a issue {issue_number}: {comments_response.status_code}")
        return []

# Adicionar comentários ao DataFrame
for index, row in df.iterrows():
    issue_number = row['number']
    comments = get_comments(issue_number)
    df.at[index, 'comments'] = comments

# Adicionar a descrição da issue
df['description'] = df['body']  # Corpo da issue, que é a descrição

# Ordenar o DataFrame pelas issues mais antigas (por data de criação)
df['created_at'] = pd.to_datetime(df['created_at'])
df = df.sort_values(by='created_at') 

# Extrair apenas o login do assignee
df['assignee'] = df['assignee'].apply(lambda x: x[0]['login'] if isinstance(x, list) and len(x) > 0 else (x['login'] if isinstance(x, dict) else None))


selected_columns = [
    "id", "number", "title", "state", "created_at", "updated_at", 
    "closed_at", "assignee", "milestone", "html_url", "labels", "comments", "description"
]

df = df[selected_columns]

# Salvar em CSV
output_file = "issues6.csv"
df.to_csv(output_file, index=False)
print(f"Issues mais antigas com comentários, labels e descrições salvas no arquivo: {output_file}")
