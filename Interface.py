import streamlit as st
import paramiko
import pandas as pd
import matplotlib.pyplot as plt

# Paramètres de connexion au serveur
ip_address = "51.159.106.237"
username = "efrei1"
password = "efrei2019"

# Connexion au serveur
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username, password=password)
sftp = ssh_client.open_sftp()

# Fonction pour lister les vidéos disponibles
def list_videos(directory):
    try:
        return [f for f in sftp.listdir(directory) if f.endswith(('.mp4', '.avi'))]
    except Exception as e:
        st.error(f"Erreur lors de la lecture du répertoire {directory}: {e}")
        return []

# Fonction pour lire le contenu d'un fichier texte et filtrer les lignes avec des valeurs non nulles
def read_filtered_txt_file(file_path):
    try:
        with sftp.file(file_path, 'r') as file:
            content = file.read().decode('utf-8')
            filtered_content = '\n'.join([line for line in content.strip().split('\n') if not line.endswith('= 0')])
            return filtered_content
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} n'existe pas.")
        return None
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier {file_path}: {e}")
        return None

# Fonction pour lire et agréger les données de tous les fichiers txt
def aggregate_data(directory, selected_month=None):
    data = {'bee': 0, 'hornet': 0, 'wasp': 0, 'fly': 0, 'butterfly': 0}
    try:
        files = [f for f in sftp.listdir(directory) if f.endswith('.txt')]
        if selected_month:
            files = [f for f in files if selected_month in f]
        for file in files:
            file_path = f"{directory}/{file}".replace("\\", "/")
            content = read_filtered_txt_file(file_path)
            if content:
                for line in content.strip().split('\n'):
                    key, value = line.split(' = ')
                    data[key.strip()] += int(value.strip())
        return data
    except Exception as e:
        st.error(f"Erreur lors de l'agrégation des données: {e}")
        return data

# Fonction pour extraire les mois disponibles à partir des noms de fichiers txt
def get_available_months(directory):
    try:
        files = [f for f in sftp.listdir(directory) if f.endswith('.txt')]
        months = sorted(set(f.split('_')[0][5:7] for f in files))  # Extraire MM
        return months
    except Exception as e:
        st.error(f"Erreur lors de la récupération des mois disponibles: {e}")
        return []

# Chemins des dossiers sur le serveur
video_directory = "Polliconnect1/Video"
result_directory = "Polliconnect1/result"

# Les onglets disponibles
tab1, tab2 = st.tabs(["Vidéos", "Statistiques"])

with tab1:
    st.title("Sélectionnez une vidéo")
    videos = list_videos(video_directory)

    # Sélection de la vidéo
    selected_video = st.selectbox("Choisissez une vidéo", videos)

    if selected_video:
        video_path = f"{video_directory}/{selected_video}".replace("\\", "/")
        txt_file_path = f"{result_directory}/{selected_video.replace('.mp4', '.txt').replace('.avi', '.txt')}".replace("\\", "/")
        st.write(f"Chemin de la vidéo: {video_path}")
        st.write(f"Chemin du fichier texte: {txt_file_path}")

        # Lire le contenu du fichier .txt correspondant à la vidéo sélectionnée
        txt_content = read_filtered_txt_file(txt_file_path)

        # Vérifier si le fichier .txt existe et afficher son contenu filtré
        if txt_content:
            st.subheader("Informations sur la vidéo")
            st.text(txt_content)
        else:
            st.subheader("Informations sur la vidéo")
            st.text("Aucune information disponible pour cette vidéo.")

        # Lire et afficher la vidéo
        st.subheader("Vidéo")
        with sftp.file(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes)

with tab2:
    st.title("Visualisation des données")

    # Agréger les données de tous les fichiers txt
    aggregated_data = aggregate_data(result_directory)
    filtered_data = {key: value for key, value in aggregated_data.items() if value > 0}

    # Créer un DataFrame à partir des données filtrées
    df = pd.DataFrame(list(filtered_data.items()), columns=['Pollinator', 'Count'])

    if not df.empty:
        # Bar chart
        st.subheader("Nombre de chaque type de pollinisateur (Toutes les données)")
        st.bar_chart(df.set_index('Pollinator'))

        # Pie chart
        st.subheader("Répartition des pollinisateurs (Toutes les données)")
        fig, ax = plt.subplots()
        ax.pie(df['Count'], labels=df['Pollinator'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("Aucune donnée disponible pour les statistiques.")

    # Récupérer les mois disponibles
    available_months = get_available_months(result_directory)
    # Sélection du mois
    selected_month = st.selectbox("Sélectionnez un mois", available_months, format_func=lambda x: f"{x}")

    if selected_month:
        # Agréger les données de tous les fichiers txt pour le mois sélectionné
        selected_month_pattern = f"-{selected_month}-"
        aggregated_data_month = aggregate_data(result_directory, selected_month_pattern)
        # Filtrer les données agrégées pour ne conserver que les catégories avec des valeurs non nulles
        filtered_data_month = {key: value for key, value in aggregated_data_month.items() if value > 0}
        # Créer un DataFrame à partir des données filtrées
        df_month = pd.DataFrame(list(filtered_data_month.items()), columns=['Pollinator', 'Count'])

        if not df_month.empty:
            st.subheader(f"Nombre de chaque type de pollinisateur (Mois {selected_month})")
            st.bar_chart(df_month.set_index('Pollinator'))

            st.subheader(f"Répartition des pollinisateurs (Mois {selected_month})")
            fig_month, ax_month = plt.subplots()
            ax_month.pie(df_month['Count'], labels=df_month['Pollinator'], autopct='%1.1f%%', startangle=90)
            ax_month.axis('equal')
            st.pyplot(fig_month)
        else:
            st.write("Aucune donnée disponible pour les statistiques pour le mois sélectionné.")

sftp.close()
ssh_client.close()
