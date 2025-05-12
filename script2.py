import paramiko

def create_ssh_client(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port, username=username, password=password)
    return client

def restart_service(ssh_client, service_name):
    print(f"[INFO] Redemarrage du service : {service_name}")
    stdin, stdout, stderr = ssh_client.exec_command(f"sudo systemctl restart {service_name}")
    err = stderr.read().decode('utf-8', errors='ignore')
    print(err.encode('ascii', errors='ignore').decode())

def check_service_status(ssh_client, service_name):
    print(f"[INFO] Etat du service : {service_name}")
    stdin, stdout, stderr = ssh_client.exec_command(f"systemctl status {service_name}")
    out = stdout.read().decode('utf-8', errors='ignore')
    print(out.encode('ascii', errors='ignore').decode())

def list_running_services(ssh_client):
    print("\n[INFO] Services actifs :")
    stdin, stdout, stderr = ssh_client.exec_command("systemctl list-units --type=service --state=running")
    out = stdout.read().decode('utf-8', errors='ignore')
    print(out.encode('ascii', errors='ignore').decode())

def check_resources(client):
    print("\n[INFO] Surveillance des ressources système :")

    # CPU
    stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)'")
    cpu_usage = stdout.read().decode('utf-8', errors='ignore')
    print(f"Usage du CPU :\n{cpu_usage.strip()}")

    # Mémoire
    stdin, stdout, stderr = client.exec_command("free -m")
    memory_usage = stdout.read().decode('utf-8', errors='ignore')
    print(f"\nUsage de la mémoire :\n{memory_usage.strip()}")

    # Disque
    stdin, stdout, stderr = client.exec_command("df -h")
    disk_usage = stdout.read().decode('utf-8', errors='ignore')
    print(f"\nUsage du disque :\n{disk_usage.strip()}")

def main():
    host = input("Adresse IP ou nom d'hote : ")
    port = 22
    user = input("Nom d'utilisateur SSH : ")
    password = input("Mot de passe SSH : ")

    try:
        ssh = create_ssh_client(host, port, user, password)
        print("Connexion SSH etablie avec succes.\n")

        while True:
            print("\n=== MENU ===")
            print("1. Redemarrer un service")
            print("2. Verifier l'etat d'un service")
            print("3. Lister les services actifs")
            print("4. Surveiller les ressources système")
            print("5. Quitter")
            choix = input("Choisissez une option : ")

            if choix == '1':
                service = input("Nom du service a redemarrer : ")
                restart_service(ssh, service)
            elif choix == '2':
                service = input("Nom du service a verifier : ")
                check_service_status(ssh, service)
            elif choix == '3':
                list_running_services(ssh)
            elif choix == '4':
                check_resources(ssh)
            elif choix == '5':
                print("Deconnexion SSH.")
                ssh.close()
                break
            else:
                print("Option invalide. Veuillez reessayer.")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()
