import logging, os
from weasyprint import HTML
from collections import OrderedDict

from formtools.wizard.views import SessionWizardView
from django.utils import translation
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import CustomerQuestionnaire, Turbine_CustomerQuestionnaire
from .tables import CustomerQuestionnaireTable
from .filters import CustomerQuestionnaireFilter
from .utils import CustomerQuestionnaireTableView
from .forms import CQBaseForm, ContractualPartnerForm, IRForm, BankDataForm, ShippingAddressForm, ContactForm, APOnsiteForm, COForm, TOForm, ContractStatusForm, DocumentationForm, CommunicationForm
from .forms import TurbineID_FormSet, Turbine_Model_FormSet, ControlSystem_FormSet, TowerType_FormSet, CMS_FormSet, ServiceLift_FormSet, GeoLocation_FormSet, Ladder_FormSet, IceSensor_FormSet, FlickerDetection_FormSet, ObstacleLight_FormSet, Antenna_FormSet, SDL_FormSet, YearlyProduction_FormSet, Maintenance_FormSet, OilExchange_FormSet, Inspection_FormSet, Gearbox_FormSet, Generator_FormSet, RotorBlade_FormSet, Converter_FormSet, Reports_FormSet

class CustomerQuestionnaireList(CustomerQuestionnaireTableView):
    model = CustomerQuestionnaire
    table_class = CustomerQuestionnaireTable
    filter_class = CustomerQuestionnaireFilter

WIZARD_FORMS = [("contact", ContactForm),
                    ("base", CQBaseForm),
                    ("contractual_partner", ContractualPartnerForm),
                    ("authorized_person", APOnsiteForm),
                    ("invoice_recipient", IRForm),
                    ("bank_data", BankDataForm),
                    ("shipping_address", ShippingAddressForm),
                    ("commercial_operator", COForm),
                    ("technical_operator", TOForm),
                    ("contract_status", ContractStatusForm),
                    ("turbineID", TurbineID_FormSet),
                    ("turbine_model", Turbine_Model_FormSet),
                    ("control_system", ControlSystem_FormSet),
                    ("location", GeoLocation_FormSet),
                    ("tower_type", TowerType_FormSet),
                    ("service_lift", ServiceLift_FormSet),
                    ("ladder", Ladder_FormSet),
                    ("cms", CMS_FormSet),
                    ("ice_sensor", IceSensor_FormSet),
                    ("flicker_detection", FlickerDetection_FormSet),
                    ("obstacle_light", ObstacleLight_FormSet),
                    ("antenna", Antenna_FormSet),
                    ("sdl", SDL_FormSet),
                    ('maintenance', Maintenance_FormSet),
                    ('inspection', Inspection_FormSet),
                    ('oil_exchange', OilExchange_FormSet),
                    ("communication", CommunicationForm),
                    ("documentation", DocumentationForm),
                    ("reports", Reports_FormSet),
                    ("yearly_production", YearlyProduction_FormSet),
                    ("gearbox", Gearbox_FormSet),
                    ("generator", Generator_FormSet),
                    ("rotor_blade", RotorBlade_FormSet),
                    ("converter", Converter_FormSet),
            ]

