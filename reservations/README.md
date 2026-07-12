# Projet Réservations — Plateforme de gestion de spectacles

Projet réalisé dans le cadre du cours **PID (Projet d'Intégration de Développement)** — EPFC.

Application web permettant à une société de production de gérer son catalogue de spectacles, ses artistes, ses représentations, et à ses membres de réserver des places en ligne.

**Stack** : Django 5.2 (backend + templates) + MySQL 11.4 (dev) / SQLite (démo) + Bootstrap 5 + Django REST Framework (API JWT)

**Démo en ligne** : https://idem1030.pythonanywhere.com/show/

---

## Prérequis

| Outil | Version minimale |
|---|---|
| Python | 3.11+ |
| MySQL / MariaDB | 10.5+ (via XAMPP-Lite recommandé) |
| pip | dernière version |
| Git | — |

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/mehdichouati/Django_PID.git
cd Django_PID/reservations
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv env
source env/Scripts/activate      # Windows (Git Bash)
# source env/bin/activate        # Linux/Mac
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Démarrer MySQL (via XAMPP-Lite), puis créer la base :

```sql
CREATE DATABASE reservations;
```

Les identifiants de connexion sont définis dans `reservations/settings.py` (`root` sans mot de passe par défaut — à adapter si besoin).

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Charger des données de test (optionnel)

```bash
python seed_types.py
python seed_show.py
python seed_more_shows.py
python seed_prices.py
```

### 7. Créer un compte administrateur

```bash
python manage.py createsuperuser
```

Puis, pour lui donner le rôle **admin** (indispensable pour créer/modifier/supprimer des artistes et spectacles) :

```bash
python manage.py shell -c "
from catalogue.models import Role, RoleUser
from django.contrib.auth.models import User
admin_role, _ = Role.objects.get_or_create(role='admin')
user = User.objects.get(username='VOTRE_USERNAME')
RoleUser.objects.get_or_create(user=user, role=admin_role)
"
```

### 8. Lancer le serveur

```bash
python manage.py runserver
```

Le site est accessible sur http://127.0.0.1:8000/show/

---

## Rôles et permissions

| Rôle | Droits |
|---|---|
| **Visiteur** (non connecté) | Consultation du catalogue (spectacles, artistes, lieux culturels Open Data) |
| **Membre** | + Réservation de places, historique de ses réservations |
| **Admin** | + Création/modification/suppression des artistes et spectacles |

L'attribution du rôle **member** est automatique à l'inscription (`/register/`). Le rôle **admin** doit être attribué manuellement (voir étape 7, ou via `/admin/`).

---

## Structure du projet