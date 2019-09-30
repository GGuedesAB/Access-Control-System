from src.database_setup import dataBaseDriver
import re

class interpreter ():
    
    def __init__ (self):
        self.COMMAND_LIST = ['define_new_group', 'insert_new_user', 'insert_new_facility', 'give_access', 'retrieve_info_from_name', 'check_access', 'add_user_info', 'edit_user', 'remove_access', 'remove_facility', 'remove_group', 'remove_user', 'change_group_description', ]
        print ('Interpreter')

    def parse_command (self, command):
        command_args = {}
        result = re.match('(.+) *(\(.*\))', command)
        if result is None:
            return False
        command_str = result.group(1)
        args = result.group(2)
        if re.match('\( *\)', args):
            return command_str, None
        command_str = command_str.rstrip()
        if command_str in self.COMMAND_LIST:
            args_parse = re.match('\(([^,]+)=([^,]+), *(.*)\)$', args)
            while args_parse:
                command_args.update({args_parse.group(1):args_parse.group(2)})
                last_checked_regexp = args_parse.group(3)
                args_parse = re.match('([^,]+)=([^,]+), *(.*)$', args_parse.group(3))
            last_arg = re.match('([^,]+)=([^,]+) *$', last_checked_regexp)
            if last_arg:
                command_args.update({last_arg.group(1):last_arg.group(2)})
        else:
            return None, None

        return command_str, command_args
        
    def execute (self, command):
        command, args = self.parse_command(command)
        print (command)
        print (args)

if __name__ == "__main__":
    command = input('-->')
    my_interpreter = interpreter()
    my_interpreter.execute(command)
