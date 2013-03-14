from django.contrib import admin

from datatrans.models import (KeyValue, 
        TranslationCacheSettings,
        StaticTranslation)


class KeyValueAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'field',
                    'value', 'language', 'edited', 'fuzzy')
    ordering = ('digest', 'language')
    search_fields = ('content_type__app_label', 'content_type__model', 'value',)
    list_filter = ('content_type', 'language', 'edited', 'fuzzy')

admin.site.register(KeyValue, KeyValueAdmin)


class StaticTranslationAdmin(admin.ModelAdmin):
    list_display = ('language', 'original', 'value', 'app_label', 'digest')
    search_fields = ('digest', 'value')
    list_filter = ('language', 'app_label')
    list_editable = ('value',)

admin.site.register(StaticTranslation, StaticTranslationAdmin)


class TranslationCacheSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(TranslationCacheSettings, TranslationCacheSettingsAdmin)
