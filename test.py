import modules.database as database
import modules.models as models 
import time

b=models.Client("Kayke Moreira", "123.456.789-10", "127.0.0.1")
time.sleep(1)
# b.create_user("Kayke Moreira")
time.sleep(1)
b.deposit(1000)
time.sleep(1)
b.withdraw(100)