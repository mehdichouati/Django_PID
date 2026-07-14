from .translations import TRANSLATIONS


def user_language(request):
    """
    Injecte automatiquement le dictionnaire de traduction correspondant à la
    langue du profil de l'utilisateur connecté (UserMeta.langue), disponible
    dans tous les templates via la variable `t`. Par défaut : français.
    """
    lang = 'FR'
    if request.user.is_authenticated and hasattr(request.user, 'meta'):
        lang = request.user.meta.langue or 'FR'

    return {
        't': TRANSLATIONS.get(lang, TRANSLATIONS['FR']),
        'current_lang': lang,
    }