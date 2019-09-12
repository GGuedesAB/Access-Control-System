import argparse
import os
import getpass
import logging
import subprocess
from time import gmtime, strftime

def arg_parser():
	parser = argparse.ArgumentParser(description='Installation script for ACS.')
	parser.add_argument('--clean', help='makes a clean installation', action='store_true')
	debbugger = parser.add_mutually_exclusive_group()
	debbugger.add_argument('--debug', help='activates ULTRA verbose mode', action='store_true')
	debbugger.add_argument('--verbose', '-v', help='activates verbose mode', action='store_true')
	args = parser.parse_args()
	return args

def _get_system_architecture (args):
	get_architecture_cmd = ['uname', '-m']
	get_architecture_process = subprocess.run(get_architecture_cmd, stdout=subprocess.PIPE)
	system_architecture = get_architecture_process.stdout.decode('utf-8').rstrip()
	return system_architecture

def _is_architecture_supported (args):
	SUPPORTED_ARCHITECTURES = ['x86_64', 'armvl7']
	my_architecture = _get_system_architecture(args)
	if args.debug:
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
		logging.info('Installing necessary packages: %s', _command_list_to_str(installation_cmd))
		installation_cmd_result = subprocess.run(installation_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if installation_cmd_result.returncode != 0:
			if not stacked_call:
				logging.warning ('Could not install packages.\nUpdating apt.')
				update_result = _update_apt(args)
				if update_result.returncode == 0:
					_install_packages(args, list_of_packages, True)
				else:
					logging.error('Something went wrong when trying to update apt.')
					exit (1)
			else:
				logging.error('Something went wrong when trying to install packages.')
				error_message = installation_cmd_result.stderr
				error_message = error_message.decode('utf-8')
				logging.error(error_message)
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
	apt_update_result = subprocess.run(apt_update_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return apt_update_result

def _check_process_completion (process):
	if type(process) is subprocess.CompletedProcess:
		if process.returncode != 0:
			logging.error('Process failed.')
			error_message = process.stderr
			error_message = error_message.decode('utf-8')
			logging.error(error_message)
	else:
		logging.debug('Function returned %s, not a subprocess.', str(process))

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
	if not _is_architecture_supported(args):
		logging.error('Your system system architecture is not supported.')
		exit (1)
	else:
		my_architecture = _get_system_architecture(args)
		list_of_packages_needed = _build_list_of_packages(my_architecture)
		_install_packages(args, list_of_packages_needed)

def make_c_files (args):
	logging.info('Making C files...')
	if (args.clean):
		make = subprocess.run(['make', '--quiet', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	make = subprocess.run(['make', '--quiet'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# Use {try except} here intead
	_check_process_completion(make)
	logging.info('C files built up!')


def setup_data_base ():
	# Call data base driver instance here
	print ('DB')


def main ():
	args = arg_parser()
	create_logger(args)
	setup_packages(args)
	make_c_files(args)
	
if __name__ == '__main__':
	main()