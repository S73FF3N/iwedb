from modeltranslation.translator import translator, TranslationOptions
from .models import CustomerQuestionnaire, Turbine_CustomerQuestionnaire

class CustomerQuestionnaireTranslationOptions(TranslationOptions):
    fields = ('scope',)

translator.register(CustomerQuestionnaire, CustomerQuestionnaireTranslationOptions)

class Turbine_CustomerQuestionnaireTranslationOptions(TranslationOptions):
    fields = ('tower_type',)

translator.register(Turbine_CustomerQuestionnaire, Turbine_CustomerQuestionnaireTranslationOptions)