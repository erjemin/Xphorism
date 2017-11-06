# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'
from django.shortcuts import render, HttpResponseRedirect
from app.models import tbContacts, tbTelephones
from django.http import HttpResponse
import time
import re
import json

def FormatPhonesNum (szPhoneNum = u"0"):
    szPhoneNum = str(szPhoneNum)
    szPhoneNum = re.sub(r"[^0-9]", u"", szPhoneNum)
    if len(szPhoneNum) == 0: szPhoneNum = u"0"
    szPhoneNum = "%011d" % int(szPhoneNum)
    return"+%s(%s)%s-%s-%s" % (szPhoneNum[0],
                               szPhoneNum[1:4],
                               szPhoneNum[4:7],
                               szPhoneNum[7:9],
                               szPhoneNum[9:11])