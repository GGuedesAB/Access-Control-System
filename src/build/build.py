import argparse
import os
import getpass
import re
import subprocess
import signal
import sys
import uuid
from time import gmtime, strftime
try:
    from src.tools import logger
    from src.database_setup import dataBaseDriver
    from src.database_setup import accessControlUser
except ModuleNotFoundError:
    print ('\nERROR: Run env_set.py before building system.\n')
    exit (1)

# Add to build the creation of first user as admin

def interrupt_handler (exception_info):
    build_logger.debug('Interrupt signal recieved: ' + str(exception_info))
    build_logger.warning('Stopping installation.')
    exit(2)

def create_logger ():
    build_logger = logger.acsLogger()
    if args.debug:
        build_logger.set_debug()
    elif args.verbose:
        build_logger.set_info()
    else:
        build_logger.set_warning()

    return build_logger

def arg_parser():
    parser = argparse.ArgumentParser(description='Installation script for ACS.')
    parser.add_argument('--clean', help='makes a clean installation', action='store_true')
    debbugger = parser.add_mutually_exclusive_group()
    debbugger.add_argument('--debug', help='activates ULTRA verbose mode', action='store_true')
    debbugger.add_argument('--verbose', '-v', help='activates verbose mode', action='store_true')
    args = parser.parse_args()
    return args

def _get_system_architecture ():
    get_architecture_cmd = ['uname', '-m']
    get_architecture_process = subprocess.run(get_architecture_cmd, stdout=subprocess.PIPE, check=True)
    system_architecture = get_architecture_process.stdout.decode('utf-8').rstrip()
    return system_architecture

def _is_architecture_supported ():
    SUPPORTED_ARCHITECTURES = ['x86_64', 'armvl7']
    my_architecture = _get_system_architecture()
    build_logger.info('System architecture is ' + my_architecture)
    if my_architecture in SUPPORTED_ARCHITECTURES:
        return True
    else:
        return False

def _build_list_of_packages (system_architecture):
    if system_architecture == 'x86_64':
        LIST_OF_PACKAGES = ['mysql-client', 'mysql-server', 'automake', 'make',
                            'python3', 'python3-pip', 'gcc', 'python3-mysqldb']
        return LIST_OF_PACKAGES
    elif system_architecture == 'armvl7':
        LIST_OF_PACKAGES = ['mariadb-client', 'mariadb-server', 'automake', 'make', 
                            'python3', 'python3-pip', 'gcc', 'python3-mysqldb']
        return LIST_OF_PACKAGES
    else:
        return None

def _command_list_to_str(listed_commands):
    separator = ' '
    result = separator.join(listed_commands)
    return result

def _install_packages (list_of_packages, stacked_call=False):
    if list_of_packages is not None:
        if args.debug:
            installation_cmd = ['sudo', 'apt-get', 'install', '-y']
        else:
            installation_cmd = ['sudo', 'apt-get', '-qq', 'install', '-y']
        installation_cmd.extend(list_of_packages)
        if not stacked_call:
            build_logger.info('Installing necessary packages: ' + _command_list_to_str(installation_cmd))
        else:
            build_logger.info('Retrying installation of necessary packages: ' + _command_list_to_str(installation_cmd))
        try:
            subprocess.run(installation_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except KeyboardInterrupt:
            interrupt_handler(sys.exc_info())
        except subprocess.CalledProcessError as installation_error:
            if not stacked_call:
                build_logger.warning ('Could not install packages. Updating apt.')
                _update_apt()
                _install_packages(list_of_packages, True)
            else:
                build_logger.error('Something went wrong when trying to install packages.')
                build_logger.error('Dumping apt error message\n\t ' + installation_error.stderr.decode('utf-8'))
                exit (1)
        build_logger.info('Package installation was successfull!')
    else:
        build_logger.error('Could not get list of packages.')
        exit (1)

def _update_apt ():
    if args.debug:
        apt_update_cmd = ['sudo', 'apt-get', 'update', '-y']
    else:
        apt_update_cmd = ['sudo', 'apt-get', '-qq', 'update', '-y']
    build_logger.debug('Updating apt: ' + _command_list_to_str(apt_update_cmd))
    try:
        subprocess.run(apt_update_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except KeyboardInterrupt:
        interrupt_handler(sys.exc_info())
    except subprocess.CalledProcessError as apt_update_error:
        print_process_error(apt_update_error)

def _call_std_subprocess (command):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as err:
        print_process_error(err)

def print_process_error (process):
        build_logger.error(process.stderr.decode('utf-8'))

def setup_packages ():
    if not _is_architecture_supported():
        build_logger.error('Your system system architecture is not supported.')
        exit (1)
    else:
        my_architecture = _get_system_architecture()
        list_of_packages_needed = _build_list_of_packages(my_architecture)
        _install_packages(list_of_packages_needed)

def make_c_files ():
    build_logger.info('Making C files...')
    my_env = os.environ.get('PYTHONPATH')
    build_folder = os.path.join(my_env, 'src', 'build')
    os.chdir(build_folder)
    if args.clean:
        _call_std_subprocess(['make', '--quiet', 'clean'])
    elif not args.clean:
        _call_std_subprocess(['make', '--quiet'])
    else:
        build_logger.info('C files built up!')

def install_data_base ():
    print('Setting up database for root.')
    try:
        root_name = input ('Your name: ')
        password = getpass.getpass('New password: ')
    except KeyboardInterrupt:
        build_logger.warning('Exiting script')
        interrupt_handler(sys.exc_info())

    try:
        start_mysql = ['sudo', '/etc/init.d/mysql', 'start']
        subprocess.run(start_mysql)
    except subprocess.CalledProcessError as err:
        build_logger.error('Could not start MYSQL.')
        print_process_error(err)
        exit(1)

    try:
        check_user_config = ['mysql', '-N', '-B', '-u', 'root', '-p' + password, '-e', '\"SELECT EXISTS(SELECT * FROM mysql.user WHERE user = \'root\');\"']
        subprocess.run(' '.join(check_user_config), stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, shell=True)
    except subprocess.CalledProcessError:
        user_is_already_configured = False
    else:
        user_is_already_configured = True

    if not user_is_already_configured:
        SQL_querry = 'DROP USER \'root\'@\'localhost\'; CREATE USER \'root\'@\'localhost\' IDENTIFIED BY \'' + password + '\'; ' + 'GRANT ALL PRIVILEGES ON *.* TO \'root\'@\'localhost\' WITH GRANT OPTION; ' + 'FLUSH PRIVILEGES;'
        root_cmd = 'sudo su -c \"/bin/sh\"'
        mysql_cmd = 'mysql -u root -e \"' + SQL_querry + '\"'
        with subprocess.Popen (root_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as root:
            root.stdin.write(mysql_cmd.encode())
            root.stdin.close()
            root.wait()

    my_env = os.environ.get('PYTHONPATH')
    SQL_querry = os.path.join(my_env, 'src', 'database_setup', 'setup.sql')
    mysql_cmd = 'mysql -u root -p' + password + ' < ' + SQL_querry
    try:
        setup = subprocess.run(mysql_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as err:
        print_process_error(err)
    build_logger.info(setup.stdout.decode('utf-8'))

    data_base_connect = dataBaseDriver.dataBaseDriver('localhost', 'root', password, 'accontrol')
    root_MAC = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    root_user = accessControlUser.acsuser(str(root_name), root_MAC, 'root', str(password))
    data_base_connect.insert_new_user(root_user)

args = arg_parser()
build_logger = create_logger()

def main ():
    setup_packages()
    make_c_files()
    install_data_base()

if __name__ == "__main__":
    main()