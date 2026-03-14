from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)


# 打印格式
def log_title(message: str):
    total_length = 80
    message_length = len(message)
    padding = max(0, total_length - message_length - 4)
    padded_message = f"{'=' * (padding // 2)} {message} {'=' * ((padding + 1) // 2)}"
    print(Fore.CYAN + Style.BRIGHT + padded_message + Style.RESET_ALL)
