import tarfile
import os
import sys


class ShellEmulator:
    def __init__(self, computername, filesystem):
        self.current_path = "/"
        self.computername = computername
        try:
            self.filesystem = tarfile.open(filesystem, "r")
        except FileNotFoundError:
            print(f"Error: Filesystem file '{filesystem}' not found. Exiting.")
            sys.exit(1)

    def start(self):
        """Запуск эмулятора командной строки."""
        while True:
            command = input(f'{self.computername}:{self.current_path}$ ')
            self.execute_command(command)

    def execute_command(self, command):
        """Разбор и выполнение команд shell."""
        command_parts = command.strip().split()

        if not command_parts:
            print("No command entered. Please try again.")
            return

        command_name = command_parts[0]

        if command_name == "ls":
            path = command_parts[1] if len(command_parts) > 1 else self.current_path
            self.ls(path)
        elif command_name == "cd":
            path = command_parts[1] if len(command_parts) > 1 else "/"
            self.cd(path)
        elif command_name == "exit":
            self.filesystem.close()
            sys.exit()
        elif command_name == "pwd":
            self.pwd()
        elif command_name == "rev":
            file_path = command_parts[1] if len(command_parts) > 1 else ""
            self.rev(file_path)
        elif command_name == "head":
            file_path = command_parts[1] if len(command_parts) > 1 else ""
            self.head(file_path)
        else:
            print(f"{command_name}: command not found")

    def ls(self, path):
        """Lists the contents of the specified directory within the virtual filesystem."""
        file_list = self.filesystem.getnames()

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(
                self.current_path, path).replace("\\", "/")

        if full_path == "/":
            result = set()
            for item in file_list:
                tarinfo = self.filesystem.getmember(item)
                if "/" not in item:
                    result.add(item + ("/" if tarinfo.isdir() else ""))
                else:
                    parts = item.split("/")
                    result.add(
                        parts[0] + ("/" if self.filesystem.getmember(parts[0]).isdir() else ""))
            for item in sorted(list(result)):
                print(item)
        else:
            try:
                tarinfo = self.filesystem.getmember(full_path[1:])
                prefix = full_path[1:] + "/"
                result = set()
                for item in file_list:
                    if item.startswith(prefix) and item != prefix:
                        rest = item[len(prefix):]
                        tarinfo = self.filesystem.getmember(item)
                        if "/" not in rest:
                            result.add(rest + ("/" if tarinfo.isdir() else ""))
                        else:
                            parts = rest.split("/")
                            result.add(
                                parts[0] + ("/" if self.filesystem.getmember(prefix + parts[0]).isdir() else ""))
                for item in sorted(list(result)):
                    print(item)
            except KeyError:
                print(f"ls: {path}: No such file or directory")


    def cd(self, path):
        """Меняет текущий каталог."""
        if path == "/":
            self.current_path = "/"
            return

        full_path = path if path.startswith("/") else os.path.join(self.current_path, path).replace("\\", "/")

        try:
            tarinfo = self.filesystem.getmember(full_path[1:])
            if tarinfo.isdir():
                self.current_path = full_path
            else:
                print(f"cd: {path}: Not a directory")
        except KeyError:
            print(f"cd: can't cd to {path}: No such file or directory")

    def pwd(self):
        """Выводит текущий рабочий каталог."""
        print(self.current_path)

    def rev(self, file_path):
        """Выводит содержимое файла в обратном порядке построчно."""
        full_path = os.path.join(self.current_path, file_path).replace("\\", "/")
        try:
            file = self.filesystem.extractfile(full_path[1:])
            if file:
                for line in file:
                    print(line.decode("utf-8").strip()[::-1])
        except KeyError:
            print(f"rev: {file_path}: No such file or directory")
        except Exception as e:
            print(f"Error reading file: {e}")

    def head(self, file_path, lines=10):
        """Выводит первые строки файла (по умолчанию 10 строк)."""
        full_path = os.path.join(self.current_path, file_path).replace("\\", "/")
        try:
            file = self.filesystem.extractfile(full_path[1:])
            if file:
                for i, line in enumerate(file):
                    if i >= lines:
                        break
                    print(line.decode("utf-8").strip())
        except KeyError:
            print(f"head: {file_path}: No such file or directory")
        except Exception as e:
            print(f"Error reading file: {e}")
