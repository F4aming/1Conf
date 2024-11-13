import argparse
from emulator import ShellEmulator

def main():
    parser = argparse.ArgumentParser(description="Unix Shell Emulator")

    parser.add_argument("-c", "--computer", default="localhost", help="Computer name for prompt")
    parser.add_argument("filename", help="Path to the filesystem tar archive")

    args = parser.parse_args()

    # Создаем экземпляр ShellEmulator с именем компьютера и файлом файловой системы
    emulator = ShellEmulator(args.computer, args.filename)
    emulator.start()

if __name__ == "__main__":
    main()
