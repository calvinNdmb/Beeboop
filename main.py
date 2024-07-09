from ultralytics import YOLO
import numpy as np
import paramiko
import os
import shutil
# Paramètres de connexion au serveur
ip_address = "51.159.106.237"
username = "efrei1"
password = "efrei2019"
model = YOLO("models/lil_big_ai.pt")
results = model("videos/4805810-hd_1280_720_30fps.mp4",save=True ,show=True, vid_stride=10, show_labels=False, conf=0.5)


def is_new_box(new_box, existing_boxes, iou_threshold=0.5):
    """
    Vérifie si la nouvelle boîte est suffisamment différente des boîtes existantes
    pour être considérée comme une nouvelle boîte.
    """
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
def create_remote_directory(sftp, remote_directory):
    dirs = remote_directory.split('/')
    for i in range(1, len(dirs) + 1):
        dir_path = '/'.join(dirs[:i])
        try:
            sftp.stat(dir_path)
        except FileNotFoundError:
            sftp.mkdir(dir_path)
def transfer_video_and_create_txt(local_video_path, txt_content):
    """
    local_video_path = "2024-07-09_9-28-59.mp4"
    txt_content = "bee = 2
    hornet = 0
    wasp = 0
    fly = 2
    butterfly = 0"
    """
    

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


unique_boxes_by_class = {}

for result in results:
    for detection in result.boxes:

        box = detection.xyxy[0].tolist()  
        cls = int(detection.cls[0])  
        
        if cls not in unique_boxes_by_class:
            unique_boxes_by_class[cls] = []
        
        if is_new_box(box, unique_boxes_by_class[cls]):
            unique_boxes_by_class[cls].append(box)

dictio = {'bee':0, 'butterfly':0, 'fly':0, 'hornet':0, 'wasp':0}
classes = {0: 'bee', 1: 'butterfly', 2: 'fly', 3: 'hornet', 4: 'wasp'}
for cls, boxes in unique_boxes_by_class.items():
    dictio = {classes[int(cls)]:len(boxes)} 
    #print(f"Nombre total de la classe {classes[int(cls)]} détectés : {len(boxes)}")


txt_output = f"bee = {dictio['bee']}\nhornet = {dictio['hornet']}\nwasp = {dictio['wasp']}\nfly = {dictio['fly']}\nbutterfly = {dictio['butterfly']}"

#transfer_video_and_create_txt("runs/detect/predict/Untitled.mp4", txt_output)
#folder_path = 'runs'
print (txt_output)
# Vérifie si le dossier existe
#if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Supprime le dossier et son contenu
    #shutil.rmtree(folder_path)
