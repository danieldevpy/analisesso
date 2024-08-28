import os, time


class DirectoryController:

    def __init__(self, path:str) -> None:
        self.path = path
        self.check_directory()


    def check_directory(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def get_archives(self):
        return os.listdir(self.path)

    def transfer(self, name):
        while True:
            try:
                archive = os.listdir(self.path)[0]
                last_extension = archive.split('.')[-1]
                if last_extension == 'xls' or last_extension == "xlsx":
                    new_path = self.path.replace(f'temp/{name}', 'all')
                    os.rename(f'{self.path}/{archive}', f'{new_path}/{name}.{last_extension}')
                    break
                else:
                    time.sleep(3)
            except:
                time.sleep(1)

    # def set_list_archives(self):
    #     self.list_archives = os.listdir(self.path)

    # def check_new_archive(self):
    #     archives = os.listdir(self.path)
    #     for archive in archives:
    #         if not archive in self.list_archives:
    #             return archive
    