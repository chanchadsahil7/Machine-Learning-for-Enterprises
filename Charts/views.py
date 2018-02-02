from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from Charts import reports
import json
import os
data = {}

def is_admin(email):
    return reports.check_is_admin(email)

def login(request):
    return render(request, 'login.html')

@login_required(login_url="/plots/")
def dashboard(request):
    return render_to_response('index.html', {'user':request.user.get_full_name})

@login_required(login_url="/plots/")
def data_cleaning(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode(encoding='UTF-8'))
        filename = data['filename']
        metrics = data['metrics']
        metrics_data = reports.get_numerical_metrics(filename,metrics)
        return HttpResponse(json.dumps(metrics_data))

@login_required(login_url="/plots/")
def home(request):
    if is_admin(request.user.email):
        return render_to_response('index.html',{'user':request.user.get_full_name})
    else:
        logout(request)
        return render_to_response('error_login.html',{})

@login_required(login_url="/plots/")
def gen_charts(request):
    if request.method=="POST":
        data = json.loads(request.body.decode(encoding='UTF-8'))
        tablename = data['tablename']
        data.pop('tablename')
        cid = reports.get_cid(request.user.email)
        l = reports.gen_charts(tablename,data,cid)
        return HttpResponse(json.dumps(l))
    else:
        cid = reports.get_cid(request.user.email)
        data = reports.get_filters(cid)
        tablename = data["tablename"]
        data.pop("tablename")
        return render_to_response("charts.html", {"data":data, "tablename":tablename, 'user':request.user.get_full_name})

@login_required(login_url="/plots/")
def remove_user(request):
    data = json.loads(request.body.decode(encoding='UTF-8'))
    print(data)
    reports.remove_user(data['uid'])
    return HttpResponse("hai")

@login_required(login_url="/plots/")
def users(request):
    if request.method == "POST":
        name = request.POST['user_name']
        email = request.POST['user_email']
        reports.add_user(name,email,request.user.email)
    users = reports.get_users(request.user.email)
    return render_to_response("users.html",{'users':users})

@login_required(login_url="/plots/")
def to_charts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode(encoding='UTF-8'))
        filename = data['data2']['filename']
        cleaning_metrics = data['data1']
        dividing_metrics = data['data2']
        cid = reports.get_cid(request.user.email)
        reports.fill_missing_values(filename,cleaning_metrics,dividing_metrics,cid)
        return HttpResponse()

@login_required(login_url="/plots/")
def file_upload(request):
    name = request.user.get_full_name
    if request.method == 'POST' and request.FILES['filename']:
        company_name="company"
        myfile = request.FILES['filename']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(os.path.curdir,"Charts","Data",company_name,myfile.name.lower()), myfile)
        uploaded_file_url = fs.url(filename)
        header = reports.get_columns(os.path.join(os.path.curdir,"Charts","Data",company_name,myfile.name.lower()))
        return render(request, 'filter_data.html', {
            'header': header,
            'filename':uploaded_file_url,
            'user': name,
        })
    return render(request, 'upload.html')


@login_required(login_url="/plots/")
def tables(request):
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
    return render_to_response('tables.html',{'companies':companies, 'user':request.user.get_full_name})

@login_required(login_url="/plots/")
def superadmin_data(request):
    company_name = request.GET.get("company",None)
    data_filtered = reports.filter_data(company_name)
    print(data_filtered)
    response = JsonResponse({'data':data_filtered, 'user':request.user.get_full_name})
    return response

@login_required(login_url="/plots/")
def logout(request):
    auth_logout(request)
    return redirect('/plots/')

