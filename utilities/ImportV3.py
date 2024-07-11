import paramiko
import os

# Paramètres de connexion au serveur
ip_address = "51.159.106.237"
username = "efrei1"
password = "efrei2019"


# Fonction pour créer les répertoires nécessaires sur le serveur
def create_remote_directory(sftp, remote_directory):
    dirs = remote_directory.split('/')
    for i in range(1, len(dirs) + 1):
        dir_path = '/'.join(dirs[:i])
        try:
            sftp.stat(dir_path)
        except FileNotFoundError:
            sftp.mkdir(dir_path)


# Fonction pour transférer une vidéo et créer un fichier texte correspondant
def transfer_video_and_create_txt(local_video_path, txt_content):
    # Extraire le nom de la vidéo
    video_name = os.path.basename(local_video_path)

    # Définir les chemins des répertoires distants
    remote_video_directory = "Polliconnect1/Video"
    remote_result_directory = "Polliconnect1/result"

    # Chemins complets des fichiers distants
    remote_video_path = f"{remote_video_directory}/{video_name}"
    remote_txt_path = f"{remote_result_directory}/{os.path.splitext(video_name)[0]}.txt"

    # Connexion au serveur
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    # Créer les répertoires nécessaires sur le serveur
    create_remote_directory(sftp, remote_video_directory)
    create_remote_directory(sftp, remote_result_directory)

    # Transférer la vidéo
    sftp.put(local_video_path, remote_video_path)

    # Créer et transférer le fichier texte
    with open("temp.txt", "w") as temp_txt:
        temp_txt.write(txt_content)
    sftp.put("temp.txt", remote_txt_path)
    os.remove("temp.txt")

    # Vérifier si les fichiers ont été transférés avec succès
    video_files = sftp.listdir(remote_video_directory)
    if video_name in video_files:
        print(f"La vidéo {video_name} a été transférée avec succès.")
    else:
        print(f"La vidéo {video_name} n'a pas été transférée.")

    txt_files = sftp.listdir(remote_result_directory)
    if os.path.basename(remote_txt_path) in txt_files:
        print(f"Le fichier texte {os.path.basename(remote_txt_path)} a été créé avec succès.")
    else:
        print(f"Le fichier texte {os.path.basename(remote_txt_path)} n'a pas été créé.")

    # Fermer les connexions
    sftp.close()
    ssh_client.close()


# Exemple d'utilisation
local_video_path = "2024-07-09_9-28-59.mp4"
txt_content = """bee = 2
hornet = 0
wasp = 0
fly = 2
butterfly = 0
"""
transfer_video_and_create_txt(local_video_path, txt_content)
