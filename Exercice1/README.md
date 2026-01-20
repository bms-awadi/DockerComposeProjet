# Exercice 1 - Docker Compose

Application composée de deux services :
- **Backend** : API Flask (Python) sur le port 5000
- **Frontend** : Page HTML servie par Nginx sur le port 3000

## Structure du projet

```
exercice1/
├── docker-compose.yml
├── Makefile
├── *.bat (scripts Windows)
├── backend/
│   ├── Dockerfile
│   └── app.py
└── frontend/
    ├── Dockerfile
    └── index.html
```

## Lancement

### Sur Linux/Mac (avec Make)

```bash
make          # Lance l'application
make clean    # Arrête les conteneurs
make fclean   # Nettoie tout (conteneurs + images + volumes)
make re       # Relance l'application proprement
```

### Sur Windows

**Option 1 : Avec Git Bash et scripts .bat**
```bash
./all.bat      # Lance l'application
./clean.bat    # Arrête les conteneurs
./fclean.bat   # Nettoie tout
./re.bat       # Relance l'application
```

**Option 2 : Commandes directes avec docker-compose (PowerShell/CMD)**
```bash
docker-compose up --build -d    # Lancer
docker-compose down             # Arrêter
docker-compose down -v          # Nettoyer
docker system prune -af         # Nettoyer les images
```


### Makefile / Scripts .bat
Les fichiers `.bat` sont des alternatives pour Windows, offrant les mêmes fonctionnalités que le Makefile :
- `all.bat` = `make all`
- `clean.bat` = `make clean`
- `fclean.bat` = `make fclean`
- `re.bat` = `make re`

## Tester l'application

Une fois lancée, accédez à :
- **Frontend** : http://localhost:3000 (affiche "Hello World")
- **API Backend** : http://localhost:5000/api/hello (retourne `{"message": "Hello World"}`)

## Technologies utilisées

- **Docker** & **Docker Compose**
- **Backend** : Python 3.9 + Flask
- **Frontend** : Nginx Alpine + HTML/JavaScript

## Prérequis

- Docker Desktop installé et démarré
- Git (pour cloner le projet)

## Installation

```bash
# Cloner le projet
git clone <votre-repo>
cd exercice1

# Lancer
make          # Linux/Mac
./all.bat     # Windows
```

## Nettoyage

Pour supprimer tous les conteneurs, volumes et images :

```bash
make fclean   # Linux/Mac
./fclean.bat  # Windows
```
