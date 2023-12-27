# custom_context_processors.py

from .models import Notification  # Import your Notification model

def notifications(request):
    if request.user.is_authenticated:
        user = request.user
        notifications = Notification.objects.filter(user=user)
    else:
        notifications = []
    
    return {'notifications': notifications}
