import logging

from formtools.wizard.views import SessionWizardView
from django.utils.translation import ugettext as _
from django.utils import translation
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

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
                    "obstacle_light": "projects/customer_questionnaire/obstacle_light.html"
                    }

def exclude_material_request(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] == _("Request for Material"):
        return False
    else:
        return True

def material_request_and_comissioned_work(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in [_("Request for Material"), _("Commisioned Work")]:
        return True
    else:
        return False

def exclude_material_request_and_support(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in [_("Request for Material"), _("Support Contract")]:
        return False
    else:
        return True

def service_and_to(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in [_("Service Contract"), _("Technical Operations Contract")]:
        return True
    else:
        return False

class CustomerQuestionnaireWizard(SessionWizardView):
    condition_dict = {'bank_data': exclude_material_request,
                        'shipping_address': material_request_and_comissioned_work,
                        'comissioning': exclude_material_request_and_support,
                        'hub_height': exclude_material_request_and_support,
                        'tower_type': exclude_material_request_and_support,
                        'cms': service_and_to,
                        'ice_sensor': service_and_to,
                        'flicker_detection': service_and_to,
                        'obstacle_light': service_and_to,}

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
        logger = logging.getLogger(__name__)
        customer_questionnaire = form_dict["contact"].save()
        for turbine in range(int(form_dict["base"]["amount_wec"].value())):
            Turbine_CustomerQuestionnaire.objects.create(customer_questionnaire=customer_questionnaire)
        #turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)
        turbine_ids = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire).values_list('id', flat=True)
        logger.info("turbine_ids: "+str(turbine_ids))
        logger.info("form language: "+str(translation.get_language()))
        for step_name in form_dict.keys():
            if not step_name == "contact":
                if not step_name in self.turbine_fields:
                    for field in form_dict[step_name]:
                        if field.name == "scope":
                            customer_questionnaire.__dict__[field.name] = str(field.value())
                            with translation.override("de"):
                                customer_questionnaire.__dict__["scope_de"] = _(field.value())
                                try:
                                    customer_questionnaire.__dict__["scope_en"] = questionnaire_translation_dict[str(field.value())]
                                except:
                                    customer_questionnaire.__dict__["scope_en"] = str(field.value())
                        else:
                            customer_questionnaire.__dict__[field.name] = field.value()
                else:
                    turbine_count = 0
                    for turbine_form in form_dict[step_name]:
                        t_object = Turbine_CustomerQuestionnaire.objects.get(id=turbine_ids[turbine_count])
                        for field in turbine_form:
                            if not field.name == "id":
                                if field.name in ["manufacturer", "turbine_model"]:
                                    t_object.__dict__[field.name+"_id"] = field.value()
                                if field.name in ["comissioning", "hub_height"] and field.value() == "":
                                    #Fehler: Form is not saved if 'comissioning' or 'hub_height' is left empty, even though both fields are null=True
                                    t_object.__dict__[field.name] = None
                                if field.name == "tower_type":
                                    #Fehler: tower_type is always assigned 'Lattice Tower'/'Gittermastturm', even when 'Tubular Tower'/'Rohrturm' is chosen
                                    t_object.__dict__[field.name] = str(field.value())
                                    with translation.override("de"):
                                        t_object.__dict__["tower_type_de"] = _(field.value())
                                        try:
                                            t_object.__dict__["tower_type_en"] = questionnaire_translation_dict[str(field.value())]
                                        except:
                                            t_object.__dict__["tower_type_en"] = str(field.value())
                                else:
                                    t_object.__dict__[field.name] = field.value()
                        t_object.save()
                        logger.info("turbine.tower_type: "+str(t_object.tower_type))
                        logger.info("turbine.tower_type_de: "+str(t_object.tower_type_de))
                        logger.info("turbine.tower_type_en: "+str(t_object.tower_type_en))
                        turbine_count += 1
        customer_questionnaire.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))

class CustomerQuestionnaireEdit(SessionWizardView):
    condition_dict = {'bank_data': exclude_material_request,
                        'shipping_address': material_request_and_comissioned_work,
                        'comissioning': exclude_material_request_and_support,
                        'hub_height': exclude_material_request_and_support,
                        'tower_type': exclude_material_request_and_support,
                        'cms': service_and_to,
                        'ice_sensor': service_and_to,
                        'flicker_detection': service_and_to,
                        'obstacle_light': service_and_to,}

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
        customer_questionnaire = CustomerQuestionnaire.objects.get(pk=self.kwargs['questionnaire_pk'])
        turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)
        for step_name in form_dict.keys():
            if not step_name == "contact":
                if not step_name in self.turbine_fields:
                    for field in form_dict[step_name]:
                        if field.name == "scope":
                            customer_questionnaire.__dict__[field.name] = str(field.value())
                        else:
                            customer_questionnaire.__dict__[field.name] = field.value()
                        customer_questionnaire.save()
                else:
                    turbine_count = 0
                    for turbine_form in form_dict[step_name]:
                        for field in turbine_form:
                            if not field.name == "id":
                                if field.name in ["manufacturer", "turbine_model"]:
                                    turbines[turbine_count].__dict__[field.name+"_id"] = field.value()
                                if field.name in ["comissioning", "hub_height"] and field.value() == "":
                                    turbines[turbine_count].__dict__[field.name] = None
                                if field.name == "tower_type":
                                    turbines[turbine_count].__dict__[field.name] = str(field.value())
                                else:
                                    turbines[turbine_count].__dict__[field.name] = field.value()
                        turbine_count += 1
        if self.request.LANGUAGE_CODE == "en":
            with translation.override("de"):
                customer_questionnaire.__dict__["scope_de"] = _(form_dict["base"]["scope"].value())
                customer_questionnaire.__dict__["scope_en"] = str(form_dict["base"]["scope"].value())
                turbine_count = 0
                for turbine_form in form_dict["tower_type"]:
                    turbines[turbine_count].__dict__["tower_type_de"] = _(turbine_form["tower_type"].value())
                    turbines[turbine_count].__dict__["tower_type_en"] = turbine_form["tower_type"].value()
                    turbines[turbine_count].save()
                    turbine_count += 1
        else:
            customer_questionnaire.__dict__["scope_en"] = questionnaire_translation_dict[str(form_dict["base"]["scope"].value())]
            turbine_count = 0
            for turbine_form in form_dict["tower_type"]:
                turbines[turbine_count].__dict__["tower_type_en"] = questionnaire_translation_dict[str(turbine_form["tower_type"].value())]
                turbines[turbine_count].__dict__["tower_type_de"] = turbine_form["tower_type"].value()
                turbine_count += 1
        for t in turbines:
            t.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))