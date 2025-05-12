import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.100', username='user', password='motdepasse')

stdin, stdout, stderr = ssh.exec_command('systemctl status ssh')

print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()

