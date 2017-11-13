# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'

from django.shortcuts import render, HttpResponseRedirect
from app.models import tbPersons, tbTelephones
from django.http import HttpResponse
import time
import json

from common_func import FormatPhonesNum

def start (request):
    # Показывает стртаничку с контактой информацией
    template = "start.html" # шаблон для подгузки
    response = render (request, template, {})
    return response


def avaho (request):
    # Показывает стртаничку с контактой информацией
    template = "avaho.html" # шаблон для подгузки
    response = render (request, template, {})
    return response


def x5( request ):
    """░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░
    :param request: request
    :return: response

    :ТЕХНИЧЕСКИЙ ДОЛГ: пока нет
    ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░"""
    tStart = time.clock()
    msg = u""
    template = "x5.html"
    dimension_to_template = {}

    # iTotalContact = tbContacts.objects.count()
    q = tbPersons.objects.raw('SELECT'
                              '  MAX(app_tbcontacts.id) AS id '
                              'FROM app_tbcontacts;')
    dimension_to_template.update({'MAX_CONTACT_ID': list(q)[0].id})
    # FOR_TEST: создает базу телефонов
    # qsCountacts = tbContacts.objects.all()
    # from random import randint
    # for Contact in qsCountacts:
    #     if not tbTelephones.objects.filter(kContacts__id=Contact.id).count() > 0:
    #         n = randint(0, 4)
    #         for i in range(0, n):
    #             Telephone = "+%01d(%03d)%03d-%02d-%02d" % (randint(1,9),
    #                                                        randint(0,999),
    #                                                        randint(100,999),
    #                                                        randint(0,99),
    #                                                        randint(0,99))
    #             AddTelephone = tbTelephones(szTelephoneNumber=Telephone, kContacts=Contact)
    #             AddTelephone.save()

    # проверяем какой JS с картами и PieCharts: упакованные или нет.

    dimension_to_template.update({'ticks': float(time.clock()-tStart)})
    response = render (request, template, dimension_to_template)
    return response


def getPersonContact (request, ContactID=1):
    """░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░
    :param request: request
    :return: response

    :ТЕХНИЧЕСКИЙ ДОЛГ: пока нет
    ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░ ░▒▓█▓▒░"""
    tStart = time.clock()
    jsonResponse = {}
    try:
        ContactID = int(ContactID)
    except:
        return HttpResponseRedirect("/")
    q = tbTelephones.objects.raw("SELECT"
                                 "  app_tbtelephones.szTelephoneNumber,"
                                 "  app_tbcontacts.* "
                                 "FROM app_tbtelephones"
                                 "   RIGHT OUTER JOIN app_tbcontacts"
                                 "    ON app_tbtelephones.kContacts_id = app_tbcontacts.id "
                                 "WHERE app_tbcontacts.id = %d;" % ContactID)
    ContactInfo = list(q)
    if len(ContactInfo) == 0:
        jsonResponse = {
            "success": False,
            "code": "no SQL-entry",
            "id": ContactID,
            "person": None,
            "phones": None
        }
    else:
        listPhones = []
        for i in ContactInfo:
            if i.szTelephoneNumber != None:
                listPhones.append(FormatPhonesNum(i.szTelephoneNumber))
        listPhones.sort()
        jsonResponse = {
            "success": True,
            "code": "Ok",
            "id": ContactID,
            "person": ContactInfo[0].szPersonBigName,
            "phones": listPhones
        }
    template = "start.html"
    dimension_to_template = {}
    return HttpResponse ( json.dumps(jsonResponse, separators=(",",":"), encoding="utf-8", ensure_ascii=False) )