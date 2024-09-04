from src.automateweb.entity.relatorio import Relatorio
from src.automateweb.controller.relatorio import RelatorioController
from typing import List
from threading import Thread
import time

class GerenciadorRelatorios:

    def __init__(self, relatorios: List[Relatorio], folder_temp: str) -> None:
        self.relatorios = relatorios
        self.folder_temp = folder_temp
        self.states = {}
        self.config()

    def config(self):
        for relatorio in self.relatorios:
            self.states[relatorio.name_for_directory()] = None

    def set_state(self, key, value):
        self.states[key] = value

    def check(self):
        while True:
            ok = True
            for _, v in self.states.items():
                if v != True:
                    ok = False
            if ok:
                print("Downloads Finalizado")
                break
            time.sleep(10)

    def start(self):
        print(f'Inicializando {len(self.relatorios)} downloads')
        for relatorio in self.relatorios:
            r_controller = RelatorioController(relatorio, self.folder_temp)
            Thread(target=r_controller.run, args=(self.set_state,)).start()
          