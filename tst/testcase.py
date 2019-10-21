from src.interface import interface
from src.interface import interpreter


def root_console (console_dispatcher):
    root_console = console_dispatcher.get_console()
    root_console.run()

def cantine_user_console (console_dispatcher):
    cantine_user_console = console_dispatcher.get_console()
    cantine_user_console.run()

def third_party_console (console_dispatcher):
    third_party_user_console = console_dispatcher.get_console()
    third_party_user_console.run

if __name__ == '__main__':
    console_dispatcher = interface.console_manager()
    root_console(console_dispatcher)