import json
import requests
from collections import defaultdict
from datetime import datetime
from datetime import datetime, timedelta
import argparse
import os
import time

registry = "nexus-server.br"
repository = 'docker-release'

# Função para obter componentes com paginação
def get_components(username, password, max_items=1):
    print(f"Iniciando obtenção de componentes do repositório: {repository}")
    continuation_token = ""
    components = []
    total_fetched = 0

    while True:
        try:
            if continuation_token == "":
                print("Fazendo a primeira requisição para obter componentes...")
                url = f"https://{registry}/service/rest/v1/components?repository={repository}"
            else:
                print(f"Fazendo requisição com continuationToken: {continuation_token}")
                url = f"https://{registry}/service/rest/v1/components?repository={repository}&continuationToken={continuation_token}"

            response = requests.get(url, auth=(username, password))

            if response.status_code != 200:
                print(f"Erro na requisição: {response.status_code}")
                break

            result = response.json()

            print(result)

            # Adiciona componentes da página atual
            components.extend(result.get('items', []))
            total_fetched += len(result.get('items', []))

            if total_fetched >= max_items:
                print(f"Limite de {max_items} itens atingido.")
                break

            continuation_token = result.get('continuationToken')
            print(f"Continuation Token: {continuation_token}")

            if continuation_token is None:
                print("Fim da paginação")
                break

        except requests.exceptions.RequestException as e:
            print(f"Erro ao realizar a requisição: {e}")
            break

    return components[:max_items]

