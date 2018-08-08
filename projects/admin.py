from django.contrib import admin
from .models import Project, Comment
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
    #mw = Field(column_name='MW')
    commisioning = Field(column_name='Commisioning')
    #age = Field(column_name='Age WTG')
    country = Field(column_name='Country')
    #place = Field(column_name='Place')
    #postal_code = Field(column_name='Postcode')
    #new_customer = Field(column_name='New Customer')
    owner = Field(column_name='Operator')
    customer__name = Field(attribute='customer__name', column_name='Customer')
    #customer_contact__name = Field(attribute='customer_contact__name', column_name='Contact Person')
    #customer_contact__mail = Field(attribute='customer_contact__mail', column_name='Mail')
    #customer_contact__phone = Field(attribute='customer_contact__phone', column_name='Phone')
    #last_contact = Field(attribute='last_contact', column_name='Last Contact')
    contract_type = Field(attribute='contract_type', column_name='Contract Type')
    run_time = Field(attribute='run_time', column_name='Run-Time')
    #department = Field(attribute='department', column_name='Department')
    #request_date = Field(attribute='request_date', column_name='Date of request')
    start_operation = Field(attribute='start_operation', column_name='Start Operations')
    price = Field(attribute='price', column_name='Price/WTG/a')
    ebt = Field(attribute='ebt', column_name='EBT')
    yearly_contract_value = Field(column_name='Contract Volume/a')
    #total_contract_value = Field(column_name='Total Contract Value')
    contract_signature = Field(attribute='contract_signature', column_name='Contract Signature')
    responsible = Field(attribute='responsible', column_name='Sales Manager')
    comments = Field(column_name="next step / bottleneck / comment")

    class Meta:
        model = Project
        fields = ('dwt', 'country', 'name', 'customer__name', 'owner', 'manufacturer', 'wtg_type', 'amount_turbines', 'commisioning', 'contract_type', 'run_time', 'price', 'yearly_contract_value', 'ebt', 'contract_signature', 'start_operation', 'status', 'prob', 'responsible', 'comments') #'last_contact', 'department', 'request_date', 'mw', 'age', 'place', 'postal_code', 'new_customer', 'customer_contact__name', 'customer_contact__mail', 'customer_contact__phone', 'total_contract_value'
        export_order = ('dwt', 'country', 'name', 'customer__name', 'owner', 'manufacturer', 'wtg_type', 'amount_turbines', 'commisioning', 'contract_type', 'run_time', 'price', 'yearly_contract_value', 'ebt', 'contract_signature', 'start_operation', 'status', 'prob', 'responsible', 'comments') #'last_contact', 'department', 'request_date', 'mw', 'age', 'place', 'postal_code', 'new_customer', 'customer_contact__name', 'customer_contact__mail', 'customer_contact__phone', 'total_contract_value'

    def dehydrate_manufacturer(self, project):
        return project.project_oem_name()

    def dehydrate_wtg_type(self, project):
        return project.project_wec_types_name()

    def dehydrate_amount_turbines(self, project):
        return project.amount_turbines()

    def dehydrate_mw(self, project):
        return project.mw()

    def dehydrate_commisioning(self, project):
        return project.first_commisioning()

    def dehydrate_age(self, project):
        return project.turbine_age()

    def dehydrate_country(self, project):
        return project.project_country()

    def dehydrate_place(self, project):
        return project.project_city()

    def dehydrate_postal_code(self, project):
        return project.project_postal()

    def dehydrate_owner(self, project):
        return project.project_owner_name()

    def dehydrate_total_contract_value(self, project):
        return project.total_contract_value()

    def dehydrate_yearly_contract_value(self, project):
        return project.yearly_contract_value()

    def dehydrate_comments(self, project):
        return project.all_comments()

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

    list_display = ['id', 'available', 'created']
    list_editable = ['available']
    list_filter = ['available']
    search_fields = ('text',)
admin.site.register(Comment, CommentAdmin)