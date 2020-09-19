import logging, os
from weasyprint import HTML
from collections import OrderedDict
from zipfile import ZipFile

from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import CustomerQuestionnaire, Turbine_CustomerQuestionnaire
from .tables import CustomerQuestionnaireTable, CustomerQuestionnaireTable2
from .filters import CustomerQuestionnaireFilter
from .utils import CustomerQuestionnaireTableView
from .forms import CQBaseForm, ContractualPartnerForm, IRForm, BankDataForm, ShippingAddressForm, ContactForm, APOnsiteForm, COForm, TOForm, ContractStatusForm, DocumentationForm, CommunicationForm
from .forms import TurbineID_FormSet, Turbine_Model_FormSet, ControlSystem_FormSet, TowerType_FormSet, CMS_FormSet, ServiceLift_FormSet, GeoLocation_FormSet, Ladder_FormSet, IceSensor_FormSet, FlickerDetection_FormSet, ObstacleLight_FormSet, Antenna_FormSet, SDL_FormSet, YearlyProduction_FormSet, Maintenance_FormSet, OilExchange_FormSet, Inspection_FormSet, Gearbox_FormSet, Generator_FormSet, RotorBlade_FormSet, Converter_FormSet, Reports_FormSet

class CustomerQuestionnaireList(CustomerQuestionnaireTableView):
    model = CustomerQuestionnaire
    table_class = CustomerQuestionnaireTable
    filter_class = CustomerQuestionnaireFilter

class Customer_CustomerQuestionnaireList(CustomerQuestionnaireTableView):
    model = CustomerQuestionnaire
    table_class = CustomerQuestionnaireTable2
    filter_class = CustomerQuestionnaireFilter
    template_name = "customer_questionnaire/list_for_customer.html"

