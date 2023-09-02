import pandas as pd
import requests
import json
import random

# Lê o arquivo de mensagens predefinidas
with open('mensagens.txt', 'r', encoding='utf-8') as file:
    mensagens = file.readlines()

# Remove quebras de linha das mensagens e cria uma lista
mensagens = [mensagem.strip() for mensagem in mensagens]

# Lê o arquivo CSV com os IDs dos usuários
df= pd.read_csv('SDW2023.csv')
user_ids=df['UserID'].tolist()

#API 
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# Função para obter informações do usuário com base no ID
def get_user(id):
    response= requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

# Filtra os usuários da API com base nos IDs do arquivo CSV
users = [user for id in user_ids if (user := get_user(id)) is not None]

# Função para escolher aleatoriamente mensagens para cada usuário
def escolhendo_mensagem_aleatoria(users, messages):
    resultados = []

    for user in users:
      
        mensagem = random.choice(messages)
        user_mensagem= f"{user['name']}, {mensagem}"
        user['new'] = user_mensagem
        resultados.append(user)

    return resultados
# Chama a função para atribuir aleatoriamente mensagens aos usuários
users_with_random_messages = escolhendo_mensagem_aleatoria(users, mensagens)
# Imprime os resultados
for user in users_with_random_messages:
    news = user['new']
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
# Função para atualizar informações do usuário
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False
for user in users:
    success = update_user(user)
    print(f"User{user['name']} update? {success}!")