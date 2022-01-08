
from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich
from account.models import Entrepreneur, Contributor
from feed.models import Like, Follow

def get_user_data(request):
    if request.user.is_authenticated:
        try:
            user_obj = Contributor.objects.get(user=request.user)
            tp = 'contributor'
        except:
            user_obj = Entrepreneur.objects.get(user=request.user)
            tp = 'entrepreneur'
        enricher = Enrich()
        notification_feed = feed_manager.get_notification_feed(user_id)
        activities = notification_feed.get(limit=25)['results']
        notifications = enricher.enrich_activities(activities)
        kwargs = {
            'login_user': request.user,
            'user_object': user_obj,
            'type': tp,
            'notifications': notifications,
            'all_likes': Like.objects.filter(actor=request.user)
            'all_follows': Follow.objects.filter(actor=request.user)
        }
    else:
        kwargs = {'login_user': None}
    return kwargs