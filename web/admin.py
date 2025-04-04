from django.contrib             import admin
from django.forms.models        import modelform_factory
from django.utils.translation   import gettext_lazy as _
from django.forms               import widgets
from django.utils.safestring    import mark_safe
from django.db                  import models

# Imports for Dynamic app registrations
from django.apps            import apps

# Unfold 
from unfold.admin                       import ModelAdmin, TabularInline, StackedInline
from import_export.admin                import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from django.utils.translation           import gettext_lazy as _



# Common Model
try:
    from .models import CommonModel
    COMMON_MODEL_AVAILABLE = True
except ImportError:
    COMMON_MODEL_AVAILABLE = False


# CONFIG CONSTANTS
admin.site.site_header  = 'WOLFx Admin'
exempt                  = [] # modelname in this list will not be registered
global_app_name         = 'web' # Replace '' with your app name




# Json Editor Widget
# https://github.com/json-editor/json-editor
class JsonEditorWidget(widgets.Widget):
    template_name = 'json_editor_widget.html'

    def __init__(self, schema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = schema

    def render(self, name, value, attrs=None, renderer=None):
        # Convert Python dictionary to JSON string
        json_value = value if value else '{}'
        # Render the JSON Editor
        style = '''
        .form-row {
            overflow: visible !important;
        }
        .je-switcher{
            margin-left: 0px !important;
        }
        .je-ready button{
            padding: 5px 10px !important;
            border: 1px solid grey !important;
        }
        .je-ready button i{
            margin-right: 5px !important;
            margin-left: 5px !important;
        }
        .je-indented-panel{
            border-radius: 0px !important;
            padding: 20px 15px !important;
        }
        '''
        return mark_safe(f'''

            <!-- FontAwesome CSS -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

            <!-- JSON Editor CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.css">

            <!-- JSON Editor JS -->
            <script src="https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js"></script>

            <style>{style}</style>
            <script src="https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js"></script>
            <textarea name="{name}" id="tx_{attrs['id']}" style="display:none;">{json_value}</textarea>
            <div id="editor_{attrs['id']}"></div>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    var editor = new JSONEditor(document.getElementById("editor_{attrs['id']}"), {{
                        schema: {self.schema},
                        startval: {json_value},
                        theme: 'html',
                        iconlib: 'fontawesome5',
                    }});
                    editor.on('change', function() {{
                        console.log("Change event triggered");
                        console.log("Editor Value:", editor.getValue());
                        document.getElementById("tx_{attrs['id']}").value = JSON.stringify(editor.getValue());
                    }});
                }});
            </script>
        ''')


class GenericStackedAdmin(TabularInline):
    extra = 1
    tab = True
    
    # This method ensures the field order is correct for inlines as well
    def get_formset(self, request, obj=None, **kwargs):
        formset         = super().get_formset(request, obj, **kwargs)
        form            = formset.form
        # custom_order    = [field for field in form.base_fields]
        
        if COMMON_MODEL_AVAILABLE:
            exempt_common_model_fields = [field.column for field in CommonModel._meta.fields]
            custom_order = [field for field in form.base_fields if field not in exempt_common_model_fields]
            # custom_order += [field for field in CommonModel._meta.fields if field in form.base_fields]
        
        form.base_fields = {field: form.base_fields[field] for field in custom_order}
        return formset


class GenericAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    def __init__(self, model, admin_site):
        self.model = model
        self.inlines = []
        self.actions = []
        self.admin_meta = getattr(model, 'admin_meta', {})

        # Dynamic admin meta from model
        # Specify a static dictionary in model
        try:
            # Admin Meta
            if model.admin_meta:
                for k,v in model.admin_meta.items():
                    self.__setattr__(k,v)
        except:
            pass
        
        # Dynamic Actions from model
        # Specify a key 'actions' in the admin_meta dictionary in model
        try:
            if 'actions' in model.admin_meta:
                for action_name in model.admin_meta['actions']:
                    # Ensure action_name is a string
                    if isinstance(action_name, str):
                        action_function = getattr(model, action_name, None)
                        if callable(action_function):
                            self.add_action(action_function, action_name)
        except Exception as e:
            # Handle or log the exception
            pass
        
        # Register Inlines
        self.register_inlines()  

        super().__init__(model, admin_site)
        
    # Function to get the fieldsets
    def get_fieldsets(self, request, obj=None):
        if 'fieldsets' in self.admin_meta:
            return self.admin_meta['fieldsets']

        common_fields = []
        try:
            if issubclass(self.model, CommonModel):
                common_fields = [field.name for field in CommonModel._meta.fields if field.editable]
        except:
            common_fields = []

        other_fields    = [field.name for field in self.model._meta.fields if field.name not in common_fields and field.editable and field.name != 'id']
        m2m_fields      = [field.name for field in self.model._meta.many_to_many]
        other_fields    += m2m_fields

        fieldsets = [
            (self.model._meta.verbose_name.title(), {
                "classes": ["tab"],
                'fields': other_fields,
            })
        ]

        if common_fields:
            fieldsets.append(
                (_("Meta Data"), {
                    "classes": ["tab"],
                    'fields': common_fields,
                })
            )

        return fieldsets
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # Check if the field is a JSONField
        if isinstance(db_field, models.JSONField) and self.admin_meta:
            # Retrieve the schema configuration for JSON fields
            json_fields_meta = self.model.admin_meta.get('json_fields', {})

            # Retrieve the schema for the specific field, if defined
            json_schema = json_fields_meta.get(db_field.name, {}).get('schema')

            if json_schema:
                # Initialize the custom widget with the specified schema
                kwargs['widget'] = JsonEditorWidget(schema=json_schema)
            # else:                                                                                         # Patch this later
            #     # Else load the django-jsoneditor widget 
            #     kwargs['widget'] = JSONEditor()

        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def get_readonly_fields(self, request, obj=None):
        # Get a list of non-editable fields
        readonly_fields = [field.name for field in self.model._meta.fields if (not field.editable or field.name == 'id')]

        return readonly_fields
    
    # Function to add actions to the admin class
    def add_action(self, action_function, action_name):
        def wrapper_action(modeladmin, request, queryset):
            for obj in queryset:
                action_method = getattr(obj, action_name)
                if callable(action_method):
                    action_method(request)

        wrapper_action.__name__ = f'admin_action_{action_name}'  # Change the name
        wrapper_action.short_description = action_name.replace('_', ' ').title()

        if not hasattr(self, 'actions') or not self.actions:
            self.actions = [wrapper_action]
        else:
            # Prevent re-adding the same action
            if wrapper_action not in self.actions:
                self.actions.append(wrapper_action)
        
        self.__dict__[wrapper_action.__name__] = wrapper_action
    
    def register_inlines(self):
        if hasattr(self.model, 'admin_meta') and 'inline' in self.model.admin_meta:
            for inline_info in self.model.admin_meta['inline']:
                for related_model, fk_name in inline_info.items():
                    self.add_inline(related_model, fk_name)

    def add_inline(self, related_model_name, fk_name):
        related_model = apps.get_model(app_label=global_app_name, model_name=related_model_name)  # Replace 'your_app_name'
        inline_class_name = f"{related_model.__name__}Inline"
        
        class_attrs = {
            'model'     : related_model,
            'fk_name'   : fk_name,
            'form'      : modelform_factory(related_model, exclude=[]),
        }

        InlineAdminClass = type(inline_class_name, (GenericStackedAdmin,), class_attrs)
        self.inlines.append(InlineAdminClass)

    # Custom Media so that we can add custom js files
    class Media:
        js = ('https://code.jquery.com/jquery-3.7.0.js', )


app = apps.get_app_config(global_app_name)
for model_name, model in app.models.items():
    # If model_name consists history
    if model_name not in exempt and 'histor' not in model_name.lower():
        # print(model_name + ' '  + str(model))
        admin.site.register(model, GenericAdmin)
    
