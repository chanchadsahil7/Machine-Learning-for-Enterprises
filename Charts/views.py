from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .reports import *
import json
import os
import pandas as pd
from .reports import *

# from django.template.context import RequestContext
data = {}

def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)

    return render(request, 'login.html')


@login_required(login_url='/plots/')
def home(request):
    if request.user.email.split('@')[1]=="solivarlabs.com":
        return render_to_response('home.html',{'user':request.user.get_full_name})
    else:
        print(request.user.email.split('@')[1])
        logout(request)
        return render_to_response('error_login.html',{})

@login_required(login_url="/plots/")
def super_user(request):
    global data
    companies={
        1:['a','a.jpg'],
        2:['b','b.jpg'],
        3:['c','c.jpg'],
        4:['d','d.jpg']
    }
    total_users={
        1:['1@gmail.com','a',1],
        2:['2@gmail.com','b',2],
        3:['3@gmail.com','c',1],
        4:['2@gmail.com','d',2],
        5:['5@gmail.com','a',1],
        6:['6@gmail.com','b',2],
        7:['7@gmail.com','c',1],
        8:['8@gmail.com','d',2],
        9:['9@gmail.com','a',1],
        10:['10@gmail.com','b',2],
        11:['11@gmail.com','c',1],
        12:['12@gmail.com','d',2],
        13:['13@gmail.com','a',1]
    }
    if request.method=="POST":
        if request.POST['company']:
            company=request.POST['company']
            admins={}
            users={}
            for i in total_users:
                if total_users[i][2]=='c' and total_users[i][3]==int(company):
                    admins[i]=total_users[i]
                    print(admins[i])
                elif total_users[i][2]=='a' and total_users[i][3]==int(company):
                    users[i]=total_users[i]
                    print(users[i])
            data = {'admins':admins,'users':users}
            return JsonResponse(data)
    return render_to_response('superuser.html',{'companies':companies})

def superadmin_data(request):
    company_name = request.GET.get("company",None)
    data_filtered = filter_data(company_name)
    print(data_filtered)
    response = JsonResponse({'data':data_filtered})
    return response

def logout(request):
    auth_logout(request)
    return redirect('/plots/')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(os.path.curdir + "\\Charts\\" + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        header = get_header(os.path.curdir + "\\Charts\\" + myfile.name)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
        })
    return render(request, 'upload.html')