import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    # This function helps us to avoid duplicate action is the Activity Stream
    # check for any similar action made in the last minute
    now = timezone.now()
    before_now = datetime.timedelta(seconds=60)
    last_minute = now - before_now
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
                                        
    if target:
        target_contenttype = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_content_type=target_contenttype,
                                                    target_id=target.id)
    if not similar_actions:
        # no existing actions found

        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False