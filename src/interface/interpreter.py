from src.database_setup import dataBaseDriver
from src.database_setup import accessControlUser
from src.interface import executer
import re

class interpreter:
    
    def __init__ (self):
        self.COMMAND_DICT = {
            'define_new_group':                 ('acsgroup',['number', 'description']), 
            'insert_new_user':                  ('acsuser', ['name', 'MAC', 'username', 'password']),
            'insert_new_facility':              ('acsfacility', ['name']),
            'give_access':                      ('acsaccess', ['group_number', 'facility_name']),
            'retrieve_all_users':               ('root', ['']),
            'retrieve_info_from_username':      ('str', ['username']),
            'retrieve_description_from_group':  ('str', ['number']),
            'retrieve_my_info':                 ('self', ['']),
            'check_access':                     ('self', ['']),
            'add_user_info':                    ('acsuser', ['name', 'username', 'password', 'MAC']),
            'edit_user':                        ('acsuser', ['name', 'username', 'password', 'group_number', 'MAC']),
            'remove_access':                    ('acsaccess', ['group_number', 'facility_name']),
            'remove_group':                     ('acsgroup', ['number']),
            'remove_user':                      ('acsuser', ['MAC', 'username']),
            'remove_facility':                  ('acsfacility', ['name']),
            'change_group_description':         ('acsgroup', ['description', 'number'])
        }

    def user_can_run (self, command):
        normal_user_commands = ['retrieve_description_from_group', 'check_access', 'retrieve_my_info']
        current_user_username = self.current_user.get_username()
        if current_user_username == 'root':
            return True
        else:
            if command in normal_user_commands:
                return True
            else:
                return False
            

    def print_command_table (self):
        command_table_as_string = ''
        for command in sorted(self.COMMAND_DICT):
            if not self.user_can_run(command):
                continue
            first_value = True
            for value in self.COMMAND_DICT[command]:
                if first_value:
                    first_value = False
                    continue
                command_table_as_string += str(command) + ' ('
                for element in value:
                    reversed_list = reversed(value)
                    last_element = next(reversed_list)
                    if element == last_element:
                        command_table_as_string += str(element) + ')'
                    else:
                        command_table_as_string += str(element) + ', '
            command_table_as_string += '\n'
        return command_table_as_string


    def login(self, username, password):
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
            self.command_executer = executer.executer(username, password)

    def get_command_table (self):
        return self.COMMAND_DICT

    def parse_command (self, command):
        command_args = {}
        result = re.match('^(.+) *(\(.*\))$', command)
        if result is None:
            raise re.error ('PARSER: Invalid command.')
        command_str = result.group(1)
        args = result.group(2)
        command_str = command_str.rstrip()
        if command_str in self.COMMAND_DICT:
            if re.match('\( *\)', args):
                return command_str, None
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
            return err.msg
        else:
            return self.command_executer.execute(self.current_user, command, args, self.get_command_table())