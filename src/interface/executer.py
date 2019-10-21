from src.database_setup import dataBaseDriver
from src.database_setup import accessControlUser
import pymysql.cursors
import pprint

class executer:
    def __init__ (self, username, password):
        self.db_driver = dataBaseDriver.dataBaseDriver('localhost', username, password, 'accontrol')

    def pretty_print (self, d, indent=2):
        for key in d:
            print (d + ': ' + d[key])

    def execute(self, command, args, command_table):

        try:
            command_arg_type, command_query_order = command_table.get(command)
        except TypeError:
            print ('EXECUTER: Command has execution errors.')
            return 1

        if command_arg_type == 'acsgroup':
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
            result = getattr(self.db_driver, command)(db_command_args)
        except ValueError as verr:
            print ('EXECUTER Value Error: ' + str(verr.args))
            return 1
        except TypeError as terr:
            print ('EXECUTER Type Error: ' + str(terr.args))
            return 1
        if result is not None :
            self.pretty_print(result[0])
        
        
