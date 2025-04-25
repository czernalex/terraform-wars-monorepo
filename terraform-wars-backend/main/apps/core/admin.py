from unfold.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
