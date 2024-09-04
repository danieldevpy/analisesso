from src.dataanalise.analise import DataAnalysis
from config import path_all

analise = DataAnalysis(path_all)
analise.load_dfs()
analise.join_dfs()
