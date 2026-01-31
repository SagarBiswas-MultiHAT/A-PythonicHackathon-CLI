from sagar_assistant import handle_command


def single_line() -> None:
    context = None
    print("\nHi, I'm Sagar. How can I help you?\n")

    while True:
        try:
            command = input("==> ")
        except (EOFError, KeyboardInterrupt):
            print("\n..:: Goodbye.")
            break

        if command.lower() == "exit":
            print("\n..:: Goodbye.")
            break

        try:
            context, response = handle_command(command, context)
            print(f"\n{response}\n")
        except RuntimeError as exc:
            print(f"\n..:: Error: {exc}\n")
        except Exception:
            print("\n..:: Unexpected error. Please try again.\n")


def multi_line() -> None:
    context = None
    print("\nHi, I'm Sagar. How can I help you?\n")

    while True:
        print("Enter your command (type 'END' on a new line to finish): ", end="")
        lines = []
        try:
            while True:
                line = input()
                if line.upper() == "END":
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\n..:: Goodbye.")
            break

        command = "\n".join(lines)

        if command.lower() == "exit":
            print("\n..:: Goodbye.")
            break

        try:
            context, response = handle_command(command, context)
            print(f"\n{response}\n")
        except RuntimeError as exc:
            print(f"\n..:: Error: {exc}\n")
        except Exception:
            print("\n..:: Unexpected error. Please try again.\n")


if __name__ == "__main__":
    single_line()
