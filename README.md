# Documentation - Basler Camera Script

## Description

Application web Flask pour capturer et visualiser des images depuis une caméra Basler en temps réel.

## Fonctionnalités

- Connexion automatique à la première caméra Basler détectée
- Capture d'images en continu avec intervalle configurable (3 secondes par défaut)
- Interface web pour visualiser les images capturées en temps réel
- Sauvegarde automatique des images dans le dossier `src/images/`
- Stream d'événements pour mise à jour automatique de l'interface

## Dépendances

- **pypylon** : Interaction avec les caméras Basler
- **flask** : Serveur web
- **opencv-python (cv2)** : Traitement d'images

## Structure

```
src/
├── app.py          # Application Flask principale
├── basler.html     # Interface web
├── style.css       # Styles
└── images/         # Images capturées
```

## Utilisation

```bash
python src/app.py
```

Accédez ensuite à l'interface web sur `http://localhost:5000`

## Gestion des erreurs

Le script inclut une gestion robuste des erreurs avec système de tentatives de connexion et logs détaillés.
