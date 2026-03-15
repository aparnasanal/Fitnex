from datetime import date

def subscription_status(request):
    profile = None
    remaining_days = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profiledb', None)
        if profile and profile.is_subscribed and profile.subscription_expiry:
            remaining_days = (profile.subscription_expiry - date.today()).days
            if remaining_days <= 0:
                profile.is_subscribed = False
                profile.subscription_expiry = None
                profile.save()
                remaining_days = None
    return {
        'profile': profile,
        'remaining_days': remaining_days
    }