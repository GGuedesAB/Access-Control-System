from src.database_setup import dataBaseDriver
from src.database_setup import accessControlUser

class executer:
    def __init__ (self, username, password):
        self.db_driver = dataBaseDriver.dataBaseDriver('localhost', username, password, 'accontrol')

    def execute(self, command, args, command_table):

        try:
            command_arg_type, command_query_order = command_table.get(command)
        except TypeError:
            print ('EXECUTER: Command has execution errors.')
            return 1

        if command_arg_type == 'acsgroup':
            db_command_args = accessControlUser.acsgroup(args.get('number'), args.get('description'))
        elif command_arg_type == 'acsuser':
            db_command_args = accessControlUser.acsuser(args.get('name'), args.get('MAC'), args.get('username'), args.get('password'))
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
                print ('EXECUTER: ' + str(verr.args))
                return 1
        if result is not None :
            print (result)
        
        
