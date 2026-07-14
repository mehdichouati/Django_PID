from rest_framework.permissions import BasePermission, SAFE_METHODS


class AffiliateLevelPermission(BasePermission):
    """
    Restreint l'accès à l'API selon le niveau d'affiliation du membre (UserMeta.affiliate_level) :
    - free    : lecture seule
    - starter : lecture seule (accès complet aux champs)
    - premium : lecture + écriture (création/modification)
    """
    message = "Votre niveau d'affiliation ne permet pas cette action. Passez à Premium pour créer/modifier des ressources."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        level = getattr(getattr(request.user, 'meta', None), 'affiliate_level', 'free')
        return level == 'premium'