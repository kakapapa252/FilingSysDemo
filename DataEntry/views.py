from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse
from .models import (
    Person,
    PersonType,
    Case,
    CaseType,
    CasePersonRelation
)


def home(request):
    cases = Case.objects.all().order_by('caseNumber')
    return render(request, "home.html", context={'cases': cases})


def file(request, id):
    context_dict = {}

    case = Case.objects.get(caseNumber=id)
    context_dict['caseTitle'] = case.caseTitle.upper()
    context_dict['tentDate'] = case.caseTentDate
    context_dict['filingDate'] = case.caseFilingDate
    context_dict['caseType'] = case.caseType.name
    context_dict['caseNumber'] = case.caseNumber

    casePersons = CasePersonRelation.objects.filter(
        case=case).order_by('typeNumber')

    p_types = PersonType.objects.filter(
        name__in=["Petitioner", "Appellant", "Plaintiff"])
    d_types = PersonType.objects.filter(name__in=["Respondent", "Defendant"])
    c_types = PersonType.objects.filter(name__in=["Client"])
    a_types = PersonType.objects.filter(name__in=["Advocate"])

    p_persons = []
    d_persons = []
    c_persons = []
    a_persons = []
    first_p = None
    first_p_type = None
    first_d = None
    first_d_type = None

    for personRelation in casePersons:
        if personRelation.personType in p_types:
            p_persons.append((personRelation.person, personRelation))
            if personRelation.typeNumber == 1:
                first_p = personRelation.person
                first_p_type = personRelation.personType.name
        if personRelation.personType in d_types:
            d_persons.append((personRelation.person, personRelation))
            if personRelation.typeNumber == 1:
                first_d = personRelation.person
                first_d_type = personRelation.personType.name
        if personRelation.personType in c_types:
            c_persons.append((personRelation.person, personRelation))
        if personRelation.personType in a_types:
            a_persons.append((personRelation.person, personRelation))

    context_dict['petitionerOne'] = first_p
    context_dict['petitionerOneType'] = first_p_type
    context_dict['defendantOne'] = first_d
    context_dict['defendantOneType'] = first_d_type

    context_dict['petitionerList'] = p_persons
    context_dict['defendantList'] = d_persons
    context_dict['clientList'] = c_persons
    context_dict['advocateList'] = a_persons
    print(a_persons)

    return render(request, "OutputFile.html", context=context_dict)
