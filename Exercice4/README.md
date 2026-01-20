# Exercice 4 - Stack PostgreSQL complète

Application web de gestion d'utilisateurs avec PostgreSQL, PgAdmin et interface web moderne.

## Description

Stack complète avec base de données PostgreSQL, interface d'administration PgAdmin, API backend Flask et frontend responsive.

## Services

- **PostgreSQL** : Base de données sur le port 5432
- **PgAdmin** : Interface d'administration sur le port 5050
- **Backend** : API Flask sur le port 5000
- **Frontend** : Interface web sur le port 3000

## Structure du projet

```
exercice4/
├── docker-compose.yml
├── Makefile
├── README.md
├── .gitignore
├── *.bat (scripts Windows)
├── pgadmin_servers.json
├── docker/
│   ├── backend.dockerfile
│   ├── frontend.dockerfile
│   ├── backend.env
│   ├── frontend.env
│   ├── pgadmin.env
│   └── postgres.env
├── backend/
│   ├── requirements.txt
│   └── src/
│       └── app.py
└── frontend/
    └── src/
        └── index.html
```

## Prérequis

- Docker Desktop installé et démarré
- Ports 3000, 5000 et 5050 disponibles

## Installation

```bash
git clone <votre-repo>
cd exercice4
```

## Lancement

### Linux/Mac

```bash
make              # Lancer l'application
make clean        # Arrêter
make purge.db     # Réinitialiser la base de données
make purge.all    # Nettoyer complètement
make re           # Relancer
```

### Windows

```bash
./all.bat         # Lancer
./clean.bat       # Arrêter
./purge_db.bat    # Réinitialiser la base
./purge_all.bat   # Nettoyer complètement
./re.bat          # Relancer
```

## Utilisation

### 1. Accéder à l'application

Après le lancement, ouvrez :

- **Frontend** : http://localhost:3000
- **PgAdmin** : http://localhost:5050
- **API Backend** : http://localhost:5000/api/health

### 2. Créer des utilisateurs

Sur http://localhost:3000 :
1. Remplissez le nom d'utilisateur et l'email
2. Cliquez sur "Créer"
3. L'utilisateur apparaît dans la liste

### 3. Modifier ou supprimer

- Cliquez sur "Modifier" pour changer les informations
- Cliquez sur "Supprimer" pour effacer un utilisateur

### 4. Accéder à PgAdmin

Sur http://localhost:5050 :
1. Connectez-vous avec :
   - Email : `admin@admin.com`
   - Mot de passe : `admin`
2. Le serveur PostgreSQL est déjà configuré
3. Mot de passe de la base : `apppassword`
4. Naviguez vers : Servers > PostgreSQL Docker > Databases > appdb > Schemas > public > Tables > users
5. Clic droit sur "users" > View/Edit Data > All Rows

## Configuration

### Fichiers .env

Tous les fichiers de configuration sont dans le dossier `docker/` :

**postgres.env**
```env
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
```

**pgadmin.env**
```env
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

**backend.env**
```env
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=apppassword
DB_HOST=postgres
DB_PORT=5432
BACKEND_PORT=5000
```

**frontend.env**
```env
FRONTEND_PORT=3000
BACKEND_URL=http://localhost:5000
```

## API Endpoints

- `GET /api/health` - Vérifier la connexion à la base
- `GET /api/users` - Liste de tous les utilisateurs
- `GET /api/users/:id` - Récupérer un utilisateur
- `POST /api/users` - Créer un utilisateur
- `PUT /api/users/:id` - Modifier un utilisateur
- `DELETE /api/users/:id` - Supprimer un utilisateur

## Persistance des données

Les données sont stockées dans des volumes Docker :
- `postgres-data` : Données PostgreSQL
- `pgadmin-data` : Configuration PgAdmin

Les données persistent même après `docker-compose down`.

### Réinitialiser la base de données

Pour supprimer toutes les données :

```bash
make purge.db     # Linux/Mac
./purge_db.bat    # Windows
```

### Nettoyer complètement

Pour supprimer tous les volumes et fichiers générés :

```bash
make purge.all    # Linux/Mac
./purge_all.bat   # Windows
```

## Technologies

- **Backend** : Python 3.9, Flask, psycopg2
- **Frontend** : HTML5, CSS3, JavaScript
- **Base de données** : PostgreSQL 15 Alpine
- **Admin** : PgAdmin 4
- **Infrastructure** : Docker, Docker Compose

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `make` / `./all.bat` | Lance l'application |
| `make clean` / `./clean.bat` | Arrête les conteneurs |
| `make purge.db` / `./purge_db.bat` | Réinitialise la base de données |
| `make purge.all` / `./purge_all.bat` | Nettoie complètement le projet |
| `make re` / `./re.bat` | Relance l'application |

## Vérification

Pour vérifier que tout fonctionne :

```bash
# Vérifier les conteneurs
docker-compose ps

# Vérifier les logs
docker-compose logs backend
docker-compose logs postgres
docker-compose logs pgadmin

# Tester l'API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/users
```

## Dépannage

### Les conteneurs ne démarrent pas

```bash
docker-compose down
docker-compose up --build
```