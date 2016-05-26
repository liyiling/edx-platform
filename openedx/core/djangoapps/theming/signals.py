from urlparse import urlparse
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.redirects.models import Redirect


@receiver(post_save, sender=Redirect)
def clear_cache(sender, instance, **kwargs):
    """
    Get the host from the instance.old_path and clear the cache of that host
    """
    cache_key = "theme_redirect.{host}".format(host=urlparse(instance.old_path).netloc)
    cache.delete(cache_key)

