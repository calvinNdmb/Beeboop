# 🐝 Beeboop 🐝

**🐝 Analysons les abeilles 🐝**

PolliConnect est un projet conçu pour surveiller et compter le nombre de pollinisateurs, tels que les **abeilles🐝** et les **papillons🦋**, visitant une zone spécifique. À l'aide d'une caméra, le projet capture des séquences vidéo en temps réel et utilise des algorithmes d'apprentissage automatique pour détecter et compter les pollinisateurs. 

Ces données permettent de mieux comprendre l'activité et les tendances de population des pollinisateurs, essentiels pour la santé des écosystèmes et la productivité agricole. Le projet utilise le cadre de détection d'objets **YOLO** pour une détection précise et efficace, garantissant une collecte de données fiable pour des analyses et des recherches ultérieures.

🤖 **Fonctionnalités** 🤖

- 🕵️ **Détection en Temps Réel des Pollinisateurs :** Utilise une caméra pour capturer des séquences en direct et détecter les pollinisateurs en temps réel.
- 📊 **Comptage Précis :** Emploie des modèles d'apprentissage automatique avancés pour un comptage précis des pollinisateurs.
- 🗂️ **Enregistrement des Données :** Enregistre le nombre et les horodatages pour l'analyse et les rapports.


## 🚀 Avant de lancer :

Faite git clone :
```bash
  git clone https://github.com/calvinNdmb/Beeboop.git
```

Installer le fichier requirements:

```python
  pip install -r requirements.txt
```
Sur un rasberri :

```python
pip3 install -r requirements.txt
```
Et regarder [lien utile](https://raspberrypi-guide.github.io/programming/install-opencv)

## 🧮 Pour lancer l'entrainement:

Le [Google colab](https://colab.research.google.com/drive/1hvyosE5pSRpjm5LHExdDigdmbghjksuc?usp=sharing) pour entraîner le model

❓Comment régler l'erreur de position des fichiers[Youtube](https://youtu.be/LNwODJXcvt4?si=bTVhICUVB16pZbIP&t=159)

## 🌐 Liens Utiles

📂 Création du Dataset [Documentation](https://universe.roboflow.com/mopi/beeboop)

🐝 Dataset Kaggle [Documentation](https://www.kaggle.com/datasets/jerzydziewierz/bee-vs-wasp)







## Documentation

📚[Ultralytics](https://docs.ultralytics.com/integrations/) -> Pour utiliser Yolo8 

📊[Count ultralytics](https://docs.ultralytics.com/guides/object-counting/) -> Pour compter les individus

🎥[Tuto OpenCV ](https://www.youtube.com/watch?v=jLPSnlaAnb4) -> Pour gérer les images

