import sqlite3
import os

class Connection():
    def __init__(self, database):
        self.__connection = sqlite3.connect(database) # Tabela de alterações de informações da conta
        self.__cur = self.__connection.cursor() # CEP, Endereço, Complemento, Telefone, Senha, Email
        transactions_attributes_definition = "( data_hora varchar(255) NOT NULL, cpf varchar(11) UNIQUE NOT NULL, titular varchar(255) NOT NULL, ip varchar(45) NOT NULL, operacao varchar(1) NOT NULL, quantia real NOT NULL )"
        self.create_table_if_not_exists("transacoes", transactions_attributes_definition)
        clients_attributes_definition = "( id_conta integer NOT NULL primary key AUTOINCREMENT, cpf varchar(11) NOT NULL unique, titular varchar(255) NOT NULL, saldo real NOT NULL)"
        self.create_table_if_not_exists("contas", clients_attributes_definition)
    def execute_query(self, query, params=()):
        response = self.__cur.execute(query, params).fetchone()
        self.__connection.commit()
        return response
    def create_table_if_not_exists(self, table_name, table_attributes): 
        self.execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} {table_attributes}")
    def register_transaction(self, client_name, client_cpf, client_ip, operation, amount, date):
        sql = "INSERT INTO transacoes (data_hora, cpf, titular, ip, operacao, quantia) VALUES (?, ?, ?, ?, ?, ?)"
        params = (date, client_cpf, client_name, client_ip, operation, amount,)
        # print("PARAMS",params)
        self.execute_query(sql, params)
    def get_money(self, client_cpf):
        try:
            return self.execute_query("SELECT saldo FROM contas WHERE cpf = ?",(client_cpf,))[0]
        except:
            raise 
    def withdraw(self, client_cpf, amount):
        self.execute_query("UPDATE contas SET saldo = saldo - ? WHERE cpf = ?",(amount,client_cpf,))
    def deposit(self, client_cpf, amount):
        self.execute_query("UPDATE contas SET saldo = saldo + ? WHERE cpf = ?",(amount,client_cpf,))
    def create_user(self, client_name, client_cpf):
        sql = "INSERT OR IGNORE INTO contas (cpf, titular, saldo) VALUES (?, ?, 0)"
        self.execute_query(sql,(client_cpf, client_name,))
    def disconnect(self):
        self.__connection.close()
