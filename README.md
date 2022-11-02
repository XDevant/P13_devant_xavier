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


### Docker
 En plus de l'inscription au registry et de Docker Desktop, vous aurez besoin de vos logs
pour CircleCI.

Note: Docker on Windows
  - Pour utiliser docker sur votre machine, windows utilise WSL 2.
WSL 2 a besoin pour fonctionner d'un windows10 family A JOUR ou Pro, 
du module Hyper-V et d'une machine permettant la Virtualisation.
  - Si la Virtualisation n'est pas activée d'après l'onglet performances
de votre gestionnaire des tâches tentez de l'activer dans le BIOS.
  - Si windows est incapable d'activer WSL 2 docker desktop plante et vous 
serez dans l'impossibilité d'utiliser docker build, compose ou run via la CLI.
Il faudra alors la construire et la tester dans le cloud.

### Heroku:
 Rendez-vous sur Heroku.com et créez un compte.
Puis une application dont le nom soit proche de "oc-lettings", il définira votre nom de domaine.

Ensuite, dans l'onglet "ressources" de votre nouvelle app, ajoutez 2 add-ons:
 - Heroku Postgres
 - Sentry

Puis attendez les messages de confirmation :
 - @ref:postgresql-trapezoidal-36307 completed provisioning, setting DATABASE_URL.
 - @ref:sentry-dimensional-81797 completed provisioning, setting SENTRY_DSN.

A ce stade, si vous vous rendez dans l'onglet "settings" de votre app et cliquez sur 
    "reveal config vars" vous devriez voir les 2 variables.
 - Ajoutez à la liste votre VRAIE "SECRET_KEY". Celle qui sera utilisée par Heroku.

Lorsque vous utiliserez Sentry, Django aura besoin du SENTRY_DSN. Renseignez-le aussi dans 
CircleCi et le .env à la base du repo (utilisé pour créer les images docker).

### Sentry
 Maintenant que vous avez une app allez sur Sentry, créez un compte et une "app". L'app se résume
au nom de domaine donné par Heroku, Sentry devrait recevoir les erreurs de votre site qd il
sera en ligne.

### CircleCi
  Inscrivez-vous, créez un projet et reliez-le au repo GIT du projet django. Il faudra vous authentifier.
Dans "Project Settings" naviguez vers "Environment Variables". C'est là qu'il faudra ajouter
quelques variables :
 - DOCKERHUB_PASSWORD
 - DOCKERHUB_USERNAME
 - HEROKU_ID
 - HEROKU_TOKEN
 - SECRET_KEY
 - SENTRY_DNS

### 2 Requirements.txt

Il y a 2 fichiers nommés requirements.txt. 
L'un à la base du projet, dans le même dossier que ce README, est celui qui
doit être utilisé pour créer l'environnement virtuel local de développement.

 Le second, à la base de l'application, dans le repertoire de manage.py est 
utilisé pour créer l'environnement virtuel de l'image docker.

 Note : les librairies et le compilateur C nécessaires pour l'installation 
de psycopg2 sont installées de façon temporaire sur l'image docker afin 
d'en limiter la taille cf. Dockerfile.

### 2 fichiers .env

 Notre appli doit pouvoir fonctionner dans 2 environnements distincts :

  - Localement avec postgres et runserver.
  - Sur Heroku avec postgres et gunicorn.

Or Heroku va communiquer certains paramètres via des variables d'environnement.
En particulier $DATABASE_URL, $SENTRY_DNS, $PORT et $SECRET_KEY dans l'image docker 
construite pour le déploiement.

 Nous allons donc injecter ces variables dans l'environnement docker via 
le flag --env-file et le fichier .env situé à la base du projet pour tester
une image aussi proche que possible de celle qui sera déployée.

 Lors des tests locaux, nous injectons dans l'environnement local les variables
contenues dans le .env situé à la base de l'appli (à côté de manage.py) 
grâce à la librairie django-environ sans remplacer celle déjà présentes.


  - Dans l'image et le repo git, il n'y a pas de .env, ils sont exclus grâce aux fichiers 
dockerignore et gitignore.

IMPORTANT : les .env sont destinés uniquement au développement local. 
Ils ne doivent ni être copiés dans les images docker ni dans git.
Deux fichiers sample.env contenant des valeurs indicatives les remplacent
dans git.


### Migration vers Postgres avant la dockerisation
Pour transférer les données de notre db SQLite locale vers notre nouvelle 
base Postgres il faut avant tout effectuer un dumpdata vers un fichier 
db.json encodé en uft-8 sans les tables content_type et auth.Permission:

##### Dumpdata:
    - `cd oc_lettings`
    - `python -Xutf8 manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission -o db.json`

### Update Django
La version d'origine est trop ancienne et génère une importante quantité de warnings.
Apres l'ajout de la librairie "six" qui manquait, Django a été upgradé en Django==4.1.2.
Cela nécessite quelques modifications dans settings.py:

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ['https://oc-lettings-oc.herokuapp.com']

C'est dans settings que le plus gros des modifications se trouvent.

### Static files
Nous utiliserons whitenoise pour servir les fichiers statiques.