WIZARD_FORMS = [("contact", ContactForm),
                    ("base", CQBaseForm),
                    ("contractual_partner", ContractualPartnerForm),
                    ("authorized_person", APOnsiteForm),
                    ("invoice_recipient", IRForm),
                    ("bank_data", BankDataForm),
                    ("shipping_address", ShippingAddressForm),
                    ("commercial_operator", COForm),
                    ("technical_operator", TOForm),
                    ("communication", CommunicationForm),
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

REQUIRED_FIELDS = {"questionnaire": (
                                    #step_name, field1, field2, ...
                                    ("contact", ("contact_company", _('Contact Company')), ("contact_name", _('Contact Name')), ("contact_mail", ('Contact Mail'))),
                                    ("base", ("scope",_('Scope')), ("wind_farm_name",_('Windfarm Name')), ("postal_code",_('Postal Code of Windfarm')), ("city",_('City of Windfarm')), ("amount_wec",_('Amount WEC'))),
                                    ("contractual_partner", ("contractual_partner",_("Contractual Partner")), ("cp_street_nr",_('Street of Contractual Partner')), ("cp_postal_code",_('Postal Code of Contractual Partner')), ("cp_city",_('City of Contractual Partner')), ("cp_phone",_('Phone number of Contractual Partner'))),
                                    ("commercial_operator", ("commercial_operator",_("Commercial Operator"))),
                                    ("technical_operator", ("technical_operator",_("Technical Operator"))),
                                    ("contract_status", ("current_service_contract",_("Current service contract")), ("desired_service_contract",_("Desired service contract scope")), ("desired_duration_service_contract",_("Desired duration of service contract")),("commencement_current_service_contract", _("Expiry of current service contract"))),
                                    ),
                    "turbine_questionnaire": (
                                            ("turbineID", ("turbine_id",_("Turbine ID")), ("comissioning",_("Date of comissioning"))),
                                            ("turbine_model", ("manufacturer",_("Manufacturer")), ("turbine_model",_("Turbine Model"))),
                                            ("control_system", ("output_power",_('Output power'))),
                                            ("tower_type", ("hub_height",_("Hub Height")), ("tower_type",_("Type of tower"))),
                                            ("service_lift", ("service_lift",_("Service Lift")), ("service_lift_type",_("Type of Service Lift"))),
                                            ("yearly_production", ("yearly_production_1",_("Yearly Production 1")), ("yearly_production_2",_("Yearly Production 2")), ("yearly_production_3",_("Yearly Production 3"))),
                                            ("gearbox", ("gearbox_type",_("Type of gearbox"))),
                                            ("generator", ("generator_type",_("Type of generator"))),
                                            ("rotor_blade", ("rotor_blade_type",_("Type of rotor blades"))),
                                            ("converter", ("converter_type",_("Type of converter")))
                                            )
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

    #Overrides render_next_step method --> entry point for custom features
    def render_next_step(self, form, **kwargs):
        wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
        if wizard_save_for_later:
            return self.render_done(form, **kwargs)
        save_for_later_modal =  self.request.POST.get('save_for_later_modal', None)
        if save_for_later_modal:
            return self.get_progress()
        go_to_step = self.request.POST.get('go-to-step', None)
        if go_to_step and list(self.get_form_list().items())[int(go_to_step)-1][0] != self.steps.current:
            #If turbineID would be skipped
            turbineID_step = list(self.get_form_list().keys()).index("turbineID")
            if int(go_to_step) > turbineID_step and self.get_cleaned_data_for_step("turbineID") == None:
                #Go to turbineID
                self.storage.current_step = list(self.get_form_list().items())[turbineID_step-1][0]
            else:
                self.storage.current_step = list(self.get_form_list().items())[int(go_to_step)-2][0]
        return super(CustomerQuestionnaireWizard, self).render_next_step(form)

    #Overrides render_done method --> entry point for custom features
    def render_done(self, form, **kwargs):
        save_for_later_modal =  self.request.POST.get('save_for_later_modal', None)
        if save_for_later_modal:
            return self.get_progress()
        final_forms = OrderedDict()
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
            if not wizard_save_for_later:
                if not form_obj.is_valid():
                    return self.render_revalidation_failure(form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj
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

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current in self.turbine_steps:
            data = self.get_cleaned_data_for_step("turbineID")
            turbine_ids = []
            if data is not None:
                for i in range(len(data)):
                    try:
                        turbine_id = data[i]["turbine_id"]
                        if turbine_id == "":
                            turbine_id = "WEA " + str(i+1)
                    except KeyError:
                        turbine_id = "WEA " + str(i+1)
                    turbine_ids.append(turbine_id)
                context.update({'turbine_ids':turbine_ids})
        if self.steps.current in ["turbineID", "inspection", "documentation"]:
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                scope = data["scope"]
                context.update({'scope':scope})
        if self.steps.current == "inspection":
                data = self.get_cleaned_data_for_step("turbine_model")
                if data is not None:
                    for i in range(len(data)):
                        if data[i] != {} and str(data[i]["turbine_model"]) in ["Senvion MM100","Repower MM82","Repower MM70","Senvion MM92/2050","Senvion MM82/2050","Repower MM82 evo","Repower MM92","Repower MM92 evo"]:
                            try:
                                context["date_blade_bearing_inspection"].append(i+1)
                            except KeyError:
                                context.update({"date_blade_bearing_inspection":[i+1]})
        return context

    def get_step_condition(self, key):
        if key in self.condition_dict:
            return self.condition_dict[key](self)
        else:
            return True

    def get_progress(self):
        steps = []
        questionnaire_steps = REQUIRED_FIELDS["questionnaire"]
        for step in questionnaire_steps:
            key = step[0]
            if self.get_step_condition(key):
                data = self.get_cleaned_data_for_step(key)
                if data != None:
                    for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        if data[field[0]] == None:
                            field_info["status"]= "not processed"
                        elif str(data[field[0]]) == "":
                            field_info["status"]= "not processed"
                        else:
                            field_info["status"]= "processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
                else:
                   for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= "not processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
        turbine_questionnaire_steps = REQUIRED_FIELDS["turbine_questionnaire"]
        for step in turbine_questionnaire_steps:
            key = step[0]
            if self.get_step_condition(key):
                data_turbines = self.get_cleaned_data_for_step(key)
                #Every turbine has to be processed to get a checkmark
                if data_turbines != None:
                    for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= ""
                        for data in data_turbines:
                            if data == {} or data[field[0]] == None or str(data[field[0]]) == "":
                                if field_info["status"] == "" or field_info["status"] == "not processed":
                                    field_info["status"]= "not processed"
                                else:
                                    field_info["status"]= "partly processed"
                            else:
                                if field_info["status"] == "" or field_info["status"] == "processed":
                                    field_info["status"]= "processed"
                                else:
                                    field_info["status"]= "partly processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
                else:
                   for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= "not processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
        html = render_to_string('projects/customer_questionnaire/questionnaire_progress.html', {'steps': steps})
        return HttpResponse(html)

    def done(self, form_list, form_dict, **kwargs):
        customer_questionnaire = form_dict["contact"].save()
        for turbine in range(int(form_dict["base"]["amount_wec"].value())):
            Turbine_CustomerQuestionnaire.objects.create(customer_questionnaire=customer_questionnaire)
        turbine_ids = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire).values_list('id', flat=True)

        if self.request.user.is_authenticated:
            setattr(customer_questionnaire, "created_by", User.objects.get(id=self.request.user.id))
            customer_questionnaire.save()

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
                                if t_object._meta.get_field(field.name).null and field.value() == "":
                                    t_object.__dict__[field.name] = None
                                elif field.name in ["manufacturer", "turbine_model"]:
                                    t_object.__dict__[field.name+"_id"] = field.value()
                                elif field.name in ["tower_type"]:
                                    setattr(t_object, field.name, field.value())
                                else:
                                    t_object.__dict__[field.name] = field.value()
                        t_object.save()
                        turbine_count += 1
        customer_questionnaire.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_view'))

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

    #Overrides render_next_step method --> entry point for custom features
    def render_next_step(self, form, **kwargs):
        wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
        if wizard_save_for_later:
            return self.render_done(form, **kwargs)
        save_for_later_modal =  self.request.POST.get('save_for_later_modal', None)
        if save_for_later_modal:
            return self.get_progress()
        go_to_step = self.request.POST.get('go-to-step', None)
        if go_to_step and list(self.get_form_list().items())[int(go_to_step)-1][0] != self.steps.current:
            #If turbineID would be skipped
            turbineID_step = list(self.get_form_list().keys()).index("turbineID")
            if int(go_to_step) > turbineID_step and self.get_cleaned_data_for_step("turbineID") == None:
                #Go to turbineID
                self.storage.current_step = list(self.get_form_list().items())[turbineID_step-1][0]
            else:
                self.storage.current_step = list(self.get_form_list().items())[int(go_to_step)-2][0]
        return super(CustomerQuestionnaireEdit, self).render_next_step(form)

    #Overrides render_done method --> entry point for custom features
    def render_done(self, form, **kwargs):
        save_for_later_modal =  self.request.POST.get('save_for_later_modal', None)
        if save_for_later_modal:
            return self.get_progress(self.kwargs['questionnaire_pk'])
        final_forms = OrderedDict()
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            wizard_save_for_later = self.request.POST.get('wizard_save_for_later', None)
            if not wizard_save_for_later:
                if not form_obj.is_valid():
                    return self.render_revalidation_failure(form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj
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
        if self.steps.current in self.turbine_steps:
            data = self.get_cleaned_data_for_step("turbineID")
            turbine_ids = []
            if data is not None:
                for i in range(len(data)):
                    try:
                        turbine_id = data[i]["turbine_id"]
                        if turbine_id == "":
                            turbine_id = "WEA " + str(i+1)
                    except KeyError:
                        turbine_id = "WEA " + str(i+1)
                    turbine_ids.append(turbine_id)
                context.update({'turbine_ids':turbine_ids})
            else:
                context.update({'turbine_ids':[]})
        if self.steps.current in ["turbineID", "inspection", "documentation"]:
            data = self.get_cleaned_data_for_step("base")
            if data is not None:
                scope = data["scope"]
            context.update({'scope':scope})
        if self.steps.current == "inspection":
                data = self.get_cleaned_data_for_step("turbine_model")
                if data is not None:
                    for i in range(len(data)):
                        if data[i] != {} and str(data[i]["turbine_model"]) in ["Senvion MM100","Repower MM82","Repower MM70","Senvion MM92/2050","Senvion MM82/2050","Repower MM82 evo","Repower MM92","Repower MM92 evo"]:
                            try:
                                context["date_blade_bearing_inspection"].append(i+1)
                            except KeyError:
                                context.update({"date_blade_bearing_inspection":[i+1]})
        return context

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def get_step_condition(self, key):
        if key in self.condition_dict:
            return self.condition_dict[key](self)
        else:
            return True

    def get_progress(self):
        steps = []
        questionnaire_steps = REQUIRED_FIELDS["questionnaire"]
        for step in questionnaire_steps:
            key = step[0]
            if self.get_step_condition(key):
                data = self.get_cleaned_data_for_step(key)
                if data != None:
                    for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        if data[field[0]] == None:
                            field_info["status"]= "not processed"
                        elif str(data[field[0]]) == "":
                            field_info["status"]= "not processed"
                        else:
                            field_info["status"]= "processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
                else:
                   for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= "not processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
        customer_questionnaire = CustomerQuestionnaire.objects.get(pk=self.kwargs['questionnaire_pk'])
        turbine_questionnaires = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)
        turbine_questionnaire_steps = REQUIRED_FIELDS["turbine_questionnaire"]
        for step in turbine_questionnaire_steps:
            key = step[0]
            if self.get_step_condition(key):
                data_turbines = self.get_cleaned_data_for_step(key)
                #Every turbine has to be processed to get a checkmark
                #If turbine_steps visited
                if data_turbines != None:
                    for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= ""
                        for idx, data in enumerate(data_turbines):
                            if data == {} or data[field[0]] == None or str(data[field[0]]) == "":
                                if field_info["status"] == "" or field_info["status"] == "not processed":
                                    field_info["status"]= "not processed"
                                    #No Data --> Check Database
                                    if getattr(turbine_questionnaires[idx], field[0]):
                                        field_info["status"]= "partly processed"
                                else:
                                    field_info["status"]= "partly processed"
                            else:
                                if field_info["status"] == "" or field_info["status"] == "processed":
                                    field_info["status"]= "processed"
                                else:
                                    field_info["status"]= "partly processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
                #Turbine_steps not visited --> Check Database
                else:
                   for field in step[1:]:
                        field_info = {}
                        field_info["name"] = field[1]
                        field_info["status"]= ""
                        for turbine_questionnaire in turbine_questionnaires:
                            if getattr(turbine_questionnaire, field[0]):
                                if field_info["status"] == "" or field_info["status"] == "processed":
                                    field_info["status"]= "processed"
                                else:
                                    field_info["status"]= "partly processed"
                            else:
                                if field_info["status"] == "" or field_info["status"] == "not processed":
                                    field_info["status"]= "not processed"
                                else:
                                    field_info["status"]= "partly processed"
                        field_info["page"] = list(self.get_form_list().keys()).index(key)+1
                        steps.append(field_info)
        html = render_to_string('projects/customer_questionnaire/questionnaire_progress.html', {'steps': steps})
        return HttpResponse(html)

    def done(self, form_list, form_dict, **kwargs):
        customer_questionnaire = CustomerQuestionnaire.objects.get(pk=self.kwargs['questionnaire_pk'])
        turbine_ids = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire).values_list('id', flat=True)

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
                        t_object = Turbine_CustomerQuestionnaire.objects.get(id=turbine_ids[turbine_count])
                        for field in turbine_form:
                            if not field.name == "id":
                                if t_object._meta.get_field(field.name).null and field.value() == "":
                                    t_object.__dict__[field.name] = None
                                elif field.name in ["manufacturer", "turbine_model"]:
                                    t_object.__dict__[field.name+"_id"] = field.value()
                                elif field.name in ["tower_type"]:
                                    setattr(t_object, field.name, field.value())
                                else:
                                    t_object.__dict__[field.name] = field.value()
                        t_object.save()
                        turbine_count += 1
        customer_questionnaire.save()
        return HttpResponseRedirect(reverse_lazy('projects:customer_view'))

def export_pdf(request, questionnaire_pk):
    customer_questionnaire = get_object_or_404(CustomerQuestionnaire, id=questionnaire_pk)
    turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)

    html_string = render_to_string('projects/customer_questionnaire/export_pdf.html', {'customer_questionnaire': customer_questionnaire, 'turbines': turbines.all(),})
    result = HTML(string=html_string).write_pdf()

    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=CustomerQuestionnaire.pdf'
    return response

