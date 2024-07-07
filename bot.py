# Importa a biblioteca Time
# from  time import sleep

# Importa funções declaradas no módulo utils.py
from utils import (open_login)

def main():
    message = open_login()
    print(message)

if __name__ == '__main__':
    main()