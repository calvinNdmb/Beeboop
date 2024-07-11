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

❗Attention❗
Installez ffmpeg avant de lancer le programme comme dans [cette video](https://youtu.be/5xgegeBL0kw?si=9IGn_WC2v2J2d5Eq)

Sur un linux :

```python
pip3 install -r requirements.txt
```
Et regarder [lien utile](https://raspberrypi-guide.github.io/programming/install-opencv) si besoin



## 🧮 Pour lancer l'entrainement:

Le [Google colab](https://colab.research.google.com/drive/1hvyosE5pSRpjm5LHExdDigdmbghjksuc?usp=sharing) pour entraîner le model


## 💡Petit tips :

- Le meilleur model est "Medium.pt" il est basé sur l'architecture [yoloV8m](https://docs.ultralytics.com/models/yolov8/) (m pour medium) --> temps d'entrainement 2H
- Le second meilleur est "nano.pt" il est basé sur l'architecture [yoloV8n](https://docs.ultralytics.com/models/yolov8/) (n pour nano) --> temps d'entrainement :1H
- Les utilities sont là pour vous aider à mieux comprendre le code en montrant des cas d'usage de certaines fonctions de notre projet.
- Comment régler l'erreur de position des fichiers[Youtube](https://youtu.be/LNwODJXcvt4?si=bTVhICUVB16pZbIP&t=159) lors de l'entrainement?


## 🌐 Liens Utiles:

- 📂 Link to the dataset [Documentation](https://universe.roboflow.com/mopi/beeboop)
- Kaggle de l'un des [datasets](https://www.kaggle.com/datasets/jerzydziewierz/bee-vs-wasp) utilisé pour les abeilles
- Roboflow universe, pour retrouver les autres [datasets](https://universe.roboflow.com/) utilisés.

## Documentation

📚[Ultralytics](https://docs.ultralytics.com/integrations/) -> Pour utiliser Yolo8 

📊[Count ultralytics](https://docs.ultralytics.com/guides/object-counting/) -> Pour compter les individus

🎥[Tuto OpenCV ](https://www.youtube.com/watch?v=jLPSnlaAnb4) -> Pour gérer les images

