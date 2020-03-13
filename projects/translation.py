from modeltranslation.translator import translator, TranslationOptions
from .models import CustomerQuestionnaire

class CustomerQuestionnaireTranslationOptions(TranslationOptions):
    fields = ('scope',)

translator.register(CustomerQuestionnaire, CustomerQuestionnaireTranslationOptions)