from flask import Flask, request, render_template
import paramiko
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_address = request.form['ipAddress']

        ssh_host = ip_address
        ssh_user = 'ubuntu'
        ssh_key_path = 'C:/Users/mahi0/Downloads/deploy.pem'  # Update this path
        repository_url = 'https://github.com/nagaladinnemahesh/scriptshell.git'  # Update with your Git repository URL
        script_path = '~/scriptshell/bash'  # Update with the path to your script on the remote server
        sudo_password = 'mahesh123'  # Replace with your sudo password

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            print("Attempting to connect to:", ssh_host)
            
            ssh.connect(ssh_host, username=ssh_user, key_filename=ssh_key_path)
            
            print(f"Successfully connected to {ssh_host}")
            
            # Clone the Git repository
            clone_command = f'git clone {repository_url}'
            stdin, stdout, stderr = ssh.exec_command(clone_command)
            print("Clone Repository Output:")
            print(stdout.read().decode())
            
            # Execute the script with sudo
            stdin, stdout, stderr = ssh.exec_command(f'sudo bash {script_path} && echo {sudo_password}')
            
            # Print the script output
            print("Script Output:")
            for line in stdout.readlines():
                print(line.strip())
            
            ssh.close()

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            print(traceback.format_exc())  # Print exception traceback

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
