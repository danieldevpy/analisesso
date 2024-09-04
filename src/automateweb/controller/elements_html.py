from src.automateweb.entity.element import Element
from selenium.webdriver.common.by import By


# // pagina login //
input_usuario = Element(
    name="Input Usuario",
    element_search='txtLogin',
    type=By.ID
)
input_password = Element(
    name="Input Password",
    element_search="txtSenha",
    type=By.ID
)
# // pagina login //

# // pagina relatorio //
combo_box_relatrio = Element(
    name="Combo Box Relatorio",
    element_search="ctl00_cphBody_ddlRelatorios",
    type=By.ID
)
btn_add_relatorio = Element(
    name="Botão + de Adicionar Relatorio",
    element_search="ctl00_cphBody_btnAddRelatorio",
    type=By.ID
)
element_await_relatorio = Element(
    name="Div que mostra quando o elemento carregou",
    element_search="ctl00_cphBody_lbRelatorio",
    type=By.ID,
    time=20
)
combo_box_columns = Element(
    name="Combo Box Seleção de Colunas/Categorias",
    element_search="ctl00_cphBody_ddlAdd63",
    type=By.ID
)
all_combo_box_page_relatorio = Element(
    name="Lista com todos os combobox",
    element_search="select",
    type=By.TAG_NAME
)
all_input_image = Element(
    name="Lista com todos os botões +",
    element_search="//input[@type='image']",
    type=By.XPATH
)
all_input_date = Element(
    name="Lista com os inputs de data",
    element_search="dtbPicker hasDatepicker",
    type=By.CLASS_NAME
)
btn_export_relatorio = Element(
    name="Botão de Exportar Relatorio",
    element_search="ctl00_cphBody_btnExportar",
    type=By.ID
)
# // pagina relatorio //