from src.database_setup import dataBaseDriver
from src.database_setup import accessControlUser
import pymysql.cursors
import pprint

class executer:
    def __init__ (self, username, password):
        self.db_driver = dataBaseDriver.dataBaseDriver('localhost', username, password, 'accontrol')

    def pretty_print (self, d):
        try:
            return_string = ''
            for element in d:
                for item, value in element.items():
                    return_string += (str(item) + ': ' + str(value) + ' | ')
                return_string += '\n\n'
        except:
            return 'Return from SQL querry is not printable.'
        else:
            return return_string

    def execute(self, current_user, command, args, command_table):

        try:
            command_arg_type, command_query_order = command_table.get(command)
        except TypeError:
            print ('EXECUTER: Command has execution errors.')
            return 1

        if command_arg_type == 'root':
            if current_user.get_username() != 'root':
                return 1
            else:
                db_command_args = None    
        elif command_arg_type == 'self':
            db_command_args = current_user.get_MAC()
        elif command_arg_type == 'acsgroup':
            db_command_args = accessControlUser.acsgroup(args.get('number'), args.get('description'))
        elif command_arg_type == 'acsuser':
            db_command_args = accessControlUser.acsuser(args.get('name'), args.get('MAC'), args.get('username'), args.get('password'), args.get('group_number'))
        elif command_arg_type == 'acsfacility':
            db_command_args = accessControlUser.acsfacility(args.get('name'))
        elif command_arg_type == 'acsaccess':
            db_command_args = accessControlUser.acsaccess(args.get('group_number'), args.get('facility_name'))
        else:
            # Commands that are not listed above have only one argument
            db_command_args = list(args.values())[0]
            
        try:
            if db_command_args is not None:
                result = getattr(self.db_driver, command)(db_command_args)
            else:
                result = getattr(self.db_driver, command)()
        except ValueError as verr:
            print ('EXECUTER Value Error: ' + str(verr.args))
            return 1
        except TypeError as terr:
            print ('EXECUTER Type Error: ' + str(terr.args))
            return 1
        if result is not None :
            return self.pretty_print(result)
        
        
