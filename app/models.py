# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'

from django.db import models

# Таблица: Контактная информация (ФИО, адрес…)
class tbContacts(models.Model):
    szPersonBigName = models.CharField(
        max_length=100,
        # должно хватать, но возможны инциденты: https://ru.wikipedia.org/wiki/Вольф%2B585_старший
        default=u"—",
        null=False,
        db_index=True,
        unique=True,
        verbose_name=u"ФИО",
        help_text=u"Полоне ФИО персоны.<br /><small><b>Допускается HTML</b>.</small>"
    )
    szParsonAdress = models.CharField(
        max_length=140,
        # должно хватать. На сегодя самый длинный адрес в России -- 138 символов.
        default=u"—",
        null=False,
        db_index=False,
        unique=False,
        verbose_name=u"Адрес",
        help_text=u"Адрес проживания персоны."
    )
    # dtContactCreate = models.DateTimeField(
    #     auto_now_add=True,
    #     db_index=False,
    #     verbose_name=u"Создано"
    # )
    # dtContactModify = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name=u"Отредактированно"
    # )

    def __unicode__(self):
        return u'%04d: %s' % (self.id, self.szPersonBigName )

    class Meta:
        verbose_name = u"Контактная информация (ФИО, адрес…)"
        verbose_name_plural = u"Контактная информация (ФИО, адрес…)"
        ordering = ['szPersonBigName']


# Таблица: телефонные номера
class tbTelephones(models.Model):
    szTelephoneNumber = models.CharField(
        max_length=20,
        default=u"+9(999)999-99-99",
        verbose_name=u"Тел.",
        help_text=u"Номер телефона.<br /><small>Учитываются только цифры, <b>все нецифровые символы при выводе будут удалены</b>. Увы.</small>"
    )
    kContacts = models.ForeignKey(
        'tbContacts',
        null=True,
        db_constraint = False,
        on_delete=models.SET_NULL,
        verbose_name=u"Контактёр",
        help_text=u"Узазать, какой персоне принадлежит этот телефон."
    )
    # dtTelephoneCreate = models.DateTimeField(
    #     auto_now_add=True,
    #     db_index=False,
    #     verbose_name=u"Создано"
    # )
    # dtTelephoneModify = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name=u"Отредактированно"
    # )

    def __unicode__(self):
        return u'%04d: %s' % (self.id, self.szTelephoneNumber )

    class Meta:
        verbose_name = u"Телефонный номер"
        verbose_name_plural = u"Телефонные номера"
        # ordering = ['kContacts']
