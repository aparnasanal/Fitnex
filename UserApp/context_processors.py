from django.utils import timezone

def subscription_status(request):
    profile = None
    remaining_days = None

    if request.user.is_authenticated:
        profile = getattr(request.user, 'profiledb', None)

        if profile and profile.is_subscribed and profile.subscription_expiry:
            remaining_time = profile.subscription_expiry - timezone.now()

            if remaining_time.total_seconds() > 0:
                remaining_days = remaining_time.days
            else:
                profile.is_subscribed = False
                profile.subscription_expiry = None
                profile.save()
                remaining_days = None

    return {
        'profile': profile,
        'remaining_days': remaining_days
    }