FORM_TEMPLATES = {"contact": "projects/customer_questionnaire/contact.html",
                    "base": "projects/customer_questionnaire/base.html",
                    "turbineID": "projects/customer_questionnaire/turbine_base.html",
                    "turbine_model": "projects/customer_questionnaire/turbine_model.html",
                    "contractual_partner": "projects/customer_questionnaire/contractual_partner.html",
                    "authorized_person": "projects/customer_questionnaire/authorized_person.html",
                    "invoice_recipient": "projects/customer_questionnaire/invoice_recipient.html",
                    "bank_data": "projects/customer_questionnaire/bank_data.html",
                    "shipping_address": "projects/customer_questionnaire/shipping_address.html",
                    "commercial_operator": "projects/customer_questionnaire/commercial_operator.html",
                    "technical_operator": "projects/customer_questionnaire/technical_operator.html",
                    "contract_status": "projects/customer_questionnaire/contract_status.html",
                    "location": "projects/customer_questionnaire/location.html",
                    "control_system": "projects/customer_questionnaire/control_system.html",
                    "tower_type": "projects/customer_questionnaire/tower_type.html",
                    "service_lift": "projects/customer_questionnaire/service_lift.html",
                    "ladder": "projects/customer_questionnaire/ladder.html",
                    "cms": "projects/customer_questionnaire/cms.html",
                    "ice_sensor": "projects/customer_questionnaire/ice_sensor.html",
                    "flicker_detection": "projects/customer_questionnaire/flicker_detection.html",
                    "obstacle_light": "projects/customer_questionnaire/obstacle_light.html",
                    "antenna": "projects/customer_questionnaire/antenna.html",
                    "sdl": "projects/customer_questionnaire/sdl.html",
                    "maintenance": "projects/customer_questionnaire/maintenance.html",
                    "inspection": "projects/customer_questionnaire/inspection.html",
                    "oil_exchange": "projects/customer_questionnaire/oil_exchange.html",
                    "communication": "projects/customer_questionnaire/communication.html",
                    "documentation": "projects/customer_questionnaire/documentation.html",
                    "reports": "projects/customer_questionnaire/reports.html",
                    "yearly_production": "projects/customer_questionnaire/yearly_production.html",
                    "gearbox": "projects/customer_questionnaire/gearbox.html",
                    "generator": "projects/customer_questionnaire/generator.html",
                    "rotor_blade": "projects/customer_questionnaire/rotor_blade.html",
                    "converter": "projects/customer_questionnaire/converter.html"
                    }

