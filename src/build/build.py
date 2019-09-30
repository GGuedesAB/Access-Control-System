import argparse
import os
import getpass
import logging
import re
import subprocess
import signal
import sys
from time import gmtime, strftime
import pymysql.cursors

def interrupt_handler (exception_info):
	logging.debug('Interrupt signal recieved: %s', str(exception_info))
	logging.warning('Stopping installation.')
	exit(2)

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
	logging.info('System architecture is %s', my_architecture)
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

def _install_packages (args, list_of_packages, stacked_call=False):
	if list_of_packages is not None:
		if args.debug:
			installation_cmd = ['sudo', 'apt-get', 'install', '-y']
		else:
			installation_cmd = ['sudo', 'apt-get', '-qq', 'install', '-y']
		installation_cmd.extend(list_of_packages)
		if not stacked_call:
			logging.info('Installing necessary packages: %s', _command_list_to_str(installation_cmd))
		else:
			logging.info('Retrying installation of necessary packages: %s', _command_list_to_str(installation_cmd))
		try:
			subprocess.run(installation_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
		except KeyboardInterrupt:
			interrupt_handler(sys.exc_info())
		except subprocess.CalledProcessError as installation_error:
			if not stacked_call:
				logging.warning ('Could not install packages. Updating apt.')
				_update_apt(args)
				_install_packages(args, list_of_packages, True)
			else:
				logging.error('Something went wrong when trying to install packages.')
				logging.error('Dumping apt error message\n\t%s', installation_error.stderr.decode('utf-8'))
				exit (1)
		logging.info('Package installation was successfull!')
	else:
		logging.error('Could not get list of packages.')
		exit (1)

def _update_apt (args):
	if args.debug:
		apt_update_cmd = ['sudo', 'apt-get', 'update', '-y']
	else:
		apt_update_cmd = ['sudo', 'apt-get', '-qq', 'update', '-y']
	logging.debug('Updating apt: %s', _command_list_to_str(apt_update_cmd))
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
		logging.error(process.stderr.decode('utf-8'))

def create_logger (args):
	log_format = "%(asctime)s - %(levelname)s: %(message)s"
	date_format = '%d-%m-%Y %H:%M:%S'
	if args.debug:
		logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)
	elif args.verbose:
		logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)
	else:
		logging.basicConfig(level=logging.WARNING, format=log_format, datefmt=date_format)

def setup_packages (args):
	if not _is_architecture_supported():
		logging.error('Your system system architecture is not supported.')
		exit (1)
	else:
		my_architecture = _get_system_architecture()
		list_of_packages_needed = _build_list_of_packages(my_architecture)
		_install_packages(args, list_of_packages_needed)

def make_c_files (args):
	logging.info('Making C files...')
	if args.clean:
		_call_std_subprocess(['make', '--quiet', 'clean'])
	elif not args.clean:
		_call_std_subprocess(['make', '--quiet'])
	else:
		logging.info('C files built up!')

def setup_env ():
	# Check if variable is not already set
	dirname = re.match('(.*\/Access-Control-System)', os.getcwd())
	dirname = dirname.group(1)
	local_env = 'export PYTHONPATH=' + dirname
	bashrc_env = 'echo \"export PYTHONPATH=' + dirname + '\" >> ~/.bashrc'
	try:
		subprocess.run(local_env, shell=True)
	except subprocess.CalledProcessError as err:
		logging.error('Could not setup environment.')
		print_process_error(err)
		exit(1)
	try:
		subprocess.run(bashrc_env, shell=True)
	except subprocess.CalledProcessError as err:
		logging.error('Could not setup environment.')
		print_process_error(err)
		exit(1)


def install_data_base ():
	logging.info('Setting up database as root, please enter your new password.\n')

	try:
		password = getpass.getpass()
	except KeyboardInterrupt:
		interrupt_handler(sys.exc_info())

	start_mysql = ['sudo', '/etc/init.d/mysql', 'start']
	try:
		subprocess.run(start_mysql)
	except subprocess.CalledProcessError as err:
		logging.error('Could not start MYSQL.')
		print_process_error(err)
		exit(1)

	SQL_querry = 'DROP USER \'root\'@\'localhost\'; CREATE USER \'root\'@\'localhost\' IDENTIFIED BY \'' + password + '\'; ' + 'GRANT ALL PRIVILEGES ON *.* TO \'root\'@\'localhost\' WITH GRANT OPTION; ' + 'FLUSH PRIVILEGES;'
	root_cmd = 'sudo su -c \"/bin/sh\"'
	mysql_cmd = 'mysql -u root -e \"' + SQL_querry + '\"'
	with subprocess.Popen (root_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as root:
		root.stdin.write(mysql_cmd.encode())
		root.stdin.close()
		root.wait()

	SQL_querry = '../database_setup/setup.sql'
	mysql_cmd = 'mysql -u root -p' + password + ' < ' + SQL_querry
	try:
		setup = subprocess.run(mysql_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	except subprocess.CalledProcessError as err:
		print_process_error(err)
	logging.info(setup.stdout.decode('utf-8'))

def main ():
	args = arg_parser()
	create_logger(args)
	setup_packages(args)
	make_c_files(args)
	install_data_base()
	setup_env()
	
if __name__ == '__main__':
	main()