def download_questionnaire_files(request, questionnaire_pk):
    customer_questionnaire = get_object_or_404(CustomerQuestionnaire, id=questionnaire_pk)
    turbines = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=customer_questionnaire)

    roadmap = customer_questionnaire.roadmap
    roadmap_submitted = roadmap.name

    single_line_diagram = customer_questionnaire.single_line_diagram
    single_line_diagram_submitted = single_line_diagram.name

    expert_reports = []
    for turbine in turbines:
        if turbine.expert_report.name:
            expert_reports.append(turbine.expert_report)
    expert_reports_submitted = len(expert_reports)

    if roadmap_submitted or single_line_diagram_submitted or expert_reports_submitted:

        file_name = customer_questionnaire.contact_company + '_' + customer_questionnaire.wind_farm_name + '.zip'
        file_name = file_name.replace(' ', '_')

        zip_file_path = os.path.join(settings.MEDIA_ROOT, 'customer_questionnaire/zip_files/' , file_name)
        with ZipFile(zip_file_path, 'w') as zip_file:
            if roadmap_submitted:
                zip_file.write(roadmap.path, arcname=roadmap.name)
            if single_line_diagram_submitted:
                zip_file.write(single_line_diagram.path, arcname=single_line_diagram.name)
            for expert_report in expert_reports:
                zip_file.write(expert_report.path, arcname=expert_report.name)

        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file, content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(zip_file_path)
            return response
    else:
        messages.info(request, _('No files to download attached to this customer questionnaire.'))
        return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))
    raise Http404

def transfer_contact(request, questionnaire_pk):
    messages.success(request, _('Questionnaire transferred successfully.'))
    return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))

def transfer_turbines(request, questionnaire_pk):
    return HttpResponseRedirect(reverse_lazy('projects:customer_questionnaire'))