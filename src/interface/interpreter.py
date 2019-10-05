from src.database_setup import dataBaseDriver
from src.interface import executer
import re

class interpreter:
    
    def __init__ (self):
        self.COMMAND_DICT = {
            'define_new_group':             ('acsgroup',['number', 'description']), 
            'insert_new_user':              ('acsuser', ['name', 'MAC', 'username', 'password']),
            'insert_new_facility':          ('acsfacility', ['name']),
            'give_access':                  ('acsaccess', ['group_number', 'facility_name']),
            'retrieve_info_from_username':  ('str', ['username']),
            'check_access':                 ('str', ['MAC']),
            'add_user_info':                ('acsuser', ['name', 'username', 'password', 'MAC']),
            'edit_user':                    ('acsuser', ['id', 'name', 'MAC', 'username', 'password', 'group_number', 'MAC']),
            'remove_access':                ('acsaccess', ['group_number', 'facility_name']),
            'remove_group':                 ('acsgroup', ['number']),
            'remove_user':                  ('acsuser', ['MAC', 'username']),
            'remove_facility':              ('acsfacility', ['name']),
            'change_group_description':     ('acsgroup', ['description', 'number'])
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
            args_parse = re.match('\(([^,]+)=([^,]+),* *(.*)\)$', args)
            last_checked_regexp = ' '
            while args_parse:
                command_args.update({args_parse.group(1):args_parse.group(2)})
                last_checked_regexp = args_parse.group(3)
                args_parse = re.match('([^,]+)=([^,]+), *(.*)$', args_parse.group(3))
            last_arg = re.match('([^,]+)=([^,]+) *$', last_checked_regexp)
            if last_arg:
                command_args.update({last_arg.group(1):last_arg.group(2)})
        else:
            raise re.error ('PARSER: Command does not exist.')
        std_cmd_arg_type, std_cmd_args = self.COMMAND_DICT[command_str]
        command_args_as_list = [c for c in command_args.keys()]
        if not set(command_args_as_list) == set(std_cmd_args):
            raise re.error ('PARSER: Wrong arguments in command.')
        return command_str, command_args
        
    def execute (self, command):
        command_executer = executer.executer()
        try:
            command, args = self.parse_command(command)
        except re.error as err:
            print(err.msg)
        else:
            command_executer.execute(command, args, self.get_command_table())