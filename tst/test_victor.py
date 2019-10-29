from src.build import build
from src.interface.interpreter import interpreter
from src.database_setup import accessControlUser as acs_module
from src.interface.executer import executer
import mock

class Test_command_list_to_str:

    def test_command_list_to_str(self):
        list_test = ("test1","test2")

        result_str = build._command_list_to_str(list_test)
        assert result_str == "test1 test2"

class Test_build_list_of_packages:

    def test_intel_build_list_of_packages(self):
        intel_test = "x86_64"

        result = build._build_list_of_packages(intel_test)
        assert result == ['mysql-client', 'mysql-server', 'automake', 'make',
                          'python3', 'python3-pip', 'gcc', 'python3-mysqldb']

    def test_arm_build_list_of_packages(self):
        arm_test = "armvl7"

        result = build._build_list_of_packages(arm_test)
        assert result == ['mariadb-client', 'mariadb-server', 'automake', 'make', 
                          'python3', 'python3-pip', 'gcc', 'python3-mysqldb']

    def test_invalid_build_list_of_packages(self):
        inv_test = "something"

        result = build._build_list_of_packages(inv_test)
        assert result == None

class Test_users_can_run:

    def test_user_can_run_as_root(self):
        command_test = "root can run command written in any way"
        user_test = acs_module.acsuser("", "", "root", "")

        i = interpreter()
        i.current_user = user_test

        result = interpreter.user_can_run(i, command_test)
        assert result == True
    
    def test_normal_user_can_run(self):
        command_test = "retrieve_description_from_group"
        user_test = acs_module.acsuser("", "", "normal_user", "")

        i = interpreter()
        i.current_user = user_test

        result = interpreter.user_can_run(i, command_test)
        assert result == True

    def test_normal_user_cannot_run(self):
        command_test = "normal user cannot run commands written anyway"
        user_test = acs_module.acsuser("", "", "normal_user", "")

        i = interpreter()
        i.current_user = user_test

        result = interpreter.user_can_run(i, command_test)
        assert result == False

class Test_print_command_table:

    def test_print_command_table_as_root(self):
        user_test = acs_module.acsuser("", "", "root", "")

        i = interpreter()
        i.current_user = user_test

        result = interpreter.print_command_table(i)
        assert result == ("add_user_info (name, username, password, MAC)\n" +
                          "change_group_description (description, number)\n" +
                          "check_access ()\n" +
                          "define_new_group (number, description)\n" +
                          "edit_user (name, username, password, group_number, MAC)\n" +
                          "give_access (group_number, facility_name)\n" +
                          "insert_new_facility (name)\n" +
                          "insert_new_user (name, MAC, username, password)\n" +
                          "remove_access (group_number, facility_name)\n" +
                          "remove_facility (name)\n" +
                          "remove_group (number)\n" +
                          "remove_user (MAC, username)\n" +
                          "retrieve_all_users ()\n" +
                          "retrieve_description_from_group (number)\n" +
                          "retrieve_info_from_username (username)\n" +
                          "retrieve_my_info ()\n")

    def test_print_command_table_as_normal_user(self):
        user_test = acs_module.acsuser("", "", "normal_user", "")

        i = interpreter()
        i.current_user = user_test

        result = interpreter.print_command_table(i)
        assert result == ("check_access ()\n" +
                          "retrieve_description_from_group (number)\n" +
                          "retrieve_my_info ()\n")

class Test_parse_command:

    def test_parse_valid_command(self):
        command_test = "define_new_group(number=1,description=test)"

        i = interpreter()

        result = interpreter.parse_command(i, command_test)
        assert result == ("define_new_group",{"number":"1", "description":"test"})
    
    def test_parse_argless_command(self):
        command_test = "check_access()"

        i = interpreter()

        result = interpreter.parse_command(i, command_test)
        assert result == ("check_access",None)

