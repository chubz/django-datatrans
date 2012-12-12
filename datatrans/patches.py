from django.utils.functional import lazy
from django.utils import translation
from django.utils.html import escape, mark_safe
from hashlib import sha1

# Store old, real ugettext function
old_ugettext = translation.ugettext

def new_ugettext(message):
    from django.core.cache import cache

    enabled = cache.get('datatrans_cache_enabled', -1)
    if enabled == -1:
        from datatrans.models import TranslationCacheSettings
        tcs = TranslationCacheSettings.objects.all()[:1]
        enabled = bool(tcs and tcs[0].enabled)
        cache.set('datatrans_cache_enabled', enabled, 30)

    if not enabled:
        return old_ugettext(message)

    lang_code = translation.get_language()

    message_bytes = unicode(message).encode('utf-8')
    key = lang_code + ';' + sha1(message_bytes).hexdigest()

    print key, message

    cached = cache.get(key)
    if not cached:
        cached = old_ugettext(message)
        cache.set(key, cached, 3600 * 24 * 7)

    return cached
    #return mark_safe(u'<span style="text-decoration: overline;" contenteditable>%s</span>' % cached)


def patch_ugettext():
    translation.ugettext = new_ugettext
    translation.ugettext_lazy = lazy(new_ugettext, unicode)

