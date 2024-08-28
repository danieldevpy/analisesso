from automateweb.controller.gerenciador import GerenciadorRelatorios
from automateweb.entity.relatorio import Relatorio, Filter
from analise.controller.analise import DataAnalysis
from googlesheet.script import insert_rows

# date = ['29/07/2024', '06/08/2024']
date = ['07/08/2024', '14/08/2024']
path_all = r'/home/daniel/Downloads/relatorios/all'
path_temp = r'/home/daniel/Downloads/relatorios/temp'

relatorio = Relatorio(
    name="TOTAL DE CHAMADOS",
    surname="TOTALDECHAMADOSPRINCIPAL",
    columns=['TIPO VTR', 'TIPO CHAMADO', 'CÓDIGO DO CHAMADO', 'CIDADE', 'IDADE DO PACIENTE', 'AÇÃO SEM INTERVENÇÃO', 'TIPO HD CHAMADO', 'PRIORIDADE (CHAMADO)', 'ÓBITO', 'SEXO DO PACIENTE'],
    filters=[Filter('DATA', date)]
)
relatorio2 = Relatorio(
    name="TOTAL DE CHAMADOS",
    surname="TOTALDECHAMADOSSECUNDARIO",
    columns=['CONDUTA', 'PRIORIDADE (CENA)', 'SUB GRUPO APH CENA', 'CÓDIGO DO CHAMADO'],
    filters=[Filter('DATA', date)]
)
relatorio3 = Relatorio(
    name="TOTAL DE CHAMADOS",
    surname="TOTALDECHAMADOSTHREE",
    columns=['USUÁRIO REGULAÇÃO CHAMADO', 'USUÁRIO ABERTURA CHAMADO', 'HD', 'DATA', 'ENCERRAMENTO', 'ESTABELECIMENTO ORIGEM', 'ESTABELECIMENTO', 'CÓDIGO DO CHAMADO'],
    filters=[Filter('DATA', date)]
)
relatorio4 = Relatorio(
    name="DESTINO PACIENTE",
    columns=['CÓDIGO DO CHAMADO', 'TIPO ESTABELECIMENTO'],
    filters=[Filter('DATA', date)]
)
relatorio5 = Relatorio(
    name="CHAMADOS POR DIA DA SEMANA x HORÁRIO",
    columns=['CÓDIGO DO CHAMADO'],
    filters=[Filter('DATA', date)]
)
relatorio6 = Relatorio(
    name="TOTAL DE ENVIOS POR VTR",
    columns=['CÓDIGO DO CHAMADO'],
    filters=[Filter('DATA', date)]
)

relatorio7 = Relatorio(
    name="TEMPO RESPOSTA ANALÍTICO - PACIENTES CRÍTICOS",
    surname="_CRITICO",
    columns=['APH', 'AÇÃO COM INTERVENÇÃO'],
    filters=[Filter('DATA', date)]
)
relatorio8 = Relatorio(
    name="TEMPO RESPOSTA ANALÍTICO - REGULAÇÃO",
    surname="_REGULACAO",
    columns=['APH', 'AÇÃO COM INTERVENÇÃO'],
    filters=[Filter('DATA', date)]
)
relatorio9 = Relatorio(
    name="TEMPO RESPOSTA ANALÍTICO - TIH",
    surname="_TIH",
    columns=['APH', 'AÇÃO COM INTERVENÇÃO'],
    filters=[Filter('DATA', date)]
)

gerenciador = GerenciadorRelatorios([relatorio, relatorio2], path_temp)
gerenciador.start()
gerenciador.check()
#
# analise = DataAnalysis(path_all)
# analise.load_dfs()
# analise.join_dfs()

