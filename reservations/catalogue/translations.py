"""
Dictionnaire de traductions simple, sans dépendance externe (pas de gettext).
Utilisé pour différencier le contenu affiché selon la langue du profil utilisateur (UserMeta.langue).
"""

TRANSLATIONS = {
    'FR': {
        'nav_spectacles': 'Spectacles',
        'nav_artistes': 'Artistes',
        'nav_lieux_culturels': 'Lieux culturels (Open Data)',
        'nav_mes_reservations': 'Mes réservations',
        'nav_bonjour': 'Bonjour',
        'nav_se_connecter': 'Se connecter',
        'nav_sinscrire': "S'inscrire",
        'nav_se_deconnecter': 'Se déconnecter',
    },
    'EN': {
        'nav_spectacles': 'Shows',
        'nav_artistes': 'Artists',
        'nav_lieux_culturels': 'Cultural venues (Open Data)',
        'nav_mes_reservations': 'My bookings',
        'nav_bonjour': 'Hello',
        'nav_se_connecter': 'Log in',
        'nav_sinscrire': 'Sign up',
        'nav_se_deconnecter': 'Log out',
    },
    'NL': {
        'nav_spectacles': 'Voorstellingen',
        'nav_artistes': 'Artiesten',
        'nav_lieux_culturels': 'Culturele plekken (Open Data)',
        'nav_mes_reservations': 'Mijn reserveringen',
        'nav_bonjour': 'Hallo',
        'nav_se_connecter': 'Inloggen',
        'nav_sinscrire': 'Registreren',
        'nav_se_deconnecter': 'Uitloggen',
    },
}