# Função para verificar se um componente é eleito para deleção
def eleita_para_delecao(component):
    version = component.get('version', '')
    
    # Inicializa last_download como None
    last_download = None
    # Verifica se 'assets' existe e não está vazio antes de acessar
    if 'lastDownloaded' in component:
        last_download = component.get('lastDownloaded')

    # Verifica se a versão não começa com 'V' ou 'v'
    has_v_prefix = version.startswith('V') or version.startswith('v')

    # Verifica se o lastDownloaded é null ou mais de 2 meses
    is_recent_download = False  # Assume que não é recente
    
    if last_download is not None:
        last_download_date = datetime.strptime(last_download, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        is_recent_download = last_download_date > datetime.now() - timedelta(days=60)

    # Verifica se a versão não contém 'latest'
    is_latest_tag = 'latest' in version.lower()  # Verifica se a versão é 'latest'

    # Eleição para deleção
    return not has_v_prefix and not is_recent_download and not is_latest_tag

# Função para agrupar componentes por group/name e listar versões, lastDownloaded e componentId
def group_components_by_name(components):
    grouped_components = defaultdict(list)

    for component in components:
        group = component.get('group', 'null')
        name = component.get('name', 'null')
        version = component.get('version', 'null')
        component_id = component.get('id', 'null')

        last_download = None
        if 'assets' in component and component['assets']:
            last_download = component['assets'][0].get('lastDownloaded')

        grouped_components[f"{group}:{name}"].append({
            'name': name,
            'version': version,
            'lastDownloaded': last_download,
            'componentId': component_id
        })

    return grouped_components

# Função para salvar componentes em um arquivo JSON
def save_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"\nComponentes salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Função para deletar um componente
def delete_component(username, password, component_id):
    time.sleep(0.2)
    url = f"https://{registry}/service/rest/v1/components/{component_id}"

    response = requests.delete(url, auth=(username, password))

    if response.status_code == 204:
        print(f"Componente {component_id} deletado com sucesso.")
    else:
        print(f"Erro ao deletar o componente {component_id}: {response.status_code} - {response.text}")

# Função para analisar componentes
def analyze_components(username, password):
    print("Iniciando listagem de componentes...")
    components = get_components(username, password)

    if not components:
        print("Nenhum componente encontrado ou erro na requisição.")
        return

    print(f"Agrupando componentes por 'group:name'...")
    grouped_components = group_components_by_name(components)

    # Listas para componentes eleitos para deleção e todos analisados
    eleitos_para_delecao = []
    todos_analisados = []

    data_hoje = datetime.now().strftime("%Y-%m-%d")

    # Exibir os componentes agrupados e verificar se são eleitos para deleção
    for group_name, versions in grouped_components.items():
        print(f"\nComponente: {group_name}")
        for version_info in versions:
            name = version_info['name']
            version = version_info['version']
            last_download = version_info['lastDownloaded']
            component_id = version_info['componentId']
            print(f"Nome: {name}, Versão: {version}, Último Download: {last_download}, Component ID: {component_id}")

            # Verifica se o componente é eleito para deleção
            if eleita_para_delecao(version_info):
                print(f"Componente {component_id} está eleito para deleção.")
                eleitos_para_delecao.append(version_info)  # Adiciona aos eleitos
            todos_analisados.append(version_info)  # Adiciona aos analisados

    # Salvar os resultados em arquivos JSON
    save_to_file(eleitos_para_delecao, f"{data_hoje}-componentes_eleitos_para_delecao.json")
    save_to_file(todos_analisados, f"{data_hoje}-componentes_analisados.json")

    # Imprimir apenas os eleitos para deleção
    print("\nComponentes eleitos para deleção:")
    for comp in eleitos_para_delecao:
        print(comp)

# Função para deletar componentes de um arquivo JSON
def delete_components_from_file(username, password, json_file):
    # Carregar componentes do arquivo JSON
    try:
        with open(json_file, 'r') as f:
            components_to_delete = json.load(f)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return

    for component in components_to_delete:
        component_id = component.get("componentId")
        if component_id:
            delete_component(username, password, component_id)
        else:
            print("Component ID não encontrado no componente.")

# Função para imprimir o resumo do script
def print_summary():
    summary = """
    Resumo do Script:

    Este script em Python realiza a análise e deleção de componentes em um repositório de imagens Docker hospedado em um servidor Nexus. 
    Ele permite ao usuário obter uma lista de componentes, agrupá-los por nome e versão, e determinar quais deles são elegíveis para deleção 
    com base em critérios específicos, como a ausência de prefixos 'V' ou 'v', a não ocorrência de downloads recentes e a não utilização da 
    tag 'latest'. O script também possui a funcionalidade de deletar componentes listados em um arquivo JSON.

    Funcionalidades Principais:
    1. Obtenção de Componentes: Usa a API do Nexus para obter componentes do repositório especificado, com suporte à paginação.
    2. Análise de Componentes: Agrupa componentes por nome e versão, verifica quais são elegíveis para deleção e salva os resultados em arquivos JSON.
    3. Deleção de Componentes: Permite a deleção de componentes especificados em um arquivo JSON.
    4. Autenticação: Usa variáveis de ambiente para obter as credenciais necessárias para autenticação.

    Como Rodar o Script:
    1. Pré-requisitos:
       - Python 3.x instalado.
       - Pacote `requests` instalado. Você pode instalar com o comando:
         pip install requests

    2. Configurar Credenciais:
       - Defina as variáveis de ambiente `username` e `password` no seu sistema:
         export username='seu_username'
         export password='sua_senha'

    3. Executar o Script:
       - No terminal, navegue até o diretório onde o script está localizado.
       - Execute o script com a ação desejada (`analisar` ou `deletar`). Por exemplo, para analisar os componentes:
         python nome_do_script.py analisar
       - Para deletar componentes usando um arquivo JSON, use:
         python analisar_imgs.py deletar --file caminho/para/o/arquivo.json

    Observações:
    - Ao executar a ação de análise, o script salva os componentes eleitos para deleção e todos os componentes analisados em arquivos JSON.
    - A deleção de componentes é realizada com base nos IDs dos componentes listados no arquivo JSON especificado.
    """
    print(summary)

# Função principal
def main(action, json_file=None):
    # Imprimir o resumo do script
    print_summary()

    # Se quiser pode colocar na unha...
    # Username
    username = os.getenv("username")
    # Password
    password = os.getenv("password")

    if action == "analisar":
        analyze_components(username, password)
    elif action == "deletar":
        if not json_file:
            print("Por favor, forneça o caminho do arquivo JSON com os componentes a serem deletados.")
            return
        delete_components_from_file(username, password, json_file)

    print("\nProcesso concluído.")

# Executar script principal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Análise e deleção de componentes.')
    parser.add_argument('action', choices=['analisar', 'deletar'], help='A ação a ser executada: "analisar" ou "deletar".')
    parser.add_argument('--file', type=str, help='Caminho para o arquivo JSON com os componentes a serem deletados.')
    args = parser.parse_args()
    main(args.action, args.file)
