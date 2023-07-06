from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
# Register your models here.
from leads.models import Leads

admin.site.register(Leads)

from django.shortcuts import render
from django import forms

# create a form field which can input a file
# class CsvImportForm(forms.Form):
#     csv_file = forms.FileField()
#
# @admin.register(models.Leads)
# class LeadsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
#     list_display = ("name","contact","email","country","industry","status")
#
#     def import_action(self,request):
#         form = CsvImportForm()
#         context = {"form": form, "form_title": "Upload csv file.",
#                     "description": "The file should have following headers: "
#                                     "[NAME,CONTACT,EMAIL,COUNTRY,INDUSTRY,STATUS]."
#                                     " The Following rows should contain information for the same.",
#                                     "endpoint": "/admin/starwars/characters/import/"}
#         return render(
#             request, "admin/import_starwars_characters.html", context
#         )

