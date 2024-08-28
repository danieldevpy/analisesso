from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from automateweb.entity.element import Element
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

class DriverController:

    def __init__(self, path_download, hadless=False, cache=False) -> None:
        self.types = {
            'xpath': By.XPATH,
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME
        }
        prefs = {
            "safebrowsing.enabled": True,
            "download.prompt_for_download": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": path_download
        }
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("prefs", prefs)
        if hadless:
            self.chrome_options.add_argument("--headless=new")
        if cache:
            self.chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options) 
        self.driver.set_window_size(500, 768)

    def get_element(self, element: Element):
        try:
            return WebDriverWait(self.driver, element.time).until(
            EC.visibility_of_element_located((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não encontrado')
        
    def get_elements(self, element: Element):
        try:
           return WebDriverWait(self.driver, element.time).until(
            EC.visibility_of_all_elements_located((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não encontrado')

    def set_value(self, element: Element, value: str, confirm=False):
        element_html = self.get_element(element)
        if confirm:
            element_html.send_keys(value, Keys.ENTER)
        else:
            element_html.send_keys(value)


    def get_element_if_clicable(self, element: Element):
        try:
            return WebDriverWait(self.driver, element.time).until(
                EC.element_to_be_clickable((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não encontrado')
        
    def await_element(self, element: Element):
        try:
            WebDriverWait(self.driver, element.time).until(
                EC.visibility_of_element_located((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não apareceu na pagina')
        
    # // elements dinamics
    def get_element_dinamic(self, element_search: str, type: str, name:str = None, time=10):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((self.types[type], element_search))
                )
        except:
            raise Exception(f"Erro ao tentar pegar {name}")
        
    def get_elements_dinamic(self, elements_search: str, type: str, name:str = None, time=10):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_all_elements_located((self.types[type], elements_search))
            )
        except:
            raise Exception(f"Erro ao tentar pegar {name}")
        
    def await_element_dinamic(self, element_search: str, type: str, name:str = None, time=10):
        try:
            WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((self.types[type], element_search))
            )
        except:
            raise Exception(f'Elemento {name} não apareceu na pagina')