import logging

from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.utils import translation

from .models import CustomerQuestionnaire, Turbine_CustomerQuestionnaire, questionnaire_translation_dict
from .tables import CustomerQuestionnaireTable
from .filters import CustomerQuestionnaireFilter
from .utils import CustomerQuestionnaireTableView
from .forms import CustomerQuestionnaireForm, CustomerQuestionnaireForm2, CustomerQuestionnaireForm3, CustomerQuestionnaireForm4, CustomerQuestionnaireForm5, CustomerQuestionnaireForm6
from .forms import TurbineID_FormSet, Manufacturer_FormSet, Turbine_Model_FormSet, HubHeight_FormSet, Comissioning_FormSet, ControlSystem_FormSet, TowerType_FormSet, CMS_FormSet, IceSensor_FormSet, FlickerDetection_FormSet, ObstacleLight_FormSet

class CustomerQuestionnaireList(CustomerQuestionnaireTableView):
    model = CustomerQuestionnaire
    table_class = CustomerQuestionnaireTable
    filter_class = CustomerQuestionnaireFilter

WIZARD_FORMS = [("contact", CustomerQuestionnaireForm6),
                    ("base", CustomerQuestionnaireForm),
                    ("contractual_partner", CustomerQuestionnaireForm2),
                    ("invoice_recipient", CustomerQuestionnaireForm3),
                    ("bank_data", CustomerQuestionnaireForm4),
                    ("shipping_address", CustomerQuestionnaireForm5),
                    ("turbineID", TurbineID_FormSet),
                    ("manufacturer", Manufacturer_FormSet),
                    ("turbine_model", Turbine_Model_FormSet),
                    ("comissioning", Comissioning_FormSet),
                    ("hub_height", HubHeight_FormSet),
                    ("control_system", ControlSystem_FormSet),
                    ("tower_type", TowerType_FormSet),
                    ("cms", CMS_FormSet),
                    ("ice_sensor", IceSensor_FormSet),
                    ("flicker_detection", FlickerDetection_FormSet),
                    ("obstacle_light", ObstacleLight_FormSet),
            ]

FORM_TEMPLATES = {"contact": "projects/customer_questionnaire/contact.html",
                    "base": "projects/customer_questionnaire/base.html",
                    "turbineID": "projects/customer_questionnaire/turbine_base.html",
                    "manufacturer": "projects/customer_questionnaire/manufacturer.html",
                    "turbine_model": "projects/customer_questionnaire/turbine_model.html",
                    "contractual_partner": "projects/customer_questionnaire/contractual_partner.html",
                    "invoice_recipient": "projects/customer_questionnaire/invoice_recipient.html",
                    "bank_data": "projects/customer_questionnaire/bank_data.html",
                    "shipping_address": "projects/customer_questionnaire/shipping_address.html",
                    "comissioning": "projects/customer_questionnaire/comissioning.html",
                    "hub_height": "projects/customer_questionnaire/hub_height.html",
                    "control_system": "projects/customer_questionnaire/control_system.html",
                    "tower_type": "projects/customer_questionnaire/tower_type.html",
                    "cms": "projects/customer_questionnaire/cms.html",
                    "ice_sensor": "projects/customer_questionnaire/ice_sensor.html",
                    "flicker_detection": "projects/customer_questionnaire/flicker_detection.html",
                    "obstacle_light": "projects/customer_questionnaire/obstacle_light.html"}

def bank_data_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] == "Materialanfrage":
        return False
    else:
        return True

def shipping_address_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Materialanfrage", "Auftragsarbeiten"]:
        return True
    else:
        return False

