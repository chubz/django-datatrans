from hashlib import sha1
from django.utils import translation


def get_key(lang_code, message):
    lang_code = translation.get_language()
    message_bytes = unicode(message).encode('utf-8')
    return lang_code + ';' + sha1(message_bytes).hexdigest()


def cached_translation(message, translation_fn):
    from django.core.cache import cache
    
    lang_code = translation.get_language()
    key = get_key(lang_code, message)

    print key, message

    cached = cache.get(key)
    if not cached:
        cached = translation_fn(message)
        cache.set(key, cached, 3600 * 24 * 7)
    return cached


def static_translation(feeder_fn, feed=True):
    def _static_translation(message):
        from datatrans.models import StaticTranslation
        
        lang_code = translation.get_language()
        message_bytes = unicode(message).encode('utf-8')
        digest = sha1(message_bytes).hexdigest()
        
        sts = StaticTranslation.objects.filter(
                language=lang_code,
                digest=digest)[:1]
        
        if not sts:
            if feed:
                st = StaticTranslation.objects.create(
                        language=lang_code,
                        digest=digest,
                        value=feeder_fn(message))
                return st.value
            else:
                return feeder_fn(message)
        else:
            return sts[0].value
        
    return _static_translation


def get_settings():
    from django.core.cache import cache
    
    settings = cache.get('datatrans_cache_settings')
    if settings is None:
        from datatrans.models import TranslationCacheSettings
        try:
            settings, created = TranslationCacheSettings.objects.get_or_create(pk=1)
        except:
            settings = TranslationCacheSettings()
        cache.set('datatrans_cache_settings', settings, 30)
    return settings

