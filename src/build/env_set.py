import re
import subprocess
import os

def setup_env ():
    # Check if variable is not already set
    dirname = re.match('(.*\/Access-Control-System)', os.getcwd())
    dirname = dirname.group(1)
    check_PYTHONPATH = "echo $PYTHONPATH"
    is_bash = 'echo $SHELL'
    restart_bash = '/bin/bash'
    bashrc_env = 'echo \"export PYTHONPATH=' + dirname + '\" >> ~/.bashrc'

    try:
        is_bash = subprocess.run(is_bash, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print ('ERROR: ' + err.stderr.decode('utf-8'))
        exit(1)
    if is_bash.stdout.decode('utf-8') != '/bin/bash\n':
        print ('ERROR: Please use bash as shell interpreter!')
        exit (1)

    try:
        env_var_check = subprocess.run(check_PYTHONPATH, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print ('ERROR: ' + err.stderr.decode('utf-8'))
        exit(1)
    else:
        is_set_PYTHONPATH = env_var_check.stdout.decode('utf-8')
        if is_set_PYTHONPATH == "\n":
            try:
                subprocess.run(bashrc_env, shell=True, check=True)
            except subprocess.CalledProcessError as err:
                print ('ERROR: ' + err.stderr.decode('utf-8'))
                exit(1)
            try:
                subprocess.run(restart_bash, shell=True, check=True)
            except subprocess.CalledProcessError as err:
                print ('ERROR: ' + err.stderr.decode('utf-8'))
                exit(1)

def install_python_dependencies():
    apt_call = ['sudo', 'apt-get', '-qq', 'install', 'python3-pip']
    pip_call = ['sudo', '-H', 'pip3', 'install', 'pymysql']
    try:
        subprocess.run(apt_call, check=True)
        subprocess.run(pip_call, check=True)
    except subprocess.CalledProcessError:
        print('ERROR: Could not install python dependencies.')
        exit(1)                

if __name__ == "__main__":
    setup_env()
    install_python_dependencies()
    print ('\nEnvironment variables are set!\n')