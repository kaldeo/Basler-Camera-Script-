# Documentation - Basler Camera Script

## Description

Ce script Python permet de détecter et de lister les caméras Basler connectées à votre système.

## Fonctionnalités

### `info.py`
Script de détection des caméras Basler qui :
- Énumère toutes les caméras Basler connectées au système
- Affiche le nombre total de caméras détectées
- Pour chaque caméra trouvée, affiche :
  - Le numéro de la caméra
  - Le modèle de la caméra
  - Le numéro de série

## Dépendances

- **pypylon** : Bibliothèque Python pour l'interaction avec les caméras Basler

## Utilisation

```bash
python src/info.py
```

## Exemples de sortie

### Aucune caméra détectée
```
Aucune caméra Basler détectée
```

### Une ou plusieurs caméras détectées
```
2 caméra(s) Basler détectée(s)
   Caméra 1: acA1300-60gm - S/N: 12345678
   Caméra 2: acA2040-90um - S/N: 87654321
```

### En cas d'erreur
```
Erreur : [message d'erreur]
```

## Gestion des erreurs

Le script inclut une gestion d'erreurs qui capture et affiche toute exception qui pourrait survenir lors de la détection des caméras.
