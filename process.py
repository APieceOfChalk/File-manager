import os
import shutil
import pathlib
from typing import Dict


class FileProcessing:

    @staticmethod
    def get_commands() -> Dict[str, str]:

        commands_dict = {
            "cd": "Перемещение между папками",
            "ls": "Вывод содержимого текущей папки на экран",
            "mkdir": "Создание папки",
            "rmdir": "Удаление папки",
            "create": "Создание файла",
            "rename": "Переименование файла/папки",
            "read": "Чтение файла",
            "remove": "Удаление файла",
            "copy": "Копирование файла/папки",
            "move": "Перемещение файла/папки",
            "write": "Запись в файл",
        }

        return commands_dict

    def __init__(self) -> None:
        self.sep = os.sep
        self.storage = PathStorage(self.sep)

    def mkdir(self, filename: str):
        current_path = self.storage.file2path(filename)
        try:
            os.mkdir(current_path)
        except FileNotFoundError:
            os.makedirs(current_path)
        except FileExistsError:
            print(f"Директория {filename} уже существует")

    def rmdir(self, filename: str):
        current_path = self.storage.file2path(filename)
        try:
            os.rmdir(current_path)
        except OSError:
            try:
                shutil.rmtree(current_path, ignore_errors=False, onerror=None)
            except FileNotFoundError:
                print(f"Директории {filename} не существует")
            except NotADirectoryError:
                print(f"Файл {filename} не является директорией")
        except FileNotFoundError:
            print(f"Директории {filename} не существует")
        except NotADirectoryError:
            print(f"Файл {filename} не является директорией")

    def cd(self, filename: str):
        """
        Перемещение между папками
        - заход в папку по имени
        - выход на уровень вверх
        - в пределах рабочей папки
        """
        self.storage.add_path(filename)
        current_path = self.storage.path

        try:
            os.chdir(current_path)
        except FileNotFoundError:
            self.storage.add_path(f"..{self.sep}")
            print(f"Директории {filename} не существует")
        except NotADirectoryError:
            self.storage.add_path(f"..{self.sep}")
            print(f"Файл {filename} не является директорией")

    def ls(self):

        current_path = self.storage.path
        filelist = os.listdir(current_path)
        for i in range(len(filelist)):
            if os.path.isdir(self.storage.file2path(filelist[i])):
                filelist[i] = f"[dir] {filelist[i]}"
            elif os.path.isfile(self.storage.file2path(filelist[i])):
                filelist[i] = f"[file] {filelist[i]}"

        r = "\n".join(filelist)
        print(f"Содержимое {current_path}:\n{r}")

    def touch(self, filename: str):
        current_path = self.storage.file2path(filename)
        try:
            open(current_path, "a").close()
        except IsADirectoryError:
            print(f"Файл {filename} уже был создан и это директория")

    def cat(self, filename: str) -> str:
        current_path = self.storage.file2path(filename)
        try:
            with open(current_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except IsADirectoryError:
            print(f"Файл {filename} является директорией")

    def rename(self, filename_old: str, filename_new: str):

        path_old = self.storage.file2path(filename_old)
        path_new = self.storage.file2path(filename_new)

        try:
            if not os.path.isfile(path_new):
                os.rename(path_old, path_new)
            else:
                raise IsADirectoryError
        except FileNotFoundError:
            print(f"Указанного файла {filename_old} не существует")
        except IsADirectoryError:
            print(f"Файл с названием {filename_new} уже существует")

    def rm(self, filename: str):
        path = self.storage.file2path(filename)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"Файла {filename} не существует")

    def cp(self, filename: str, path: str):
        path_old = self.storage.file2path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            buff = self.storage.file2path(path)

            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + self.sep + filename)
            else:
                path_new = self.storage.file2path(path)
        try:
            shutil.copyfile(path_old, path_new)
        except IsADirectoryError:
            shutil.copytree(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def mv(self, filename: str, path: str):
        path_old = self.storage.file2path(filename)
        if ".." in path:
            path_new = self.storage.upper_path + self.sep + filename
        else:
            buff = self.storage.file2path(path)
            if os.path.isdir(buff):
                path_new = self.storage.file2path(path + self.sep + filename)
            else:
                path_new = self.storage.file2path(path)
        try:
            shutil.move(path_old, path_new)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def write(self, filename: str, *data: str):
        text = " ".join(data)
        path = self.storage.file2path(filename)
        try:
            with open(path, "a") as file:
                file.write(text)
        except IsADirectoryError:
            print(f"Указанный файл {filename} является директорией")

    def router(self, command: str):

        commands = [
            self.cd,
            self.ls,
            self.mkdir,
            self.rmdir,
            self.touch,
            self.rename,
            self.cat,
            self.rm,
            self.cp,
            self.mv,
            self.write,
        ]
        item_dict = dict(zip(FileProcessing.get_commands().keys(), commands))
        return item_dict.get(command, None)


class PathStorage:

    def __init__(self, sep : str) -> None:
        self.sep = sep
        self.__storage = ["storage"]

    def add_path(self, path: str) -> None:
        if ".." in path and len(self.__storage) != 1:
            self.__storage.pop(-1)
        elif ".." in path:
            print("Выход за из директории")
        else:
            self.__storage.append(path)

    def file2path(self, file_name: str) -> str:
        locale_storage = self.__storage.copy()
        locale_storage.append(file_name)
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(locale_storage)

    @property
    def path(self):
        abs_path = pathlib.Path(__file__).parent.absolute()
        return str(abs_path) + self.sep + self.sep.join(self.__storage)

    @property
    def upper_path(self):
        abs_path = pathlib.Path(__file__).parent.absolute()
        print(self.__storage[1:])
        return str(abs_path) + self.sep + self.sep.join(self.__storage[:1])