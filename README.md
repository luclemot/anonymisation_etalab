# Anonymisation de micro-données

## Introduction

L'objectif de cet outil open source est de proposer un module d'anonymisation de donnée tabulaire, au niveau de granularité de l'individu.

La définition de l'anonymisation est à entendre au [sens de la CNIL](https://www.cnil.fr/fr/lanonymisation-de-donnees-personnelles).

Un jeu de données est considéré comme anonyme s'il respecte les trois critères suivants :
- Le critère de non-individualisation : Il est impossible d'identifier un individu parmi le jeu de données anonymisé
- Le critère de non-corrélation : Etant donné un jeu de données externe, il n'est pas possible de retrouver le même individu dans les deux jeux
- Le critère de non-inférence : Il n'est pas possible de prédire (avec une forte certitude) un nouvel attribut d'un individu présent dans le jeu

Cet outil n'a pas pour ambition d'être applicable à tout cas particulier, mais se présente comme utilisable avec n'importe quel jeu de données personnelles sous forme de tableau. Il suffit de choisir quelques paramètres, comme les variables d'intérêt du jeu, et leur nature (numérique, catégorielle, mais encore identifiante, quasi-identifiante) afin que le code produise une version anonymisée du jeu.

Ce module comporte aussi une approche adverse, qui elle cherche à quantifier la qualité de l'anonymisation réalisée. Il est question de trouver l'équilibre optimal entre la qualité de l'anonymisation (la protection des informations personnelles) et la qualité de l'information conservée (la conservation des propriétés statistiques notamment.)

## Installation

Ce module n'est actuellement pas déployé en ligne. Pour l'utiliser en local, il suffit de créer un environnement virtuel à partir du fichier `environment.yml`.

## Structure de données

Le module est adapté à un jeu de données avec une extension *.csv*.

## Structure du module

Ce repo est constitué d'un dossier [utils](utils/) dans lequel se trouvent les fonctions et objets nécessaires pour l'anonymisation et le contrôle de qualité, et du dossier [data](data/) dans lequel la donnée est stockée après anonymisation en préparation aux modules adverses.
- Le notebook principal est [anonymisation.ipynb](anonymisation.ipynb), dans lequel l'anonymisation s'opère.
- Le notebook de l'approche adverse est [adversary.ipynb](adversary.ipynb), dans lequel l'approche adverse implémentée par nos soins est réalisée. Il étudie la qualité de l'anonymisation selon les trois criètres de la CNIL.
- Le notebook secondaire est [anonymeter.ipynb](anonymeter.ipynb), dans lequel l'outil `Anonymeter` estime et quantifie la performance d'une attaque adverse, et donc évalue la qualité de l'anonymisation.

### Dossier utils

Le dossier utils comprend un ensemble de fichiers qui contiennent toutes les fonctions nécessaires au bon fonctionnement du module. On y retrouve notamment :
- Le fichier [exploration.py](utils/exploration.py), qui contient les fonctions d'exploration et de nettoyage de dataset.
- Le fichier [correlation.py](utils/correlation.py), qui contient les fonctions déterminant les relations de corrélation entre les variables.
- Le fichier [perturbation.py](utils/perturbation.py), qui contient les fonctions de perturbation pour les variables numériques.
- Le fichier [outliers.py](utils/outliers.py), qui contient les fonctions d'identification des outliers.
- Le fichier [inference.py](utils/inference.py), qui contient la structure d'objet nécessaire pour étudier le critère de non-inférence.
- Le fichier [stats.py](utils/stats.py), qui contient les fonctions quantifiant l'évolution de la qualité statistique du jeu de données avant et après anonymisation.

Par ailleurs,
- Le fichier [tools.py](utils/tools.py) contient des fonctions basiques.
- Le fichier [ano_correc.py](utils/ano_correc.py) devra être supprimé ASAP. En effet, il s'agit la d'une correction en local du repository d'anonymisation [anonymity](https://github.com/SGMAP-AGD/anonymisation). La pull request n'a pas encore été faite pour corriger les fonctions obsolètes.

## Méthodologie

- Anonymisation :
Le module commence par une étape de nettoyage et d'exploration de données.
Ensuite, il applique les méthodes d'anonymisation suivantes: une agrégation locale avec k=0.1% de la taille du jeu pour les variables catégorielles, et un bruit additif pour les variables numériques.
Enfin, il tente d'identifier les outliers et les écarte le cas échéant.
- Module adverse :
Le module débute par une analyse de qualité du critère de non-individualisation, puis de non-inférence. Ensuite, il quantifie la distance entre le jeu de données initial et celui anonymisé.
Enfin, il estime des métriques clés d'anonymisation pour le jeu initial et anonymisé pour comparaison.

## Performance

Le code est très coûteux d'un point de vue temporel. Comme la plupart des outils d'anonymisation existants, il peut prendre plusieurs heures à tourner sur un très grand jeu de données.
Cependant, le module adverse témoigne d'une forte diminution de risque de ré-identification ou d'inférence après anonymisation.

## Voies d'amélioration

Les méthodes d'anonymisation utilisées dans ce module sont assez simples. Il pourrait être très pertinent d'ajouter des méthodes plus complexes, pour les variables catégorielles comme numériques.

## Le tester

Le fichier des équidés, disponible [ici](https://www.data.gouv.fr/fr/datasets/fichier-des-equides/) permet de tester le module.
