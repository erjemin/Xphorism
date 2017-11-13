# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'

from django.contrib import admin
from app.models import tbPersons, tbTelephones

class ContactsAdmin (admin.ModelAdmin):
    search_fields = ['szPersonName', 'szParsonAdress']
    list_display = ('szPersonName', 'id', 'szParsonAdress' )
admin.site.register(tbPersons, ContactsAdmin)


class TelephonesAdmin (admin.ModelAdmin):
    search_fields = ['kContacts', 'szTelephoneNumber']
    list_display = ('kContacts', 'kContacts' )
admin.site.register(tbTelephones, TelephonesAdmin)