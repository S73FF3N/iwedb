from modeltranslation.translator import translator, TranslationOptions
from .models import Event, Date

class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'time_interval', 'duration')

translator.register(Event, EventTranslationOptions)

class DateTranslationOptions(TranslationOptions):
    fields = ('status', 'comment', 'part_of_contract')

translator.register(Date, DateTranslationOptions)