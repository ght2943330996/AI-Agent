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


def print_welcome():
    """打印 DummyCode 欢迎页面"""
    print()
    # Logo ASCII 艺术 - 大号 DummyCode
    logo = f"""{Fore.CYAN}{Style.BRIGHT}
    ██████╗ ██╗   ██╗███╗   ███╗███╗   ███╗██╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗
    ██╔══██╗██║   ██║████╗ ████║████╗ ████║██║   ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ██║  ██║██║   ██║██╔████╔██║██╔████╔██║██║   ██║██║     ██║   ██║██║  ██║█████╗
    ██║  ██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║██║     ██║   ██║██║  ██║██╔══╝
    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝╚██████╗╚██████╔╝██████╔╝███████╗
    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝{Style.RESET_ALL}
    """
    print(logo)

    # 欢迎语
    print(f"    {Style.BRIGHT}{Fore.CYAN}欢迎使用 DummyCode{Style.RESET_ALL}")
    print(f"    {Fore.LIGHTBLACK_EX}一款基于 LLM + MCP + RAG 的智能代码助手{Style.RESET_ALL}")
    print()

    # 快速开始提示
    print(f"    {Style.BRIGHT}快速开始:{Style.RESET_ALL}")
    print(f"      {Fore.YELLOW}/help{Style.RESET_ALL}  {Fore.LIGHTBLACK_EX}- 查看所有可用命令{Style.RESET_ALL}")
    print(f"      {Fore.YELLOW}/new{Style.RESET_ALL}   {Fore.LIGHTBLACK_EX}- 创建新会话{Style.RESET_ALL}")
    print(f"      {Fore.YELLOW}/list{Style.RESET_ALL}  {Fore.LIGHTBLACK_EX}- 列出所有会话{Style.RESET_ALL}")
    print()

    # 分隔线
    print(f"    {Fore.LIGHTBLACK_EX}{'─' * 60}{Style.RESET_ALL}")
