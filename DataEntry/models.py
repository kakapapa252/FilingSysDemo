from unicodedata import category
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime


# Create your models here.


class PersonType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return (self.name)


class CaseType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return (self.name)


class Case(models.Model):
    id = models.AutoField(primary_key=True)
    caseNumber = models.PositiveIntegerField(
        null=False, blank=False, default=0)
    caseTitle = models.CharField(max_length=200, blank=False, null=False)
    caseType = models.ForeignKey(
        CaseType, on_delete=models.DO_NOTHING, default=None, null=True)
    caseTentDate = models.DateField(
        _("Tent Date"), null=True, default=None, auto_now_add=False, auto_now=False)
    caseFilingDate = models.DateField(
        _("Filing Date"), null=True, default=None, auto_now_add=False, auto_now=False)

    def __str__(self):
        return (str(self.caseNumber) + " " + str(self.caseTitle))


class Person(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200, blank=False, null=False)
    fatherName = models.CharField(max_length=200, blank=False, null=False)
    age = models.PositiveIntegerField(
        null=False, blank=False, default=0)
    address = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(_("email address"), blank=False, null=False)

    def __str__(self):
        return (self.name)


class CasePersonRelation(models.Model):
    id = models.AutoField(primary_key=True)

    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    personType = models.ForeignKey(PersonType, on_delete=models.DO_NOTHING)
    typeNumber = models.PositiveIntegerField(
        null=False, blank=False, default=0)

    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING)

    def __str__(self):
        return (self.person.name) + " Case: " + str(self.case.caseNumber)
