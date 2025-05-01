from requests.auth import HTTPBasicAuth
import requests
import json
import os
import sys

class Glpi:
    def __init__(self):
        print("Inicializando a classe Glpi...")
        self.credenciais_glpi = self.carrega_credenciais_glpi()
        self.base_url = self.credenciais_glpi["Url_Base"]
        self.headers = {
            "Content-Type": "application/json",
            "App-Token": self.credenciais_glpi["App-Token"]
        }
        self.init_session()

    def init_session(self):
        print("Iniciando sessão no GLPI...")
        url = f"{self.base_url}/initSession"
        response = requests.get(url, headers=self.headers, auth=HTTPBasicAuth(self.credenciais_glpi["User"], self.credenciais_glpi["Senha"]))
        response = response.text.strip()
        response = response.lstrip('\ufeff\n')
        response = json.loads(response)
        self.headers['Session-Token'] = response['session_token']
        print(f"Session Token: {response['session_token']}")

    def carrega_credenciais_glpi(self):
        #Carrega as credenciais de um arquivo JSON.
        print("Carregando credenciais GLPI...")
        path = os.getcwd()  # Obtém o diretório atual
        with open(f"{path}/bot_glpi_base/config/credenciais_glpi.json", "r") as arquivo:
            return json.load(arquivo)

# Filtro que retorna todos os chamados com status "NOVOS"
    def get_ticket(self):
        print("Consultando chamados NOVOS...")
        url = f"{self.base_url}/search/Ticket/"
        params = {
            "criteria[0][field]": 12,
            "criteria[0][searchtype]": "equals",
            "criteria[0][value]": 1,
            "uid_cols": "true",
            "range": "0-200"
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code in [200, 206]:
            print(f"Resposta recebida com sucesso: {response.status_code}")
            resposta = response.text.strip()
            resposta = resposta.lstrip('\ufeff\n')
            dados_json = json.loads(resposta)
            if dados_json['totalcount'] != 0:
                print("Chamados novos coletados.")
                return dados_json['data']
            else:
                print("Não há chamados na fila do GLPI. Automação encerrada.")
                sys.exit(0)
        else:
            print(f"{response.status_code} - Falha ao consultar ticket na API.")
            sys.exit(0)

# Filtro que retorna todos os técnicos do grupo
    def get_users(self):
        print("Consultando técnicos no grupo...")
        url = f"{self.base_url}/search/User/"
        params = {
            "criteria[0][field]": 13,
            "criteria[0][searchtype]": "equals",
            "criteria[0][value]": 25,
            "forcedisplay[0]": 2,
            "uid_cols": "true",
            "range": "0-200",
        }

        response = requests.get(url, headers=self.headers, params=params)
        print(f"Resposta dos técnicos: {response.status_code}")
        print(response.content)
        if response.status_code in [200, 206]:

            data_str = response.content
            data_str = data_str.decode('utf-8')
            # Remover qualquer nova linha no início, caso exista
            data_str = data_str.lstrip('\n')

            if data_str.startswith('\ufeff'):
                data_str = data_str[1:]
            # Carregar a string JSON para um dicionário
            data_json = json.loads(data_str)

            print(f"Técnicos recebidos: {data_json}")

            # Trata os técnicos no grupo e adiciona a quantidade de chamados que cada técnico tem
            if data_json.get("totalcount", 0) > 0:
                tecnicos = []
                for tecnico in data_json.get("data", []):
                    tecnico_id = tecnico.get("User.id")
                    tecnico_nome = tecnico.get("User.name")

                    print(f"Consultando chamados do técnico {tecnico_nome}...")
                    # Função que retorna a quantidade de chamados do técnico atual
                    ticket_count = self.get_ticket_por_tecnico(tecnico_id)

                    tecnicos.append({
                        "id": tecnico_id,
                        "name": tecnico_nome,
                        "ticket_count": ticket_count
                    })
                print(f"Técnicos encontrados: {len(tecnicos)}")
                return tecnicos
            else:
                print("Não há técnicos no grupo informado.")
                sys.exit(0)
        else:
            print(f"{response.status_code} - Falha ao consultar técnicos na API.")
            sys.exit(1)

# Função que verifica quantos chamados cada técnico tem em sua fila
    def get_ticket_por_tecnico(self, tecnico_id):
        print(f"Consultando chamados para o técnico {tecnico_id}...")
        url = f"{self.base_url}/search/Ticket/"
        params = {
            "criteria[0][field]": 12,
            "criteria[0][searchtype]": "equals",
            "criteria[0][value]": 2,
            "criteria[1][field]": 5,
            "criteria[1][searchtype]": "equals",
            "criteria[1][value]": tecnico_id,
            "uid_cols": "true",
            "range": "0-200"
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code in [200, 206]:
            resposta = response.text.strip()
            resposta = resposta.lstrip('\ufeff\n')
            tecnicos_json = json.loads(resposta)
            print(f"Chamados encontrados para o técnico {tecnico_id}: {tecnicos_json['totalcount']}")
            return tecnicos_json['totalcount']

# Ordena a lista de técnicos de forma crescente, baseado na quantidade de chamados
    def score_chamados(self, tecnicos):
        print("Ordenando lista de técnicos de acordo com a quantidade de chamados...")
        return sorted(tecnicos, key=lambda x: x["ticket_count"])

# Função que distribui os chamados de acordo com a ordem da lista "tecnicos"
    def distribui_chamado(self, tickets, tecnicos):
        print(f"Distribuindo chamado {tickets['Ticket.id']} para o técnico {tecnicos['id']}...")
        url = f"{self.base_url}/Ticket/{tickets['Ticket.id']}/Ticket_User"

        body = {
            "input": {
                "tickets_id": tickets['Ticket.id'],
                "users_id": tecnicos['id'],
                "type": 2
            }
        }

        response = requests.post(url, headers=self.headers, json=body)
        print(f"Resposta ao distribuir chamado: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    print("Iniciando automação GLPI...")
    glpi = Glpi()
    tecnicos = glpi.get_users()

    for tecnico in tecnicos:
        print(f"Técnico: {tecnico['name']} | Chamados atribuídos: {tecnico['ticket_count']}")
