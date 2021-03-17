
from process import FileProcessing


def main():
    file_processing = FileProcessing()

    while True:

        command = input("\nВведите команду -> ").split(" ")

        if command[0] == "exit":
            break

        result = file_processing.router(command[0])
        if result:
            try:
                result(*command[1:])
            except TypeError:
                print(f"Команда {command[0]} была вызвана с некорректными аргументами")

        else:
            commands_str = "\n".join(
                [
                    f"{key} - {value}"
                    for (key, value) in FileProcessing.get_commands().items()
                ]
            )
            print(f"Команда {command[0]} не найдена! Список команд:\n{commands_str}")

    print("Произведен выход из программы.")


if __name__ == "__main__":
    main()
