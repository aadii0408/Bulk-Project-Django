import csv
import json
import math

from django.contrib.sites import requests
from django.http import HttpResponse, response, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from . import forms, models
from django.contrib import messages
from django.http import JsonResponse
from .forms import AddRecordForm
import csv
from .models import Leads
import pandas as pd


# Create your views here.
@login_required(login_url='login')
def home(request):
    records = Leads.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('base')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('base')
    else:
        return render(request, 'base.html')


# @login_required(login_url='login')
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, "Yaayy!, You Have Successfully Registered! Welcome!")
            return redirect('login')

    return render(request, 'signup.html')


# @login_required(login_url='login')
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Thank You. You Have Been Logged In!")
            return redirect('base')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    data = Leads.objects.all()
    active = Leads.objects.filter(status="Active Leads").count()
    dead = Leads.objects.filter(status="Dead Leads").count()
    response = {

        "active": active,
        "dead": dead,
        "data": data

    }
    print(response)
    return render(request, 'dashboard.html',response)

# @login_required(login_url='login')
# def status(request):
#     # data = Leads.objects.all()
#     count = Leads.objects.all().count()
#     context = {'count': count }
#     return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def imp(request):

    # Return the list of dictionaries
    return render(request, 'import.html', {'data': None})
    # return render(requests, 'import.html')


@login_required(login_url='login')
def leads(request):
    data = Leads.objects.filter(is_deleted=False)
    return render(request, 'leads.html',{'data': data})





def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('base')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('base')





def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Leads.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('base')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('base')


@login_required(login_url='login')
def show_csv(request):
    df = pd.read_csv(request.FILES['myFile'].file.name)
    columns = df.columns
    db_fields_list = ["created_at", "first_name", "last_name", "contact", "email", "country", "industry", "status"]
    fields_not_in_csv = []
    fields_in_csv = []
    for i in columns:
        if i not in db_fields_list:
            fields_not_in_csv.append(i)
        else:
            fields_in_csv.append(i)
    dictionary1 = {
            "created_at":[],
            "first_name":[],
            "last_name":[],
            "contact":[],
            "email":[],
            "country":[],
            "industry":[],
            "status":[],
            "skip":[]
        }
    dictList = []
    for index,i in df.iterrows():
        dictionary = {
            "created_at":[],
            "first_name":[],
            "last_name":[],
            "contact":[],
            "email":[],
            "country":[],
            "industry":[],
            "status":[],
            "skip":[],
        }
        for j in fields_in_csv:
            # print(i['first_name'])
            if i[j]==math.nan:
                dictionary[j].append('')
                dictionary1[j].append('')
            else:
                dictionary[j].append(str(i[j]))
                dictionary1[j].append(str(i[j]))
            # print(dictionary)
        for j in fields_not_in_csv:
            dictionary["skip"].append(str(i[j]))
            dictionary1["skip"].append(str(i[j]))
        # lead = Leads.objects.create(
        #     created_at=dictionary['created_at'][0],
        #     first_name=dictionary['first_name'][0],
        #     last_name=dictionary['last_name'][0],
        #     contact=dictionary['contact'][0],
        #     email=dictionary['email'][0],
        #     country=dictionary['country'][0],
        #     industry=dictionary['industry'][0],
        #     status=dictionary['status'][0]
        # )
        dictList.append(dictionary)
    dictionary1['created_at'] = ", ".join(dictionary1['created_at'])
    dictionary1['first_name'] = ", ".join(dictionary1['first_name'])
    dictionary1['last_name'] = ", ".join(dictionary1['last_name'])
    dictionary1['contact'] = ", ".join(dictionary1['contact'])
    dictionary1['email'] = ", ".join(dictionary1['email'])
    dictionary1['country'] = ", ".join(dictionary1['country'])
    dictionary1['industry'] = ", ".join(dictionary1['industry'])
    dictionary1['status'] = ", ".join(dictionary1['status'])
    dictionary1['skip'] = ", ".join(dictionary1['skip'])


    # with open(request.FILES['myFile'].file.name, 'r') as csvfile:
    #     # Create a `csv.reader` object for the CSV file.


    #     # Iterate over the `csv.reader` object to read the data from the CSV file.
    #     data = []
    #     # print(reader)
    #     db_fields_list = ["Id", "created_at", "first_name", "last_name", "contact", "email", "country", "industry",
    #                       "status"]
    #     fields_not_in_csv = []
    #     # x = csvfile.readlines()[1]
    #     # print(x)

    #     # for row in reader:
    #     #     print(row)
    #     # for field in row:
    #     #     if not row[field] in db_fields_list:
    #     #         fields_not_in_csv.append(field)
    #     # print(Leads.objects.all())
    #     index = 0
    #     for row in reader:
    #         if index > 0:
    #             Leads.objects.create(
    #                 created_at=row[0],
    #                 first_name=row[1],
    #                 last_name=row[2],
    #                 contact=row[3],
    #                 email=row[4],
    #                 country=row[5],
    #                 industry=row[6],
    #                 status=row[7]
    #             )
    #             data.append(row)
    #         index = index + 1
    #         # print(data)
    #     # Leads.objects.get()

    #     data = Leads.objects.all()
    #     li=list(range(0,8))
    return render(request, 'show.html', {'data': dictList, 'data1': dictionary1, 'columns':dictionary.keys()})
        # context = {}
        # code to query the database goes here!

        # add data to context
        # context["leads"] = Leads.objects.all()
        # return render(request, 'show.html', context)

    # return render(request, 'show.html' , {'leads':lead})

    #     return data
@csrf_exempt
@login_required(login_url='login')
def delete(request):
    if request.method == 'POST':
        for i in request.POST.getlist('ids[]'):
            lead = Leads.objects.get(id=i)
            lead.is_deleted = True
            lead.save()
        return JsonResponse({"message":"Leads Deleted Successfully"})
    else:
        return redirect('base')

@csrf_exempt
@login_required(login_url='login')
def csvSave(request):
    if request.method == 'POST':
        columns = ['createdAt', 'firstName', 'lastName', 'contact', 'email', 'country', 'industry', 'status', 'skip']
        csvColumns = list(json.loads(request.POST.get('data')).keys())
        for i in columns:
            if i not in csvColumns:
                return HttpResponse(f"{i} does not Exist !!",status=400)
        data = json.loads(request.POST.get('data'))
        for i in range(0,len(data['createdAt'].split(", "))):
            Leads.objects.create(
                created_at=data['createdAt'].split(", ")[i],
                first_name=data['firstName'].split(", ")[i],
                last_name=data['lastName'].split(", ")[i],
                contact=data['contact'].split(", ")[i],
                email=data['email'].split(", ")[i],
                country=data['country'].split(", ")[i],
                industry=data['industry'].split(", ")[i],
                status=data['status'].split(", ")[i]
            )            
        return HttpResponse("Data Saved Successfully")
    else:
        return redirect('base')
