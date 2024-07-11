import os
import cv2
#Usefule to flip images for data augmentation
def flip_images(input_folder, output_folder):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    i=0
    # Parcourir tous les fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        i+=1
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Vous pouvez ajouter d'autres extensions d'image si nécessaire
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            if image is not None:
                # Retourner l'image de 180 degrés
                flipped_image = cv2.flip(image, -1)

                # Chemin de sauvegarde pour l'image retournée
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, flipped_image)
                print(f"Image saved: {output_path}")
            else:
                print(f"Failed to read image: {image_path}")
        if i==95:
            break

input_folder = '.\input_to_rotate'
output_folder = '.\output_to_rotate'

flip_images(input_folder, output_folder)
