# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'

from django.contrib import admin
from app.models import tbContacts, tbTelephones

class ContactsAdmin (admin.ModelAdmin):
    search_fields = ['szPersonBigName', 'szParsonAdress']
    list_display = ('szPersonBigName', 'id', 'szParsonAdress' )
admin.site.register(tbContacts, ContactsAdmin)


class TelephonesAdmin (admin.ModelAdmin):
    search_fields = ['kContacts', 'szTelephoneNumber']
    list_display = ('kContacts', 'kContacts' )
admin.site.register(tbTelephones, TelephonesAdmin)