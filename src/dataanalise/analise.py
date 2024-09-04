import pandas as pd
from src.automateweb.controller.directory import DirectoryController
from typing import Dict
import os

class DataAnalysis:

    def __init__(self, path: str) -> None:
        self.dfs:Dict[str, pd.DataFrame] = {}
        self.df_principal: pd.DataFrame = None
        self.path = path
        self.messages = []
        

    def load_dfs(self):
        archives = DirectoryController(self.path).get_archives()
        for archive in archives:
            if archive != 'finaldf.xlsx':
                path = self.path + '/' + archive
                init = archive[0]
                if archive == 'TOTALDECHAMADOSPRINCIPAL.xls':
                    self.df_principal = pd.read_html(path)[0]
                    column_names = self.df_principal.iloc[2]
                    self.df_principal = self.df_principal[3:]
                    self.df_principal.columns = column_names
                    self.df_principal.columns = ['IDADE' if pd.isna(col) else col for col in self.df_principal.columns]
                    self.df_principal = self.df_principal.reset_index(drop=True)
                else:
                    df = pd.read_html(path)[0]
                    column_names = df.iloc[2]
                    df = df[2:]
                    df.columns = column_names
                    if 'TOTAL' in df.columns:
                        df = df.drop('TOTAL', axis=1)
                    if init == '_':
                        df = df[['APH', 'CHAMADO']]
                        df = df.rename(columns={'APH': f'APH{archive.split('.')[0]}'})
                    df = df.reset_index(drop=True)
                    self.dfs[archive.split('.')[0]] = df
    
    def join_dfs(self):
        for _, df in self.dfs.items():
            for name_col in df.columns.values:
                if name_col != 'CÓDIGO DO CHAMADO' and name_col != "CHAMADO":
                    self.df_principal[name_col] = ''

        errors = []
        shape = self.df_principal.shape[0]

        for i in range(shape):
            row_value = self.df_principal.at[i, 'CÓDIGO DO CHAMADO']
            for df_name, df in self.dfs.items():
                try:
                    try:
                        index_linha = df[df['CÓDIGO DO CHAMADO'] == row_value].index
                    except:
                            new_row_value = row_value.split('/')[0]
                            index_linha = df[df['CHAMADO'] == new_row_value].index
                            if not index_linha:
                                errors.append(f"Não encontrado código de chamado em linha {i}")

                    if not index_linha.empty:
                        match_index = index_linha[0]
                        for col in df.columns:
                            if col != "CÓDIGO DO CHAMADO" and col != "CHAMADO":
                                value = df.at[match_index, col]
                                self.df_principal.at[i, col] = value

                except Exception as e:
                    errors.append(f"Error processing dataframe {df_name} at index {i}: {e}")

            mult = i * 100
            por = int(mult / shape)
            os.system('clear')
            print(f'Gerando relatorio final - Progresso ({i}/{shape}) {por}%')

        column_order = [
            'TIPO VTR', 'TIPO HD CHAMADO', 'TIPO CHAMADO', 'SEXO DO PACIENTE',	'PRIORIDADE (CHAMADO)',	'ÓBITO', 'IDADE',
            'IDADE DO PACIENTE', 'CÓDIGO DO CHAMADO', 'CIDADE', 'AÇÃO SEM INTERVENÇÃO', 'TOTAL', 'APH_CRITICO',
            'APH_REGULACAO', 'APH_TIH', 'SUB GRUPO APH CENA', 'PRIORIDADE (CENA)', 'CONDUTA', 'TIPO ESTABELECIMENTO',
            'HOSPITAL',	'PLACA', 'VEÍCULO (BASE)', 'DIA DA SEMANA', 'HORA',	'HD', 'DATA', 'ESTABELECIMENTO ORIGEM',
            'ESTABELECIMENTO', 'ENCERRAMENTO', 'USUÁRIO REGULAÇÃO CHAMADO', 'USUÁRIO ABERTURA CHAMADO'
        ]
        
        columns_present = [col for col in column_order if col in self.df_principal.columns]

        self.df_principal = self.df_principal[columns_present]

        self.df_principal.to_excel(self.path+'/'+'finaldf.xlsx', engine="openpyxl", index=False)

        os.system('clear')
        msg_final = f'Gerando relatorio final - Progresso ({shape}/{shape}) 100%'
        self.messages.append(msg_final)
        print(msg_final)
        print("errors:", errors)

    def treat_for_google_sheet(self):
        df = pd.read_excel(self.path+'/'+'finaldf.xlsx')
        df.fillna('', inplace=True)
        df['TOTAL'] = df['TOTAL'].astype(int, errors='ignore')
        shape = df.shape[0]
        new_rows = []
        for i, row in enumerate(df.values[:-1]):
            new_rows.append([str(data) for data in row])
            mult = i * 100
            por = int(mult / shape)
            os.system('clear')
            if len(self.messages) > 0:
                print(self.messages[0])
            print(f'Tratamento de dados sheets - Progresso ({i}/{shape}) {por}%')
        
        os.system('clear') 
        if len(self.messages) > 0:
            print(self.messages[0])
        print(f'Tratamento de dados sheets - Progresso ({shape}/{shape}) 100%')

        return new_rows