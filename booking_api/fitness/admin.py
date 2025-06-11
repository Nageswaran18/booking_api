from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config("fitness").get_models()

for model in app_models:
    class GenericAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]
        search_fields = [field.name for field in model._meta.fields if field.get_internal_type() in ["CharField", "TextField"]]  
        list_filter = [field.name for field in model._meta.fields if field.get_internal_type() in ["BooleanField", "DateField", "DateTimeField", "ForeignKey"]]  

    admin.site.register(model, GenericAdmin)