def exclude_material_request(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Request for Material"]:
        return False
    else:
        return True

def material_request_and_comissioned_work(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Request for Material", "Commisioned Work"]:
        return True
    else:
        return False

def exclude_material_request_and_support(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Request for Material", "Support Contract"]:
        return False
    else:
        return True

def service_and_to(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Service Contract", "Technical Operations Contract"]:
        return True
    else:
        return False

def service_and_commisioned_work(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Service Contract", "Commisioned Work"]:
        return True
    else:
        return False

def only_service(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('base') or {'scope': 'none'}
    if cleaned_data['scope'] in ["Service Contract"]:
        return True
    else:
        return False

class CustomerQuestionnaireWizard(SessionWizardView):
    condition_dict = {'authorized_person': exclude_material_request_and_support,
                        'bank_data': exclude_material_request,
                        'shipping_address': material_request_and_comissioned_work,
                        'commercial_operator': service_and_to,
                        'technical_operator': only_service,
                        'contract_status': only_service,
                        'location': only_service,
                        'tower_type': exclude_material_request_and_support,
                        'service_lift': exclude_material_request_and_support,
                        'ladder': exclude_material_request_and_support,
                        'cms': service_and_to,
                        'ice_sensor': service_and_to,
                        'flicker_detection': service_and_to,
                        'obstacle_light': service_and_to,
                        'antenna':service_and_to,
                        'sdl': service_and_to,
                        'maintenance': service_and_to,
                        'inspection': exclude_material_request_and_support,
                        'oil_exchange': service_and_to,
                        'communication': service_and_to,
                        'reports': only_service,
                        'documentaion': service_and_commisioned_work,
                        'yearly_production': service_and_to,
                        'gearbox': service_and_to,
                        'generator': service_and_to,
                        'rotor_blade': service_and_to,
                        'converter': service_and_to,
                        }

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'customer_questionnaire'))

    turbine_fields = ["turbineID", "manufacturer", "turbine_model", "comissioning", "latitude", "longitude", "hub_height", "control_system", "tower_type", "service_lift", "service_lift_type", "arrester", "ladder", "cms", "cms_type", "ice_sensor", "ice_sensor_type", "flicker_detection", "flicker_detection_type", 'obstacle_light_system', 'obstacle_light_manufacturer', 'obstacle_light_type', 'antenna', 'antenna_type', 'sdl', 'yearly_production_1', 'sdl', 'yearly_production_2', 'sdl', 'yearly_production_3', 'recent_maintenance', 'date_of_recent_maintenance', 'date_of_5_year_maintenance', 'date_of_transformer_maintenance', 'date_of_converter_maintenance', 'date_of_lattice_maintenance', 'date_of_overhaul_winch', 'date_oil_exchange_main_bearing', 'oil_type_main_bearing', 'date_oil_exchange_yaw_gearbox', 'oil_type_yaw_gearbox', 'date_oil_exchange_yaw_bearing', 'oil_type_yaw_bearing', 'date_oil_exchange_pitch_gearbox', 'oil_type_pitch_gearbox', 'date_oil_exchange_hydraulic', 'oil_type_hydraulic', 'feed_in_tarif', 'date_cb_inspection_machine_tower', 'date_recurring_inspection', 'date_rotor_blade_inspection', 'date_gearbox_endoscopy', 'date_safety_inspection', 'date_service_lift_maintenance', 'date_service_lift_inspection', 'date_electric_inspection', 'date_blade_bearing_inspection','gearbox_manufacturer', 'gearbox_type', 'gearbox_serialnr', 'gearbox_year', 'generator_manufacturer', 'generator_type', 'generator_serialnr', 'generator_year', 'rotor_blade_manufacturer', 'rotor_blade_type', 'rotor_blade_serialnr', 'rotor_blade_year', 'converter_manufacturer', 'converter_type', 'converter_serialnr', 'converter_year', 'output_power', 'expert_reports']

    turbine_steps = ["turbineID", "turbine_model", "control_system", "location", "tower_type", "service_lift", "ladder", "cms", "ice_sensor", "flicker_detection", "obstacle_light", "antenna", "sdl", "maintenance", "inspection", "oil_exchange", "reports", "yearly_production", "gearbox", "generator", "rotor_blade", "converter"]

    def render_next_step(self, form, **kwargs):
        wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
        if wizard_save_for_later:
            return self.render_done_without_validation(form, **kwargs)
        else:
            return super(CustomerQuestionnaireWizard, self).render_next_step(form)

    def render_done_without_validation(self, form, **kwargs):

        final_forms = OrderedDict()
        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            final_forms[form_key] = form_obj

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def get_form_initial(self, step):

        if step in self.turbine_steps:
            form_class = self.form_list[step]
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                extra = data["amount_wec"]
                form_class.extra = extra
        return super(CustomerQuestionnaireWizard, self).get_form_initial(step)

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current in ["turbineID", "inspection", "documentation"]:
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                scope = data["scope"]
            context.update({'scope':scope})
        return context

    def done(self, form_list, form_dict, **kwargs):
        logger = logging.getLogger(__name__)
        customer_questionnaire = form_dict["contact"].save()
        for turbine in range(int(form_dict["base"]["amount_wec"].value())):
            Turbine_CustomerQuestionnaire.objects.create(customer_questionnaire=customer_questionnaire)
        turbine_ids = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire).values_list('id', flat=True)
        logger.info("turbine_ids: "+str(turbine_ids))
        logger.info("form language: "+str(translation.get_language()))
        for step_name in form_dict.keys():
            if not step_name == "contact":
                if not step_name in self.turbine_steps:
                    for field in form_dict[step_name]:
                        if field.name in ["scope"]:
                            setattr(customer_questionnaire, field.name, field.value())
                        elif customer_questionnaire._meta.get_field(field.name).null and field.value() == "":
                                    customer_questionnaire.__dict__[field.name] = None
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
                                if field.name in ["tower_type"]:
                                    setattr(t_object, field.name, field.value())
                                elif t_object._meta.get_field(field.name).null and field.value() == "":
                                    t_object.__dict__[field.name] = None
                                else:
                                    t_object.__dict__[field.name] = field.value()
                        t_object.save()
                        turbine_count += 1
        customer_questionnaire.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))

class CustomerQuestionnaireEdit(SessionWizardView):
    condition_dict = {'authorized_person': exclude_material_request_and_support,
                        'bank_data': exclude_material_request,
                        'shipping_address': material_request_and_comissioned_work,
                        'commercial_operator': service_and_to,
                        'technical_operator': only_service,
                        'contract_status': only_service,
                        'location': only_service,
                        'tower_type': exclude_material_request_and_support,
                        'service_lift': exclude_material_request_and_support,
                        'ladder': exclude_material_request_and_support,
                        'cms': service_and_to,
                        'ice_sensor': service_and_to,
                        'flicker_detection': service_and_to,
                        'obstacle_light': service_and_to,
                        'antenna':service_and_to,
                        'sdl': service_and_to,
                        'maintenance': service_and_to,
                        'inspection': exclude_material_request_and_support,
                        'oil_exchange': service_and_to,
                        'communication': service_and_to,
                        'reports': only_service,
                        'documentaion': service_and_commisioned_work,
                        'yearly_production': service_and_to,
                        'gearbox': service_and_to,
                        'generator': service_and_to,
                        'rotor_blade': service_and_to,
                        'converter': service_and_to,
                        }

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'customer_questionnaire'))

    turbine_fields = ["turbineID", "manufacturer", "turbine_model", "comissioning", "hub_height", "control_system", "tower_type", "cms", "ice_sensor", "flicker_detection", "obstacle_light"]

    turbine_steps = ["turbineID", "turbine_model", "control_system", "location", "tower_type", "service_lift", "ladder", "cms", "ice_sensor", "flicker_detection", "obstacle_light", "antenna", "sdl", "maintenance", "inspection", "oil_exchange", "reports", "yearly_production", "gearbox", "generator", "rotor_blade", "converter"]

    def render_next_step(self, form, **kwargs):
        wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
        if wizard_save_for_later:
            return self.render_done_without_validation(form, **kwargs)
        else:
            return super(CustomerQuestionnaireEdit, self).render_next_step(form)

    def render_done_without_validation(self, form, **kwargs):

        final_forms = OrderedDict()
        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            final_forms[form_key] = form_obj

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

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
        if step in self.turbine_steps:
            kwargs["questionnaire_pk"] = self.kwargs["questionnaire_pk"]
        return kwargs

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current in ["turbineID", "inspection", "documentation"]:
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                scope = data["scope"]
            context.update({'scope':scope})
        return context

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        customer_questionnaire = CustomerQuestionnaire.objects.get(pk=self.kwargs['questionnaire_pk'])
        turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)
        for step_name in form_dict.keys():
            if not step_name == "contact":
                if not step_name in self.turbine_steps:
                    for field in form_dict[step_name]:
                        if field.name in ["scope"]:
                            setattr(customer_questionnaire, field.name, field.value())
                        elif customer_questionnaire._meta.get_field(field.name).null and field.value() == "":
                                    customer_questionnaire.__dict__[field.name] = None
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
                                if turbines[turbine_count]._meta.get_field(field.name).null and field.value() == "":
                                    turbines[turbine_count].__dict__[field.name] = None
                                elif field.name in ["tower_type"]:
                                    setattr(turbines[turbine_count], field.name, field.value())
                                else:
                                    turbines[turbine_count].__dict__[field.name] = field.value()
                        turbine_count += 1
        for t in turbines:
            t.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))

def export_pdf(request, questionnaire_pk):
    customer_questionnaire = get_object_or_404(CustomerQuestionnaire, id=questionnaire_pk)
    turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)

    html_string = render_to_string('projects/customer_questionnaire/export_pdf.html', {'customer_questionnaire': customer_questionnaire, 'turbines': turbines.all(),})
    result = HTML(string=html_string).write_pdf()

    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=CustomerQuestionnaire.pdf'
    return response