## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure
- Docker Desktop, un compte Docker-Hub, docker CLI.
- Compte Heroku et CLI, sentry et postgres add ons.
- Compte Sentry et sdk CLI

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

Note: Docker on Windows
  - Pour utiliser docker sur votre machine, windows utilise WSL 2.
WSL 2 a besoin pour fonctionner d'un windows10 family A JOUR ou Pro, 
du module Hyper-V et d'une machine permettant la Virtualisation.
  - Si la Virtualisation n'est pas activée d'après l'onglet performances
de votre gestionnaire des tâches tentez de l'activer dans le BIOS.
  - Si windows est incapable d'activer WSL 2 docker desktop plante et vous 
serez dans l'impossibilité d'utiliser docker build, compose ou run via la CLI.
Il faudra alors la construire et la tester dans le cloud.


### 2 Requirements.txt

Il y a 2 fichiers nommés requirements.txt. 
L'un à la base du projet, dans le même dossier que ce README, est celui qui
doit être utilisé pour créer l'environnement virtuel local de développement.

 Le second, à la base de l'application, dans le repertoire de manage.py est 
utilisé pour créer l'environnement virtuel de l'image docker.

 La principale différence entre les 2 est que dans l'image docker, nous 
utiliserons Gunicorn pour servir l'app et non runserver, ansi que psycopg2
pour la base de donnée postgres.

 Note : les librairies et le compilateur C nécessaires pour l'installation 
de psycopg2 sont installées de façon temporaire sur l'image docker afin 
d'en limiter la taille cf. Dockerfile.

 De plus flake8 et quelques outils de tests comme selenium ne sont pas utiles
dans l'image.
 
### 2 fichiers .env

 Notre appli doit pouvoir fonctionner dans 3 environnements distincts :
 
  - Localement, sans docker avec sqlite3 et en utilisant runserver.
  - Localement dans l'image docker avec postgres et runserver.
  - Sur Heroku avec postgres et gunicorn.

Or Heroku va communiquer certains paramètres via des variables d'environnement.
En particulier $DATABASE_URL, $SENTRY_DNS et $PORT.

Et CircleCi injectera une $SECRET_KEY dans l'image docker construite pour 
le déployement.

 Nous allons donc injecter ces variables dans l'environnement docker via 
le flag --env-file et le fichier .env situé à la base du projet pour tester
une image aussi proche que possible de celle qui sera déployée.

 Lors des tests locaux, nous injectons dans l'environnement local les variables
contenues dans le .env situé à la base de l'appli (à côté de manage.py) 
grâce à la librairie django-environ sans remplacer celle déjà présentes.

 Le fichier settings.py de Django est donc configuré de la manière suivante :

  - Si Heroku est détecté les variables sont lues via os.environ.get et
donc seules les celle injectées par CircleCi (SECRET_KEY, logs heroku) et 
Heroku seront considérées. Django va donc se réveiller avec une db 
postgres vide et sans ses migrations.

Sinon, les variables seront lues par django-environ.

  - Dans l'image, il n'y a pas de .env, ils sont exclus grâce au fichier 
dockerignore, comme les migrations.
 Donc django-environ renverra exactement les mêmes valeurs que
os.environ.get. Django va se réveiller avec une db postgres vide et sans
ses migrations.
  - Localement, les variables d'environnement seront complétées par celles du 
.env et donc chercher son fichier sqlite3 et conserver son historique de 
migrations.

IMPORTANT: les .env sont destinés uniquement au développement local. 
Ils ne doivent ni être copiés dans les images docker ni dans git.
Deux fichiers sample.env contenant des valeurs indicatives les remplacent
dans git.


### Migration vers Postgres pendant la dockerisation
Avant :
Pour transférer les données de notre db SQLite locale vers notre nouvelle 
base Postgres il faut avant tout effectuer un dumpdata vers un fichier 
db.json encodé en uft-8 sans la table content_type.

De plus, comme nous allons forcer Django à changer de backend, il est impératif 
que ni SQLite3 ni les migrations ne soient copiés dans l'image docker.

Dockerfile :
Nous allons partir de l'image docker contenant un petit linux et python 3.10
Pour notre bd Postgres nous avons besoin du client et de psycopg2.

Nous installons les librairies C qui sont nécessaires à l'installation de 
psycopg2 mais pas à notre appli dans un répertoire temporaire par la suite effacé.
Il s'agit de postgresql-dev, musl-dev et linux-headers.

Pour finir il nous faut dans oc_lettings_site/management/commands une
commande maison qui sera lancée lors du démarrage de nos conteneurs.

Cette commande va enchainer Makemigration, Migrate, Loaddata et 
Runserver ou Gunicorn selon l'argument passé.
Usage : startserver or starserver windows