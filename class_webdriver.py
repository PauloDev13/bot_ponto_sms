import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WebDrive(metaclass=SingletonMeta):
    driver = None

    def __init__(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://natal.rn.gov.br/sms/ponto/index.php')
        driver.implicitly_wait(15)

        self.driver = driver
