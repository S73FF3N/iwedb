from django.contrib import admin
from .models import Project, Comment, Technologieverantwortlicher, Calculation_Tool, OfferNumber
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from import_export.fields import Field

class ProjectRessources(resources.ModelResource):
    name = Field(attribute='name', column_name='Project')
    dwt = Field(attribute='dwt', column_name='Einheit')
    status = Field(attribute='status', column_name='Status')
    prob = Field(attribute='prob', column_name='Probability')
    manufacturer = Field(column_name='OEM')
    wtg_type = Field(column_name='WTG Type')
    amount_turbines = Field(column_name='Amount WTG')
    commisioning = Field(column_name='Commisioning')
    country = Field(column_name='Country')
    owner = Field(column_name='Operator')
    customer__name = Field(attribute='customer__name', column_name='Customer')
    contract_type = Field(attribute='contract_type', column_name='Contract Type')
    run_time = Field(attribute='run_time', column_name='Run-Time')
    start_operation = Field(attribute='start_operation', column_name='Start Operations')
    price = Field(attribute='price', column_name='Price/WTG/a')
    ebt = Field(attribute='ebt', column_name='EBT')
    yearly_contract_value = Field(column_name='Contract Volume/a')
    contract_signature = Field(attribute='contract_signature', column_name='Contract Signature')
    sales_manager = Field(attribute='sales_manager', column_name='Sales Manager')
    comments = Field(column_name="next step / bottleneck / comment")

    class Meta:
        model = Project
        fields = ('dwt', 'country', 'name', 'customer__name', 'owner', 'manufacturer', 'wtg_type', 'amount_turbines', 'commisioning', 'contract_type', 'run_time', 'price', 'yearly_contract_value', 'ebt', 'contract_signature', 'start_operation', 'status', 'prob', 'sales_manager', 'comments') #'last_contact', 'department', 'request_date', 'new_customer', 'customer_contact__name', 'customer_contact__mail', 'customer_contact__phone', 'total_contract_value'
        export_order = ('dwt', 'country', 'name', 'customer__name', 'owner', 'manufacturer', 'wtg_type', 'amount_turbines', 'commisioning', 'contract_type', 'run_time', 'price', 'yearly_contract_value', 'ebt', 'contract_signature', 'start_operation', 'status', 'prob', 'sales_manager', 'comments') #'last_contact', 'department', 'request_date', 'new_customer', 'customer_contact__name', 'customer_contact__mail', 'customer_contact__phone', 'total_contract_value'

    def dehydrate_manufacturer(self, project):
        return project._project_oem_name()

    def dehydrate_wtg_type(self, project):
        return project._project_wec_types_name()

    def dehydrate_amount_turbines(self, project):
        return project._amount_turbines()

    def dehydrate_commisioning(self, project):
        return project.first_commisioning

    def dehydrate_yearly_contract_value(self, project):
        return project._yearly_contract_value()

    def dehydrate_country(self, project):
        return project._project_country()

    def dehydrate_owner(self, project):
        return project._project_owner_name()

    def dehydrate_comments(self, project):
        return project._all_comments()

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectRessources

    list_display = ['name', 'id', 'available', 'customer', 'created', 'updated']
    list_editable = ['available']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
admin.site.register(Project, ProjectAdmin)

class CommentRessources(resources.ModelResource):
    class Meta:
        model = Comment

class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentRessources

    list_display = ['id', 'text', 'content_type', 'object_id', 'available', 'created', 'created_by']
    list_editable = ['available']
    list_filter = ['available']
    search_fields = ('text',)
admin.site.register(Comment, CommentAdmin)

class TechnologieverantworlicherAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'technology_responsible']
admin.site.register(Technologieverantwortlicher, TechnologieverantworlicherAdmin)

class Calculation_ToolAdmin(admin.ModelAdmin):
    list_display = ['version', 'created']
admin.site.register(Calculation_Tool, Calculation_ToolAdmin)

class OfferNumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'wind_farm', 'amount', 'sales_manager', 'created', 'created_by']
admin.site.register(OfferNumber, OfferNumberAdmin)