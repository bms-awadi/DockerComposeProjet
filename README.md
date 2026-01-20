# Projet Docker Compose - 4 Exercices

Série de 4 exercices pour apprendre Docker Compose et la containerisation d'applications web complètes.

### Exercice 1 - Backend + Frontend
Application de base avec deux services communiquant entre eux.

**Services :**
- Backend Flask (Python) - Port 5000
- Frontend Nginx (HTML) - Port 3000

**Concepts :**
- docker-compose.yml basique
- Communication entre conteneurs
- Makefile

**Fonctionnalité :**
Le frontend affiche "Hello World" récupéré depuis l'API backend.

---

### Exercice 2 - Base de données SQLite et CRUD
Ajout d'une base de données avec persistance via volumes Docker.

**Services :**
- Backend Flask avec SQLite
- Frontend avec interface CRUD
- Volume pour la persistance

**Concepts :**
- Volumes Docker
- Base de données persistante
- API REST complète (Create, Read, Update, Delete)
- Nouvelle commande Makefile : `purge`

**Fonctionnalité :**
Gestion complète d'utilisateurs (username/password) avec stockage persistant.

---

### Exercice 3 - API externe via réseau Tor
Anonymisation des requêtes HTTP via le réseau Tor.

**Services :**
- Backend Flask
- Frontend HTML/CSS/JS
- Tor (proxy SOCKS5) - Port 9050
- API externe : RandomUser.me

**Concepts :**
- Proxy réseau avec Tor
- Configuration Tor personnalisée
- Requêtes HTTP via proxy
- API externe

**Fonctionnalité :**
Récupération d'utilisateurs aléatoires depuis une API externe en passant par Tor pour l'anonymat.

---

### Exercice 4 - Stack PostgreSQL complète
Application professionnelle avec PostgreSQL et interface d'administration.

**Services :**
- Backend Flask avec psycopg2
- Frontend responsive
- PostgreSQL 15 - Port 5432
- PgAdmin 4 - Port 5050

**Concepts :**
- PostgreSQL en production
- PgAdmin pour l'administration
- Fichiers .env pour la configuration
- Structure de projet avancée
- Healthchecks
- Deux commandes purge : `purge.db` et `purge.all`

**Fonctionnalité :**
Gestion d'utilisateurs avec base PostgreSQL, interface d'admin PgAdmin et frontend moderne.

---

## Structure globale

```
ProjectDockerfile/
├── Exercice1/
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── backend/
│   └── frontend/
├── Exercice2/
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── backend/
│   └── frontend/
├── Exercice3/
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── backend/
│   ├── frontend/
│   └── tor/
└── Exercice4/
    ├── docker-compose.yml
    ├── Makefile
    ├── docker/
    ├── backend/
    └── frontend/
```

## Commandes Makefile communes

Tous les exercices partagent ces commandes de base :

| Commande | Description |
|----------|-------------|
| `make` ou `make all` | Lance l'application |
| `make clean` | Arrête les conteneurs |
| `make fclean` | Nettoie tout (conteneurs + images + volumes) |
| `make re` | Relance l'application proprement |

### Commandes spécifiques

**Exercice 2 :**
- `make purge` : Réinitialise la base de données SQLite

**Exercice 4 :**
- `make purge.db` : Réinitialise uniquement la base PostgreSQL
- `make purge.all` : Nettoie complètement le projet

## Scripts Windows (.bat)

Chaque exercice inclut des scripts batch pour Windows :
- `all.bat` : Lancer
- `clean.bat` : Arrêter
- `fclean.bat` : Nettoyer
- `re.bat` : Relancer
- `purge.bat` ou `purge_db.bat` / `purge_all.bat` : Réinitialiser

## Technologies utilisées

**Langages et frameworks :**
- Python 3.9 avec Flask
- HTML5, CSS3, JavaScript
- SQL (SQLite, PostgreSQL)

**Bases de données :**
- SQLite (Exercice 2)
- PostgreSQL 15 (Exercice 4)

**Infrastructure :**
- Docker & Docker Compose
- Nginx Alpine
- Tor (dperson/torproxy)
- PgAdmin 4

**Outils de développement :**
- Make (Linux/Mac)
- Batch scripts (Windows)
- Git

## Prérequis

- Docker Desktop installé et démarré
- Git (pour cloner les projets)
- Ports disponibles : 3000, 5000, 5050, 9050, 9051

## Installation rapide

```bash
# Cloner le projet
git clone <votre-repo>

# Exercice 1
cd Exercice1
make              # ou ./all.bat sur Windows

# Exercice 2
cd ../Exercice2
make

# Exercice 3
cd ../Exercice3
make

# Exercice 4
cd ../Exercice4
make
```