from ultralytics import YOLO
import numpy as np
import paramiko
import os
import shutil
import stat
import ffmpeg

# Paramètres de connexion au serveur
ip_address = "51.159.106.237"
username = "efrei1"
password = "efrei2019"
model = YOLO("models/lil_big_ai.pt")

# Fonction pour vérifier la présence d'un fichier
def verify_file(remote_directory, file_name):
    # Connexion au serveur
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    # Lister les fichiers dans le répertoire distant
    try:
        files = sftp.listdir(remote_directory)
        if file_name in files:
            print(f"Le fichier {file_name} est présent dans le répertoire {remote_directory}.")
            return True
        else:
            print(f"Le fichier {file_name} n'est pas présent dans le répertoire {remote_directory}.")
            return False
    except FileNotFoundError:
        print(f"Le répertoire {remote_directory} n'existe pas sur le serveur.")
        return False

    # Fermer les connexions
    sftp.close()
    ssh_client.close()

# Fonction pour supprimer un fichier
def delete_file(remote_file_path):
    # Connexion au serveur
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    # Supprimer le fichier
    try:
        sftp.remove(remote_file_path)
        print(f"Le fichier {remote_file_path} a été supprimé avec succès.")
    except FileNotFoundError:
        print(f"Le fichier {remote_file_path} n'existe pas sur le serveur.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier : {e}")

    # Fermer les connexions
    sftp.close()
    ssh_client.close()

def transfer_specific_video(local_video_path):
    video_name = os.path.basename(local_video_path)
    remote_video_directory = "Polliconnect1/Video"
    remote_video_path = f"{remote_video_directory}/{video_name}"

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()
    create_remote_directory(sftp, remote_video_directory)
    sftp.put(local_video_path, remote_video_path)

    video_files = sftp.listdir(remote_video_directory)
    if video_name in video_files:
        print(f"La vidéo {video_name} a été transférée avec succès.")
    else:
        print(f"La vidéo {video_name} n'a pas été transférée.")

    sftp.close()
    ssh_client.close()

def list_files_recursive(sftp, remote_directory):
    files = []
    for entry in sftp.listdir_attr(remote_directory):
        remote_path = f"{remote_directory}/{entry.filename}"
        if stat.S_ISDIR(entry.st_mode):
            files += list_files_recursive(sftp, remote_path)
        else:
            files.append(remote_path)
    return files

def list_files(remote_directory):
    # Connexion au serveur
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    # Lister les fichiers et dossiers de manière récursive
    files = list_files_recursive(sftp, remote_directory)

    # Fermer les connexions
    sftp.close()
    ssh_client.close()

    return files

def is_new_box(new_box, existing_boxes, iou_threshold=0.5):
    def compute_iou(box1, box2):
        x1, y1, x2, y2 = box1
        x3, y3, x4, y4 = box2
    
        x_left = max(x1, x3)
        y_top = max(y1, y3)
        x_right = min(x2, x4)
        y_bottom = min(y2, y4)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x4 - x3) * (y4 - y3)
        
        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou
    
    for box in existing_boxes:
        if compute_iou(new_box, box) > iou_threshold:
            return False
    return True

def transfer_video_and_create_txt(local_video_path, txt_content):
    video_name = os.path.basename(local_video_path)
    remote_video_directory = "Polliconnect1/Video"
    remote_result_directory = "Polliconnect1/result"
    remote_video_path = f"{remote_video_directory}/{video_name}"
    remote_txt_path = f"{remote_result_directory}/{os.path.splitext(video_name)[0]}.txt"

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()

    create_remote_directory(sftp, remote_video_directory)
    create_remote_directory(sftp, remote_result_directory)

    sftp.put(local_video_path, remote_video_path)

    with open("temp.txt", "w") as temp_txt:
        temp_txt.write(txt_content)
    sftp.put("temp.txt", remote_txt_path)
    os.remove("temp.txt")

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

    sftp.close()
    ssh_client.close()

def download_file(remote_file_path, local_file_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)
    print("Connexion OK", ip_address)

    sftp = ssh_client.open_sftp()
    try:
        sftp.get(remote_file_path, local_file_path)
        print(f"Le fichier {remote_file_path} a été téléchargé avec succès vers {local_file_path}.")
    except FileNotFoundError:
        print(f"Le fichier {remote_file_path} n'a pas été trouvé sur le serveur.")

    sftp.close()
    ssh_client.close()

def create_remote_directory(sftp, remote_directory):
    dirs = remote_directory.split('/')
    for i in range(1, len(dirs) + 1):
        dir_path = '/'.join(dirs[:i])
        try:
            sftp.stat(dir_path)
        except FileNotFoundError:
            sftp.mkdir(dir_path)

def convert_avi_to_mp4(input_file, output_file):
    try:
        ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)
        print(f"Conversion de {input_file} à {output_file} réussie.")
    except ffmpeg.Error as e:
        print(f"Erreur lors de la conversion de {input_file} à {output_file}: {e}")
        
# Assurez-vous que le répertoire local "videos" existe
if not os.path.exists('videos'):
    os.makedirs('videos')

remote_directory = "Polliconnect1/Test"
all_files = list_files(remote_directory)
for remote_file_path in all_files:
    local_file_path = f'videos/{os.path.basename(remote_file_path)}'
    download_file(remote_file_path, local_file_path)
    
    if os.path.exists(local_file_path):
        results = model(local_file_path, save=True, show=False, vid_stride=10, show_labels=True, conf=0.3, iou=0.45)

        unique_boxes_by_class = {}
        for result in results:
            for detection in result.boxes:
                box = detection.xyxy[0].tolist()
                cls = int(detection.cls[0])
                
                if cls not in unique_boxes_by_class:
                    unique_boxes_by_class[cls] = []
                
                if is_new_box(box, unique_boxes_by_class[cls]):
                    unique_boxes_by_class[cls].append(box)

        dictio = {'bee': 0, 'butterfly': 0, 'fly': 0, 'hornet': 0, 'wasp': 0}
        classes = {0: 'bee', 1: 'butterfly', 2: 'fly', 3: 'hornet', 4: 'wasp'}
        for cls, boxes in unique_boxes_by_class.items():
            dictio[classes[int(cls)]] = len(boxes)

        txt_output = f"bee = {dictio['bee']}\nhornet = {dictio['hornet']}\nwasp = {dictio['wasp']}\nfly = {dictio['fly']}\nbutterfly = {dictio['butterfly']}"
        input_file = f'runs/detect/predict/{os.path.splitext(os.path.basename(remote_file_path))[0]}.avi'
        output_file = f'runs/detect/predict/{os.path.splitext(os.path.basename(remote_file_path))[0]}.mp4'
        convert_avi_to_mp4(input_file, output_file)
        transfer_video_and_create_txt(f"runs/detect/predict/{os.path.splitext(os.path.basename(remote_file_path))[0]}.mp4", txt_output)
        
        #print(txt_output)

        if os.path.exists(local_file_path):
            os.remove(local_file_path)
            print(f"Le fichier {local_file_path} a été supprimé avec succès.")
        else:
            print(f"Le fichier {local_file_path} n'existe pas.")
    else:
        print(f"Le fichier {local_file_path} n'a pas été téléchargé correctement.")

    # Utiliser le nom du fichier directement pour vérification et suppression
    file_name = os.path.basename(remote_file_path)

    # Vérifier si le fichier existe
    if verify_file(remote_directory, file_name):
        # Supprimer le fichier
        delete_file(f"{remote_directory}/{file_name}")
        # Vérifier à nouveau si le fichier existe
        verify_file(remote_directory, file_name)
    folder_path = 'runs'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)





