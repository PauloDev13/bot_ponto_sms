# Importa as dependencias da biblioteca da botcity
from botcity.web.parsers import table_to_dict
from botcity.plugins.excel import BotExcelPlugin

# Importa as ferramentas da biblioteca Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Importa a dependencia do ChromeDriverManager do webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
# Importa a biblioteca settings
from settings import Settings
# Importa sleep da biblioteca Time
from time import sleep

import pickle

from class_webdriver import WebDrive

# Cria um novo arquivo do tipo excel
excel: BotExcelPlugin = BotExcelPlugin()

# Define as variáveis
# CPF: str = input('Digite o CPF (ex: 123.456.789-00): ')
# MONTH_START: int = int(input('Digite o mês de inicial(ex: 01, 02, 10, 11...): '))
# YEAR_START: int = int(input('Digite o ano inicial (ex: 2005): '))
# MONTH_END: int = int(input('Digite o mês final(ex: 01, 02, 10, 11...): '))
# YEAR_END: int = int(input('Digite o ano final (ex: 2005): '))

def open_login():
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = WebDrive().driver

    def s_cookies(self, browser, loc):
        pickle.dump(browser.get_cookies(), open(loc, 'wb'))

    # driver.get("https://natal.rn.gov.br/sms/ponto/index.php")

    # Encontra o input de entrada do login, insere o login do usuário e pressiona TAB
    user = driver.find_element(by=By.XPATH, value="//*[@id='cpf']")
    user.send_keys(Settings().USER_LOGIN)
    user.send_keys(Keys.TAB)

    # Espera 1 segundo
    sleep(1)

    # Encontra o input de entrada da senha, digita insere a senha do usuário
    password = driver.find_element(by=By.XPATH, value="//*[@id='senha']")
    password.send_keys(Settings().USER_PASSWORD)

    # Localiza o primeiro Iframe da página e entra nele
    driver.switch_to_frame(0)
    # Localiza dentro Iframe o elemento que tem o box do recaptcha e clica nele
    cap = driver.find_element(by=By.XPATH,  value="//*[@id='recaptcha-anchor']")
    cap.click()
    # Sai do Iframe e volta para o html principal
    driver.switch_to_default_content()

    # Espera 15 segundos
    sleep(15)

    # Encontra o button de entrada e clica
    button = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
    button.click()
    # Espera 2 segundos
    sleep(2)

    # Minimiza a janela do navegador
    driver.minimize_window();

    return fetch_data(CPF, MONTH_START, YEAR_START, MONTH_END, YEAR_END, driver)
# FIM DA FUNÇÃO OPEN_LOGIN
#*********************************************

def fetch_data(
        cpf: str, month_start: int, year_start: int,
        month_end: int, year_end: int, driver: any
) -> str:
    try:
        # Faz um laço usando o ano inicial e o ano final
        for year in range(year_start, year_end + 1):
            # Se o ano inicial igual ao ano final
            if year_start == year_end:
                # Chama a função loop_for_data que lê os dados da tabela
                loop_for_data(cpf, month_start, month_end + 1, year, driver)
            # Se o ano igual ao ano inicial
            elif year == year_start:
                # Chama a função loop_for_data que lê os dados da tabela
                loop_for_data(cpf, month_start, 13, year, driver)
            # Se o ano menor que ano final
            elif year < year_end:
                # Chama a função loop_for_data que lê os dados da tabela
                loop_for_data(cpf, 1, 13, year, driver)
            # Qualquer outra condição
            else:
                # Chama a função loop_for_data que lê os dados da tabela
                loop_for_data(cpf, 1, month_end + 1, year, driver)

        # Chama a função month_description para pegar o nome do mês inicial e final
        start_month: str = month_description(month_start)
        end_month: str = month_description(month_end)

        # Cria o arquivo do Excel e salva no diretório
        excel.write(
            fr'C:\Users\prmorais\Desktop\BOT\{name_employee()}_DE_{start_month}.{year_start}_A_{end_month}.{year_end}.xlsx')

        message: str = 'Arquivo gerado com sucesso!'
        # Espera 3 segundos
        sleep(1)
        # Fecha a instância do navegador

    except:
        message: str = 'Erro ao gerar Arquivo. Tente novamente!'

    return message
# FIM DA FUNÇÃO FETCH_DATA
#************************************************************

# Retorna o valor da variável str_name_employee capturado na função loop_for_data()
def name_employee() -> str:
    return str_name_employee

# Fução de apoio
# Recebe os parâmetros CPF, MÊS_INICIAL, MÊS FINAL, ANO e uma instância do navegador
# Faz loop usando o intervalo mês inicial e mês final
def loop_for_data(cpf: str, month_start: int, month_end: int, year: int, driver: any) -> None:
    print(f'DRIVER: {driver}')
    global str_name_employee

    for month in range(month_start, month_end):
        # Monta a URL com os query params CPF, Mês e Ano para acessar os dados
        driver.get(
            f'https://natal.rn.gov.br/sms/ponto/interno/aprova_justificativa/detalhes.php?cpf={cpf}&mes={month}&ano={year}')

        # Atribui a variável str_name_employe o valor contido no span (nome do servidor)
        str_name_employee = driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]').text

        # Acessa a tabela e transforma os dados coletados num array de dicionários
        data_table = driver.find_element(by=By.XPATH, value="//*[@id='mesatual']/table")
        data = table_to_dict(data_table)

        # Adciona linhas de cabeçalho em cada mês no arquivo do Excel
        excel.add_row('*****************************************************************')
        excel.add_row(f'{month_description(month)}/{year}')
        excel.add_row('*****************************************************************')
        excel.add_row(
            [
                'DATA ENTRADA',
                'ENTRADA',
                'DATA SAÍDA',
                'SAÍDA',
                'TRABALHADA',
                'JUSTIFICADA',
                'STATUS'
            ]
        )

        # Chama a função add_data_rows_excel que adiciona os dados no arquivo Excel
        add_data_rows_excel(data)

# Função de apoio
# Recebe como parâmetro um array de dados e faz um loop nele
def add_data_rows_excel(data) -> None:
    # Atribui às variáveis os valores do array
    for item in data:
        str_data_entrada: str = item.get('data_entrada')
        str_entrada = item.get('entrada')
        str_data_saida: str = item.get('data_saída')
        str_saida = item.get('saída')
        str_trabalhada = item.get('trabalhada')
        str_hora_justificada = item.get('hora_justificada')
        str_status = item.get('status')

        # Adciona nova linha no arquivo do Excel a cada interação com os valores das variáveis
        # setados acima
        excel.add_row(
            [
                str_data_entrada,
                str_entrada,
                str_data_saida,
                str_saida,
                str_trabalhada,
                str_hora_justificada,
                str_status
            ]
        )


# Retorna o nome dos meses abreviado
def month_description(month: int) -> str:
    month_array = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    return month_array[month - 1]


def s_cookies(self,browser, loc):
    pickle.dump(browser.get_cookies(), open(loc,'wb'))

def l_cookies(self,browser, loc, url=None):
    cookies = pickle.load(open(loc,'rb'))

    url = "https://google.com" if url is None else url
    browser.get(url)
    for cookie in cookies:
        browser.add_cookie(cookie)