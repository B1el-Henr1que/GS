import oracledb
import json

def menu():
    print("Escolha uma opção:")
    print("1 - Inserir")
    print("2 - Consultar")
    print("3 - Alterar")
    print("4 - Excluir")
    print("5 - Exportar Consultas para JSON")
    print("6 - Sair")

def inserir(conn, cursor):
    id = int(input("Digite o ID: "))
    nome = input("Digite o nome: ")
    idade = int(input("Digite a idade: "))
    sql = "INSERT INTO Pacientes (id, nome, idade) VALUES (:id, :nome, :idade)"
    cursor.execute(sql, {"id": id, "nome": nome, "idade": idade})
    conn.commit()
   

def consultar(conn, cursor):
    sql = "SELECT * FROM Pacientes"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(json.dumps(rows))
    with open('consulta.json', 'w') as f:
        json.dump(rows, f)

def alterar(conn, cursor):

    idade = int(input("Digite a nova idade: "))
    id_pessoa = int(input("Digite o ID da pessoa a ser alterada: "))
    sql = "UPDATE Pacientes SET idade = :idade WHERE id = :id_pessoa"
    cursor.execute(sql, {"idade": idade, "id_pessoa": id_pessoa})
    conn.commit()

def excluir(conn, cursor):
    id_pessoa = int(input("Digite o ID da pessoa a ser excluída: "))
    sql = "DELETE FROM Pacientes WHERE id = :id_pessoa"
    cursor.execute(sql, {"id_pessoa": id_pessoa})
    conn.commit()

def main():
    try:
        conn = oracledb.connect(user = 'RM99463',password = '310803',dsn = 'oracle.fiap.com.br/orcl')
        cursor = conn.cursor()
        while True:
            menu()
            opcao = int(input("Digite a opção: "))
            if opcao == 1:
                inserir(conn, cursor)
            elif opcao == 2:
                consultar(conn, cursor)
            elif opcao == 3:
                alterar(conn, cursor)
            elif opcao == 4:
                excluir(conn, cursor)
            elif opcao == 5:
                consultar(conn, cursor)
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")
    except oracledb.Error as e:
        print(f"Erro: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()