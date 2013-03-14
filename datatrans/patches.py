from django.utils.functional import lazy
from django.utils import translation
from django.utils.html import escape, mark_safe


# Store old, real ugettext function
old_ugettext = translation.ugettext

def old_translation(message):
    return old_ugettext(message)

def new_ugettext(message):
    from django.core.cache import cache
    from datatrans import cachetrans

    settings = cachetrans.get_settings()
   
    if not settings.enabled:
        return old_ugettext(message)
    
    translation_fn = old_translation
    if settings.enable_static_translations:
        translation_fn = cachetrans.static_translation(old_translation, feed=settings.feed_static_translations)

    translated = cachetrans.cached_translation(message, translation_fn)
    #return mark_safe(translated)
    return mark_safe(u'<span style="text-decoration: overline;" contenteditable>%s</span>' % translated)


def patch_ugettext():
    translation.ugettext = new_ugettext
    translation.ugettext_lazy = lazy(new_ugettext, unicode)

