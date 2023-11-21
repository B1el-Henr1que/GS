import cx_Oracle
import json

# Conectar ao banco de dados Oracle
def conectar_banco():
    try:
        connection = cx_Oracle.connect("rm99463/310803@localhost:oracle.fiap.com.br/orcl")
        return connection
    except cx_Oracle.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

# Menu de opções
def exibir_menu():
    print("1. Inserir")
    print("2. Excluir")
    print("3. Alterar")
    print("4. Consultar")
    print("5. Exportar Consultas para JSON")
    print("6. Sair")

# Inserir registro

def inserir_registro(connection, cursor):
    try:
        nome = input("Digite o nome: ")
        idade = int(input("Digite a idade: "))
        email = input("Digite o email: ")

        # Substitua 'sua_tabela' pelos nomes reais das suas tabelas e colunas
        cursor.execute("INSERT INTO sua_tabela (nome, idade, email) VALUES (:1, :2, :3)", (nome, idade, email))
        connection.commit()

        print("Registro inserido com sucesso!")
    except cx_Oracle.Error as error:
        print(f"Erro ao inserir registro: {error}")

    pass

# Excluir registro
def excluir_registro(connection, cursor):
    try:
        id_para_excluir = int(input("Digite o ID do registro a ser excluído: "))

        # Substitua 'sua_tabela' pelos nomes reais das suas tabelas e colunas
        cursor.execute("DELETE FROM sua_tabela WHERE id = :1", (id_para_excluir,))
        connection.commit()

        print("Registro excluído com sucesso!")
    except cx_Oracle.Error as error:
        print(f"Erro ao excluir registro: {error}")

    pass

# Alterar registro

def alterar_registro(connection, cursor):
    try:
        id_para_alterar = int(input("Digite o ID do registro a ser alterado: "))
        novo_nome = input("Digite o novo nome: ")

        # Substitua 'sua_tabela' pelos nomes reais das suas tabelas e colunas
        cursor.execute("UPDATE sua_tabela SET nome = :1 WHERE id = :2", (novo_nome, id_para_alterar))
        connection.commit()

        print("Registro alterado com sucesso!")
    except cx_Oracle.Error as error:
        print(f"Erro ao alterar registro: {error}")

    pass


def consultar_registros(connection, cursor):
    try:
        # Substitua 'sua_tabela' pelos nomes reais das suas tabelas e colunas
        cursor.execute("SELECT * FROM sua_tabela")
        registros = cursor.fetchall()

        for registro in registros:
            print(registro)
    except cx_Oracle.Error as error:
        print(f"Erro ao consultar registros: {error}")

    pass

# Exportar consultas para JSON
def exportar_para_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as json_file:
        json.dump(dados, json_file, indent=2)
    print(f"Dados exportados para {nome_arquivo}")

# Rastrear e Identificar Doenças Transmissíveis
def rastrear_identificar_transmissiveis(connection, cursor):
    try:
        paciente_id = int(input("Digite o ID do paciente: "))
        data_leitura = input("Digite a data da leitura (no formato YYYY-MM-DD HH:MM:SS): ")
        temperatura = float(input("Digite a temperatura (em Celsius): "))
        batimentos_cardiacos = int(input("Digite os batimentos cardíacos por minuto: "))
        pressao_arterial = input("Digite a pressão arterial (no formato XX/YY): ")

        # Substitua 'sua_tabela_rastreamento' pelos nomes reais das suas tabelas e colunas
        cursor.execute("INSERT INTO sua_tabela_rastreamento (paciente_id, data_leitura, temperatura, batimentos_cardiacos, pressao_arterial) VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD HH24:MI:SS'), :3, :4, :5)",
                       (paciente_id, data_leitura, temperatura, batimentos_cardiacos, pressao_arterial))
        connection.commit()

        # Verificar se os dados indicam potencial caso de doença transmissível
        identificar_potencial_transmissivel(paciente_id, temperatura, batimentos_cardiacos)
        
        print("Dados de rastreamento registrados com sucesso!")
    except cx_Oracle.Error as error:
        print(f"Erro ao rastrear dados do paciente: {error}")

def identificar_potencial_transmissivel(paciente_id, temperatura, batimentos_cardiacos):
    # Critérios básicos para identificar potencial caso de doença transmissível
    temperatura_limite = 38.0
    batimentos_cardiacos_limite = 100

    if temperatura > temperatura_limite or batimentos_cardiacos > batimentos_cardiacos_limite:
        # Caso os critérios sejam atendidos, registre o potencial caso
        registrar_potencial_caso(paciente_id, temperatura, batimentos_cardiacos)

def registrar_potencial_caso(paciente_id, temperatura, batimentos_cardiacos):
    # Aqui você pode realizar ações adicionais, como registrar no banco de dados ou notificar autoridades de saúde
    print(f"Potencial caso de doença transmissível para o paciente {paciente_id}.")
    print(f"Sintomas: Temperatura {temperatura}°C, Batimentos Cardíacos {batimentos_cardiacos}/min.")
    enviar_email_notificacao(f"Potencial caso de doença transmissível para o paciente {paciente_id}. Sintomas: Temperatura {temperatura}°C, Batimentos Cardíacos {batimentos_cardiacos}/min.")

def enviar_email_notificacao(mensagem):
    # Configurar suas credenciais SMTP e destinatários
    remetente_email = 'seu_email@gmail.com'
    remetente_senha = 'sua_senha'
    destinatario_email = 'destinatario@example.com'

    # Configurar servidor SMTP
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente_email
    msg['To'] = destinatario_email
    msg['Subject'] = 'Alerta de Potencial Caso de Doença Transmissível'

# Função principal
def main():
    connection = conectar_banco()

    if connection:
        cursor = connection.cursor()

        while True:
            exibir_menu()
            opcao = input("Digite a opção desejada: ")

            if opcao == '1':
                inserir_registro(connection, cursor)
            elif opcao == '2':
                excluir_registro(connection, cursor)
            elif opcao == '3':
                alterar_registro(connection, cursor)
            elif opcao == '4':
                consultar_registros(connection, cursor)
            elif opcao == '5':
                # Realize pelo menos 3 consultas e forneça os dados como parâmetro para a função
                dados_consulta = []
                exportar_para_json(dados_consulta, 'consultas.json')
            elif opcao == '6':
                break
            else:
                print("Opção inválida. Tente novamente.")

        # Fechar conexão com o banco de dados ao sair do programa
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
