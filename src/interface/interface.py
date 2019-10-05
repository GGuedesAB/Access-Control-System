# This is an interface for admin
import logging
from src.interface import interpreter

class console_factory ():
    def __init__ (self):
        self.number_of_instances = 0
        self.instance_dict = {}

    def get_console (self):
        self.console = console(self.id)
        self.id = self.number_of_instances
        self.number_of_instances += 1
        self.instance_dict.update({self.id : self.console})
        return self.console


class console ():
    def __init__ (self, console_id):
        self.id = console_id
        self.create_logger ()

    def create_logger (self):
	    log_format = "%(asctime)s - %(levelname)s: %(message)s"
	    date_format = '%d-%m-%Y %H:%M:%S'
	    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)
	    
    def run (self):
        try:
            while (True):
                command = input ('-->')
                interpreter.execute(command)
        except KeyboardInterrupt:
            logging.info('Console exit.')
            return 2



def main ():
    my_console = console_factory.get_console()
    my_console.run()

if __name__ == "__main__":
    main()