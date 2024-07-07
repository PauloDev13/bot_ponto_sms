from utils import (fetch_data, l_cookies)
from class_webdriver import WebDrive


CPF: str = input('Digite o CPF (ex: 123.456.789-00): ')
MONTH_START: int = int(input('Digite o mês de inicial(ex: 01, 02, 10, 11...): '))
YEAR_START: int = int(input('Digite o ano inicial (ex: 2005): '))
MONTH_END: int = int(input('Digite o mês final(ex: 01, 02, 10, 11...): '))
YEAR_END: int = int(input('Digite o ano final (ex: 2005): '))


def main():
    print('CHAMOU')
    driver = WebDrive().driver
    l_cookies('', driver, '')

    message = fetch_data(CPF, MONTH_START, YEAR_START, MONTH_END, YEAR_END, driver)
    print(message)


if __name__ == '__main__':
    main()
