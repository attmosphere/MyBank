import random
import time
import os 
try:
    import database
except ModuleNotFoundError:
    import modules.database as database

class Client:
    def __init__(self, name, cpf, ip):
        self._name = name
        self.__cpf = cpf
        self.__money = 0
        self.__ip = ip
        self.filename_ = f"mybank_database.db"
        self.database_instance = database.Connection(self.filename_)
        self.database_instance.create_user(name, cpf)
    @property
    def money(self):
       account_money = self.database_instance.get_money(f"\"self._name\"")
       return account_money
    @money.setter
    def money(self, *args, **kwargs):
        raise PermissionError("Não é possível modificar o dinheiro diretamente.")
    def register_transaction(self, amount, op): 
        time_now = time.ctime()
        self.database_instance.register_transaction(client_name=self._name, client_cpf=self.__cpf, client_ip=self.__ip, operation=op, amount=amount, date=time_now)
    def deposit(self, amount): # adiciona dinheiro no saldo
        if amount < 0: 
            raise ValueError("O valor do depósito deve ser positivo.")
        elif not isinstance(amount, (int, float)):
            raise ValueError("Apenas números.")
        self.database_instance.deposit(self.__cpf, amount)
        self.register_transaction(amount, "+")
        return True
    def withdraw(self, amount): # tira dinheiro do saldo
        money = self.database_instance.get_money(self.__cpf)
        if amount > money:
            raise PermissionError("O valor do saque excede o saldo na sua conta.")
        elif not isinstance(amount, (int, float)):
            raise ValueError("Apenas números.")
        elif amount < 0:
            raise ValueError("O valor do saque deve ser positivo.")
        self.database_instance.withdraw(self.__cpf, amount)
        self.register_transaction(amount, "-")
        return True
    def __str__(self):
        return f"Nome do titular: {self._name} {self.__cpf}\nSaldo: ${self.__money}"
    def create_user(self, name, cpf):
        self.database_instance.create_user(name, cpf)
            
        


if __name__ == "__main__":
    print("Isso não é feito para ser executado diretamente. Por favor execute a aplicação principal (main.py)")