class CustomerQuestionnaireWizard(SessionWizardView):
    condition_dict = {'bank_data': bank_data_form,
                        'shipping_address': shipping_address_form}

    turbine_fields = ["turbineID", "manufacturer", "turbine_model", "comissioning", "hub_height", "control_system", "tower_type", "cms", "ice_sensor", "flicker_detection", "obstacle_light"]

    def get_form_initial(self, step):
        if step in self.turbine_fields:
            form_class = self.form_list[step]
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                extra = data["amount_wec"]
                form_class.extra = extra
        #if step in ["turbine_model"]:
        #    form_class = self.form_list[step]
        #    data = self.get_cleaned_data_for_step("turbineID")
        #    data = [tid["turbine_id"] for tid in data]
            #if data is not None:
            #    count = 0
            #    for f in form_class.forms:
            #        f.initial = {'turbine_id': data[count]}
            #        count += 1
        return super(CustomerQuestionnaireWizard, self).get_form_initial(step)

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    """def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current in ["turbineID", "manufacturer", "turbine_model"]:
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                amount_wec = data["amount_wec"]
            context.update({'amount_wec':range(amount_wec)})
        return context"""

    def done(self, form_list, form_dict, **kwargs):
        log = logging.getLogger(__name__)
        customer_questionnaire = form_dict["contact"].save()
        turbine_dict = {}
        for turbine in range(int(form_dict["base"]["amount_wec"].value())):
            turbine_dict[str(turbine)] = Turbine_CustomerQuestionnaire.objects.create(customer_questionnaire=customer_questionnaire)
        log.info("turbine dict: "+str(turbine_dict))
        for step_name in form_dict.keys():
            log.info("step: "+step_name)
            if not step_name == "contact":
                if not step_name in self.turbine_fields:
                    for field in form_dict[step_name]:
                        customer_questionnaire.__dict__[field.name] = field.value()
                        customer_questionnaire.save()
                else:
                    turbine_count = 0
                    for turbine_form in form_dict[step_name]:
                        turbine_count_str = str(turbine_count)
                        for field in turbine_form:
                            if not field.name == "id":
                                log.info("field: "+str(field.name))
                                log.info("value: "+str(field.value()))
                                if field.name in ["manufacturer", "turbine_model"]:
                                    turbine_dict[turbine_count_str].__dict__[field.name+"_id"] = field.value()
                                else:
                                    turbine_dict[turbine_count_str].__dict__[field.name] = field.value()
                                turbine_dict[turbine_count_str].save()
                        turbine_count += 1
        if self.request.LANGUAGE_CODE == "en":
            with translation.override("de"):
                customer_questionnaire.__dict__["scope_de"] = _(form_dict["base"]["scope"].value())
        else:
            customer_questionnaire.__dict__["scope_en"] = questionnaire_translation_dict[str(form_dict["base"]["scope"].value())]
        return render(self.request, 'projects/customer_questionnaire/done.html')

class CustomerQuestionnaireEdit(SessionWizardView):
    condition_dict = {'bank_data': bank_data_form,
                        'shipping_address': shipping_address_form}

    turbine_fields = ["turbineID", "manufacturer", "turbine_model", "comissioning", "hub_height", "control_system", "tower_type", "cms", "ice_sensor", "flicker_detection", "obstacle_light"]

    def get_form_instance(self, step):
        if not self.instance_dict:
            if 'questionnaire_pk' in self.kwargs:
                questionnaire_pk = self.kwargs['questionnaire_pk']
                return CustomerQuestionnaire.objects.get(pk=questionnaire_pk)
        return None

    def get_form_kwargs(self, step=None):
        if step is None:
            step = self.steps.current

        kwargs = super().get_form_kwargs(step)
        if step in self.turbine_fields:
            kwargs["questionnaire_pk"] = self.kwargs["questionnaire_pk"]
        return kwargs

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        log = logging.getLogger(__name__)
        customer_questionnaire = CustomerQuestionnaire.objects.get(pk=self.kwargs['questionnaire_pk'])
        turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)
        log.info("turbines: "+str(turbines))
        for step_name in form_dict.keys():
            if not step_name == "contact":
                if not step_name in self.turbine_fields:
                    for field in form_dict[step_name]:
                        customer_questionnaire.__dict__[field.name] = field.value()
                        customer_questionnaire.save()
                else:
                    turbine_count = 0
                    for turbine_form in form_dict[step_name]:
                        for field in turbine_form:
                            if not field.name == "id":
                                if field.name in ["manufacturer", "turbine_model"]:
                                    turbines[turbine_count].__dict__[field.name+"_id"] = field.value()
                                    log.info("field value: "+str(field.value()))
                                else:
                                    turbines[turbine_count].__dict__[field.name] = field.value()
                                #log.info("turbines[turbine_count]: "+str(turbines[turbine_count]))
                        turbine_count += 1
        for t in turbines:
            t.save()
        log.info("turbines: "+str(turbines))
        if self.request.LANGUAGE_CODE == "en":
            with translation.override("de"):
                customer_questionnaire.__dict__["scope_de"] = _(form_dict["base"]["scope"].value())
        else:
            customer_questionnaire.__dict__["scope_en"] = questionnaire_translation_dict[str(form_dict["base"]["scope"].value())]
        return render(self.request, 'projects/customer_questionnaire/done.html')