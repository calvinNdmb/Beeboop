import paramiko
import os

# Paramètres de connexion au serveur
ip_address = "51.159.106.237"
username = "efrei1"
password = "efrei2019"

# Fonction pour télécharger un fichier depuis le serveur
def download_file(remote_file_path, local_file_path):
    # Connexion au serveur
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    # Télécharger le fichier
    try:
        sftp.get(remote_file_path, local_file_path)
        print(f"Le fichier {remote_file_path} a été téléchargé avec succès vers {local_file_path}.")
    except FileNotFoundError:
        print(f"Le fichier {remote_file_path} n'a pas été trouvé sur le serveur.")

    # Fermer les connexions
    sftp.close()
    ssh_client.close()

# Exemple d'utilisation
remote_file_path = "Polliconnect1/Test/2024-07-09_9-28-59.mp4"
local_file_path = "2024-07-09_9-28-59.mp4"
download_file(remote_file_path, local_file_path)
