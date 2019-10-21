from src.database_setup import dataBaseDriver
from src.interface import executer
import re

class interpreter:
    
    def __init__ (self, username, password):
        self.command_executer = executer.executer(username, password)
        self.COMMAND_DICT = {
            'define_new_group':                 ('acsgroup',['number', 'description']), 
            'insert_new_user':                  ('acsuser', ['name', 'MAC', 'username', 'password']),
            'insert_new_facility':              ('acsfacility', ['name']),
            'give_access':                      ('acsaccess', ['group_number', 'facility_name']),
            'retrieve_info_from_username':      ('str', ['username']),
            'retrieve_description_from_group':  ('str', ['number']),
            'check_access':                     ('str', ['MAC']),
            'add_user_info':                    ('acsuser', ['name', 'username', 'password', 'MAC']),
            'edit_user':                        ('acsuser', ['name', 'username', 'password', 'group_number', 'MAC']),
            'remove_access':                    ('acsaccess', ['group_number', 'facility_name']),
            'remove_group':                     ('acsgroup', ['number']),
            'remove_user':                      ('acsuser', ['MAC', 'username']),
            'remove_facility':                  ('acsfacility', ['name']),
            'change_group_description':         ('acsgroup', ['description', 'number'])
        }

    def get_command_table (self):
        return self.COMMAND_DICT

    def parse_command (self, command):
        command_args = {}
        result = re.match('(.+) *(\(.*\))', command)
        if result is None:
            raise re.error ('PARSER: Invalid command.')
        command_str = result.group(1)
        args = result.group(2)
        if re.match('\( *\)', args):
            return command_str, None
        command_str = command_str.rstrip()
        if command_str in self.COMMAND_DICT:
            args_parse = re.match('\(([^,]+)=([^,]*),* *(.*)\)$', args)
            last_checked_regexp = ' '
            while args_parse:
                if args_parse.group(2) == '':
                    value = None
                else:
                    value = args_parse.group(2)
                command_args.update({args_parse.group(1):value})
                last_checked_regexp = args_parse.group(3)
                args_parse = re.match('([^,]+)=([^,]*), *(.*)$', args_parse.group(3))
            last_arg = re.match('([^,]+)=([^,]*) *$', last_checked_regexp)
            if last_arg:
                if last_arg.group(2) == '':
                    value = None
                else:
                    value = last_arg.group(2)
                command_args.update({last_arg.group(1):value})
        else:
            raise re.error ('PARSER: Command does not exist.')
        std_cmd_arg_type, std_cmd_args = self.COMMAND_DICT[command_str]
        command_args_as_list = [c for c in command_args.keys()]
        if not set(command_args_as_list) == set(std_cmd_args):
            raise re.error ('PARSER: Wrong arguments in command.')
        return command_str, command_args
        
    def execute (self, command):
        try:
            command, args = self.parse_command(command)
        except re.error as err:
            print(err.msg)
        else:
            self.command_executer.execute(command, args, self.get_command_table())