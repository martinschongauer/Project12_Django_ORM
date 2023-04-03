# Project12_Django_ORM
Projet 12: Développez une architecture back-end sécurisée en utilisant Django ORM 

Conception à l'aide de Django d'une API REST de gestion pour la société EpicEvents. Elle permet de gérer des listes d'employés, de clients, de contrats et d'événements ainsi que les relations qu'ils entretiennent les uns avec les autres. Tandis que les membres de l'équipe de vente peuvent créer les contrats, les clients, et les événements, les membres de l'équipe support disposent d'un accès limité, pour des raisons de sécurité, à la gestion des événements qui leur ont été attribués. Une équipe de gestion, dont les droits sont proches de ceux du super-utilisateur, peut accéder à tous les endpoints et, en particulier, gérer les autres équipes.

***

### Installation et lancement
Se placer dans un dossier de travail vide et récupérer le code:
```
$ git clone https://github.com/martinschongauer/Project12_Django_ORM
```

Créer et activer un environnement Python pour ce projet (sous Linux - Ubuntu):
```
$ python3 -m venv env
$ source env/bin/activate
```

Sous Windows 10 les commandes peuvent varier légèrement:
```
$ python -m venv env
$ env\Scripts\activate
```

Installer ensuite les dépendances listées dans le fichier requirements.txt:
```
$ pip install -r requirements.txt
```

Lancer le programme:
```
$ python3 manage.py runserver
```

(ou "python" selon la configuration de la machine)

### Initialisation du projet
Le projet est configuré pour utiliser une base de données PostgreSQL, dont les identifiants sont les suivants:

```
Nom de la BDD : eeventsdb
Utilisateur : postgres
Mot de passe : password
Connexion à l'hôte local au port 5432
```

Pour initialiser la base de données, entrer les commandes suivantes:

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python3 manage.py init_api
```

Le script d'initialisation init_api se situe dans api/managment/commands et il permet de créer des données par défaut pour commencer à travailler (utilisateurs, contrats...).

### Usage général
La zone d'administration est accessible à l'adresse suivante:

http://127.0.0.1:8000/admin

admin est le "superuser", et il partage le mot de passe *password* avec tous les autres utilisateurs par défaut.

Une fois l'API lancée, ses endpoints peuvent être utilisés à l'aide de Postman.