class Test_execute_from_interpreter:

    def test_execute_invalid_command(self):
        command_test = "Commands cannot be written anyway"

        i = interpreter()

        result = interpreter.execute(i,command_test)
        assert result == ("PARSER: Invalid command.")
    
    def test_execute_nonexistent_command(self):
        command_test = "unexistent_command(args_dont_matter)"

        i = interpreter()

        result = interpreter.execute(i,command_test)
        assert result == ("PARSER: Command does not exist.")

    def test_execute_command_with_wrong_arguments(self):
        command_test = "define_new_group(wrong_argument=any_value)"

        i = interpreter()

        result = interpreter.execute(i,command_test)
        assert result == ("PARSER: Wrong arguments in command.")

    @mock.patch("src.interface.executer.executer")
    def test_execute_valid_command(self, exc_mock):
        exc_inst = mock.MagicMock()
        exc_inst.execute.return_value = "Mocked output" # pretty print output
        user_test = acs_module.acsuser("", "", "root", "")
        command_test = "define_new_group(number=1,description=test)" #just a valid command for parsing to complete
        
        i = interpreter()
        i.current_user = user_test
        i.command_executer = exc_inst
            
        result = interpreter.execute(i,command_test)
        assert result == ("Mocked output")

class Test_pretty_print:

    def test_valid_pretty_print(self):
        list_of_dicts_test = ( {"1":"2","3":"4"}, {"5":"6","7":"8"} )

        result = executer.pretty_print(None, list_of_dicts_test)
        assert result == "1: 2 | 3: 4 | \n\n5: 6 | 7: 8 | \n\n"
    
    def test_invalid_pretty_print(self):
        not_a_list_of_dicts_test = "anything"

        result = executer.pretty_print(None, not_a_list_of_dicts_test)
        assert result == "Return from SQL querry is not printable."

class Test_execute_from_executer:

    def test_execute_command_with_errors(self):
        command_test = "test"
        command_table_test = {"command":"not_test"}

        result = executer.execute(None, None, command_test, None, command_table_test)
        assert result == 1
    
    def test_execute_root_command_as_normal_user(self):
        command_test = "test"
        command_table_test = {"command":("type","order")}
        user_test = acs_module.acsuser("", "", "normal_user", "")

        result = executer.execute(None, user_test, command_test, None, command_table_test)
        assert result == 1

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_root_type_command_as_root(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "retrieve_all_users"
        command_table_test = {"retrieve_all_users":("root","")} #command type = root
        user_test = acs_module.acsuser("", "", "root", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, None, command_table_test)
        assert result == "Mocked Output"

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_acsgroup_type_command_as_root(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "define_new_group"
        args_test = {"number":1,"description":"test"}
        command_table_test = {"define_new_group":("acsgroup","")} #command type = acsgroup
        user_test = acs_module.acsuser("", "", "root", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, args_test, command_table_test)
        assert result == "Mocked Output"

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_acsuser_type_command_as_root(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "insert_new_user"
        args_test = {"name":"test","username":"test","MAC":"test","password":"test","group_number":"teste"}
        command_table_test = {"insert_new_user":("acsuser","")} #command type = acsuser
        user_test = acs_module.acsuser("", "", "root", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, args_test, command_table_test)
        assert result == "Mocked Output"
    
    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_acsfacility_type_command_as_root(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "insert_new_facility"
        args_test = {"name":"test"}
        command_table_test = {"insert_new_facility":("acsfacility","")} #command type = acsfacility
        user_test = acs_module.acsuser("", "", "root", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, args_test, command_table_test)
        assert result == "Mocked Output"

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_acsaccess_type_command_as_root(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "give_access"
        args_test = {"group_number":"1", "facility_name":"test"}
        command_table_test = {"give_access":("acsaccess","")} #command type = acsaccess
        user_test = acs_module.acsuser("", "", "root", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, args_test, command_table_test)
        assert result == "Mocked Output"

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_str_type_command_as_normal_user(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "retrieve_description_from_group"
        args_test = {"number":1}
        command_table_test = {"retrieve_description_from_group":("str","")} #command type = str
        user_test = acs_module.acsuser("", "", "normal_user", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, args_test, command_table_test)
        assert result == "Mocked Output"

    @mock.patch("src.database_setup.dataBaseDriver.dataBaseDriver")      
    def test_execute_self_type_command_as_normal_user(self, dbDriver_mock):
        dbDriver_inst = mock.MagicMock()
        command_test = "retrieve_my_info"
        command_table_test = {"retrieve_my_info":("self","")} #command type = self
        user_test = acs_module.acsuser("", "", "normal_user", "")

        e = skip_init(executer)
        e.db_driver = dbDriver_inst
        e.pretty_print=mock.Mock(return_value="Mocked Output")

        result = e.execute(user_test, command_test, None, command_table_test)
        assert result == "Mocked Output"

#to make it possible to test executer.execute()
def skip_init(cls):
    actual_init = cls.__init__
    cls.__init__ = lambda *args, **kwargs: None
    instance = cls()
    cls.__init__ = actual_init
    return instance
    

    

