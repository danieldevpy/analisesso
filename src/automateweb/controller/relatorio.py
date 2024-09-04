from src.automateweb.controller.driver import DriverController
from src.automateweb.entity.relatorio import Relatorio
from src.automateweb.controller import elements_html
from src.automateweb.controller.retry import retry
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.support.ui import Select
from src.automateweb.controller.directory import DirectoryController
import time


class RelatorioController:

    def __init__(self, relatorio: Relatorio, path_download) -> None:
        self.relatorio = relatorio
        self.path = f'{path_download}/{relatorio.name_for_directory()}'
        self.directory = DirectoryController(self.path)
        self.driver_controller = DriverController(self.path)

    @retry
    def get_page(self, url: str):
        self.driver_controller.driver.get(url)
        if self.driver_controller.driver.current_url != url:
            raise
        
    @retry
    def __await_box_fields__(self, id_combo, value):
        select_columns = self.driver_controller.get_element_dinamic(f'ctl00_cphBody_lbAdd{id_combo}', 'id', 'est')
        size = select_columns.get_attribute("size")
        if int(size) != value:
            time.sleep(1)
            raise

    @retry
    def __await_box_relatorio__(self):
        # verifico se o botão de adicionar relatorio está na tela e em seguida eu clico nele
        self.driver_controller.get_element_if_clicable(elements_html.btn_add_relatorio).click()
        # uso a função await para verificar se o relatorio já foi adicionado
        self.driver_controller.await_element(elements_html.element_await_relatorio)

    def login(self):
        # acessa o site de login do sso
        self.get_page('https://cisbaf.ssosamu.com:3001/SSONOVAIGUACU/login.aspx')
        # seta o valor no input de usuário
        self.driver_controller.set_value(elements_html.input_usuario, 'Daniel.Fernandes')
        # seta o valor no input de password e já aperta o enter na variavel confirm
        self.driver_controller.set_value(elements_html.input_password, '42658265', confirm=True)
        time.sleep(2)
        try:
            Alert(self.driver_controller.driver).accept()
        except:
            pass
        self.driver_controller.get_element_dinamic('//*[@id="btnAtualizar"]', 'xpath', 'btn login').click()


    def select_relatorio(self):
        # variavel para verificar se o relatorio foi encontrado
        encontred = False
        # acessa o site de relatorios do sso
        self.get_page('https://cisbaf.ssosamu.com:3001/SSONOVAIGUACU/_Relatorio/frmConsultaRelatorioNovo.aspx')
        # obtenho o elemento select do relatorio
        try:
            element_select = self.driver_controller.get_element(elements_html.combo_box_relatrio)
        except:
            element_select = self.driver_controller.get_element(elements_html.combo_box_relatrio)
        # atributo o element select para a classe Select do selenium
        select = Select(element_select)
        # faço um for em todas as opções do select
        for option in select.options:
            # verificação se a opção do select é igual ao nome do relatorio
            if option.text == self.relatorio.name:
                # após encontrar a opção correta eu escolho a opção no elemento select
                select.select_by_value(option.get_attribute('value'))
                # caso encontre altere o valor para True
                encontred = True
        if not encontred:
            raise Exception("Relatório não encontrado, verifique o nome")

        self.__await_box_relatorio__()

    @retry
    def __await__click__(self, option, select_fields, button_fields):
        select_fields.select_by_value(option.get_attribute('value'))
        time.sleep(0.5)
        button_fields.click()
        time.sleep(3)

    def insert_fields(self):
        for i, field in enumerate(self.relatorio.columns):
            all_selects = [Select(select) for select in self.driver_controller.get_elements(elements_html.all_combo_box_page_relatorio)]
            all_buttons = self.driver_controller.get_elements(elements_html.all_input_image)
            select_fields = all_selects[2]
            button_fields = all_buttons[2]
            number_id_section = all_buttons[2].get_attribute("id")[23:]
            encontred = False
            for option in select_fields.options:
                if field == option.text:
                    encontred = True
                    self.__await__click__(option, select_fields, button_fields)
                    self.__await_box_fields__(number_id_section, i+1)
                    break
            if not encontred:
                raise Exception(f"Field {field} não encontrado")
            time.sleep(1)
                
    def insert_filter(self):
        for filter in self.relatorio.filters:
            all_selects = [Select(select) for select in self.driver_controller.get_elements(elements_html.all_combo_box_page_relatorio)]
            all_buttons = self.driver_controller.get_elements(elements_html.all_input_image)
            select_filter = all_selects[5]
            button_filter = all_buttons[5]
            encontred = False
            for option in select_filter.options:
                if filter.name == option.text:
                    select_filter.select_by_value(option.get_attribute('value'))
                    button_filter.click()
                    time.sleep(4)
                    try:
                        fields_date = self.driver_controller.get_elements_dinamic('hasDatepicker', 'class', 'teste')
                    except:
                        fields_date = self.driver_controller.get_elements_dinamic('hasDatepicker', 'class', 'teste')
                    dates = filter.get_date()
                    for i, field in enumerate(fields_date):
                        id_element = field.get_attribute('id')
                        command = f"document.getElementById('{id_element}').value = '{dates[i]}';"
                        self.driver_controller.driver.execute_script(command)
                        field.click()
                    encontred = True
                    break
            if not encontred:
                raise Exception(f"Field {filter.name} não encontrado")
   

    def export_relatorio(self):
        btn = self.driver_controller.get_element_if_clicable(elements_html.btn_export_relatorio)
        self.driver_controller.driver.execute_script(f"arguments[0].click();", btn)
    

    def run(self, state):
        try:
            self.login()
            time.sleep(1)
            self.select_relatorio()
            time.sleep(1)
            self.insert_fields()
            time.sleep(1)
            self.insert_filter()
            time.sleep(1)
            self.export_relatorio()
            time.sleep(1)
            self.directory.transfer(self.relatorio.name_for_directory())
            time.sleep(5)
            self.driver_controller.driver.quit()
            state(self.relatorio.name_for_directory(), True)
        except:
            state(self.relatorio.name_for_directory(), False)
