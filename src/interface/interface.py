# This is an interface for admin
import getpass
from src.tools import logger
from src.database_setup import accessControlUser
from src.database_setup import dataBaseDriver
from src.interface import interpreter

class console_manager:

    class __console_manager:
        def __init__ (self):
            pass
        def __str__ (self):
            return repr(self)

    instance = None

    def __init__ (self):
        self.logger = logger.acsLogger()
        self.logger.set_warning()

        if not console_manager.instance:
            console_manager.instance = console_manager.__console_manager()
            self.number_of_instances = 1
            self.instance_dict = {}

        else:
            self.logger.error ('Only one instance of console manager can be created.')
            exit(1)
        
    def get_console (self):
        self.id = self.number_of_instances
        self.console = console(self.id, True)
        self.number_of_instances += 1
        self.instance_dict.update({self.id : self.console})
        return self.console

    def list_consoles (self):
        return self.instance_dict

    def deactivate_console (self, console):
        console.is_active = False

    def destroy_console (self, console):
        self.deactivate_console(console)
        to_be_killed_console_id = console.get_id()
        del self.instance_dict[to_be_killed_console_id]
        self.logger.warning ('Killing console ' + str(to_be_killed_console_id))

class console:
    def __init__ (self, console_id, is_active):
        try:
            print ('Please identify yourself.')
            username = input('Username: ')
            # password = getpass.getpass()
            password = input('Password: ')
        except KeyboardInterrupt:
            print ('\n')
            exit (2)
        db_driver = dataBaseDriver.dataBaseDriver('localhost', username, password, 'accontrol')
        try:
            info = db_driver.retrieve_info_from_username(username)[0]
        except IndexError as iderr:
            print ('ERROR: ' + iderr.args)
            exit(1)
        except UnboundLocalError as uberr:
            print ('ERROR: ' + uberr.args)
            exit(1)
        else:
            self.current_user = accessControlUser.acsuser(info.get('name'), info.get('MAC'), username, password)
            self.is_active = is_active
            self.id = console_id
            self.interpreter = interpreter.interpreter()
            self.interpreter.login(username, password)
            self.logger = logger.acsLogger()
            self.logger.set_warning()

    def get_id (self):
        return self.id

    def run (self):
        if self.is_active:
            try:
                while (True):
                    command = input ('-->')
                    print (command)
                    self.interpreter.execute(command)
            except KeyboardInterrupt:
                print ('\n')
                self.logger.warning('Console exit.')
                return 2
            except EOFError:
                self.logger.info ('Finished reading script.')
                return 0
        else:
            self.logger.error('Cannot reach console.')

def main():
    console_fac = console_manager()
    console_1 = console_fac.get_console()
    console_1.run()

if __name__ == "__main__":
    main()