import pandas as pd
import psycopg2
from psycopg2 import sql
import json

# Carregar os dados do arquivo CSV
df = pd.read_csv("issues_final.csv")  # Substitua pelo seu DataFrame

# Substituir NaN por None (NULL no PostgreSQL) nas colunas de data
df['created_at'] = df['created_at'].apply(lambda x: None if pd.isna(x) else x)
df['closed_at'] = df['closed_at'].apply(lambda x: None if pd.isna(x) else x)

# Garantir que 'assignee' seja um JSON válido ou NULL
df['assignee'] = df['assignee'].apply(lambda x: None if pd.isna(x) else (json.dumps(x) if isinstance(x, dict) else None))

# Garantir que 'milestone' seja um JSON válido ou NULL
df['milestone'] = df['milestone'].apply(lambda x: None if pd.isna(x) else (json.dumps(x) if isinstance(x, dict) else None))

# Garantir que 'labels' seja uma lista ou NULL
df['labels'] = df['labels'].apply(lambda x: None if pd.isna(x) else x.strip("[]").replace("'", "").split(",") if isinstance(x, str) else None)

# Garantir que 'comments' seja uma lista ou NULL
df['comments'] = df['comments'].apply(lambda x: None if pd.isna(x) else x.strip("[]").replace("'", "").split(",") if isinstance(x, str) else None)

# Adicionar a descrição da issue
df['description'] = df['description'].apply(lambda x: None if pd.isna(x) else x)

# Estabelecendo a conexão com o banco de dados
conn = psycopg2.connect(
    dbname="", user="", password="", host=""
)
cursor = conn.cursor()

# Inserir os dados na tabela 'issues'
for index, row in df.iterrows():
    query = sql.SQL("""
        INSERT INTO issues (id, number, title, state, created_at, updated_at, closed_at, assignee, milestone, html_url, labels, comments, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(query, (
        row['id'], row['number'], row['title'], row['state'], row['created_at'], 
        row['updated_at'], row['closed_at'], row['assignee'], row['milestone'], 
        row['html_url'], row['labels'], row['comments'], row['description']
    ))

# Commitar as mudanças e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Dados inseridos com sucesso!")
