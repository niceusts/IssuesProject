import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# Função para verificar os temas na issue
def classificar_temas(descricao, comentarios):
    # Palavras-chave para refatoração e testes de regressão
    refatoracao_keywords = [
        "refactor", "refactoring", "cleanup", "improvement", "optimization", 
        "code quality", "clean code", "modularization", "restructure", 
        "restructure code", "simplify", "improve", "redesign", "code review", 
        "revise", "enhance", "refine", "deprecate", "remove dead code", 
        "consolidate", "reorganize", "streamline"
    ]
    regressao_keywords = [
        "regression", "regression test", "test", "bug", "failure", "failed", 
        "automated test", "unit test", "integration test", "test suite", 
        "test case", "validation", "verification", "broken", "defect", "issue", 
        "fault", "crash", "error", "bugfix", "fix", "patch", "failure report"
    ]

    # Garantir que 'descricao' e 'comentarios' sejam strings (se forem listas, junte os itens)
    if isinstance(descricao, list):
        descricao = ' '.join(descricao)  # Juntar todos os itens da lista em uma única string
    
    if isinstance(comentarios, list):
        comentarios = ' '.join(comentarios)  # Juntar todos os itens da lista em uma única string

    # Garantir que 'descricao' e 'comentarios' sejam não nulos
    descricao = descricao if descricao else ""
    comentarios = comentarios if comentarios else ""

    # Verificar se as palavras-chave estão na descrição ou nos comentários
    temas = []

    # Verificar se as palavras-chave de refatoração estão na descrição ou comentários
    if any(keyword in descricao.lower() for keyword in refatoracao_keywords) or any(keyword in comentarios.lower() for keyword in refatoracao_keywords):
        temas.append("Refatoração")

    # Verificar se as palavras-chave de testes de regressão estão na descrição ou comentários
    if any(keyword in descricao.lower() for keyword in regressao_keywords) or any(keyword in comentarios.lower() for keyword in regressao_keywords):
        temas.append("Testes de Regressão")

    return temas

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"), 
    user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"), 
    host=os.getenv("DB_HOST")
)
cursor = conn.cursor()

# Selecionar as issues que precisam ser processadas
cursor.execute("SELECT id, description, comments FROM issues")
issues = cursor.fetchall()

# Para cada issue, identificar os temas relacionados
for issue in issues:
    issue_id, descricao, comentarios = issue
    temas = classificar_temas(descricao, comentarios)

    # Atualizar o campo tema_relacionado na tabela
    if temas:
        # Converter os temas em uma lista no formato correto do PostgreSQL
        temas_array = '{' + ', '.join(temas) + '}'
        cursor.execute(sql.SQL("""
            UPDATE issues
            SET tema_relacionado = %s
            WHERE id = %s
        """), (temas_array, issue_id))

# Commitar as mudanças e fechar a conexão
conn.commit()
cursor.close()
conn.close()

print("Temas relacionados atualizados com sucesso!")
