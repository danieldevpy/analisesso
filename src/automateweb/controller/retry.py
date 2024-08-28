from datetime import datetime

def register_error(error: str):
    # Abre o arquivo no modo de append (adicionar)
    with open('errors.txt', 'a') as f:
        # Escreve a nova linha no arquivo
        f.write(error + '\n')

def retry(fun):
    def wrapper(self, *args, **kwargs):
        total = 10
        for t in range(total):
            try:
                fun(self, *args, **kwargs)
                break
            except Exception as e:
                error = f"{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} /-/ Numero máximo de tentativa execido /-/ relatorio {self.relatorio.name} /-/ função {fun.__name__} /-/ error {str(e)}"
                if t >= total:
                    register_error(error)
                    raise Exception(error)
                
    return wrapper
