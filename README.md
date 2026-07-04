# Projet Réservations — PID

Application de gestion de réservations de spectacles développée avec Django dans le cadre du cours PID (EPFC).

## Stack technique

- Backend : Python / Django 5.2
- Base de données : MySQL (XAMPP)
- Frontend : Bootstrap + jQuery
- API : Django REST Framework

## Installation

```bash
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Organisation du dépôt

- `reservations/` — projet Django
- `reservations/catalogue/` — app principale (spectacles, artistes, lieux, réservations)
- `docs/` — diagrammes et documentation du projet