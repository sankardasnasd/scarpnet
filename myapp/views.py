import datetime
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')


def login(request):
    return render(request,'login.html')

def login_post(request):
    username = request.POST['username']
    password = request.POST['password']

    a = Login.objects.filter(username=username, password=password)
    if a.exists():
        b = Login.objects.get(username=username, password=password)
        request.session['lid'] = b.id
        if b.type == 'admin':
            return HttpResponse('''<script>alert("Login successfully ");window.location='/admin_home'</script>''')
        elif b.type == 'agency':
            return HttpResponse('''<script>alert("Login successfully ");window.location='/agency_home'</script>''')
        elif b.type == 'user':
            return HttpResponse('''<script>alert("Login successfully ");window.location='/user_home'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')



def admin_home(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    s=Scrap.objects.all()
    scount=s.count()
    request.session['scount']=scount

    u=User.objects.all()
    ucount=u.count()
    request.session['ucount']=ucount

    a = Agency.objects.all()
    acount = a.count()
    request.session['acount'] = acount
    return render(request,'admin/admin_home.html',{'scount':scount,'ucount':ucount,'acount':acount})


def add_category(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    if 'submit' in request.POST:
        name=request.POST['name']

        aa=Category.objects.filter(name=name)
        if aa.exists():
            return HttpResponse('''<script>alert("Already Taken ");window.location='/add_category'</script>''')

        a=Category()
        a.name=name
        a.save()
        return HttpResponse('''<script>alert("Added ");window.location='/add_category'</script>''')
    return render(request,'admin/add_category.html')


def admin_view_category(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Category.objects.all().order_by('-id')
    return render(request,'admin/view_category.html',{'data':a})


def delete_cat(request,id):
    a=Category.objects.get(id=id)
    a.delete()
    return HttpResponse('''<script>alert("Deleted ");window.location='/admin_view_category'</script>''')


def admin_view_user(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    users = User.objects.all().order_by('-id')  # Fetch all users from the database
    return render(request, 'admin/view user.html', {'users': users})

def admin_view_agency(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    users = Agency.objects.all().order_by('-id')  # Fetch all users from the database
    return render(request, 'admin/view_agency.html', {'users': users})


def accept_agency(request,id):
    a=Login.objects.filter(id=id).update(type='agency')
    b=Agency.objects.filter(LOGIN_id=id).update(status='Approved')
    return HttpResponse('''<script>alert("Approved ");window.location='/admin_view_agency'</script>''')

def reject_agency(request,id):
    a=Login.objects.filter(id=id).update(type='pending')
    b=Agency.objects.filter(LOGIN_id=id).update(status='Rejected')
    return HttpResponse('''<script>alert("Rejected ");window.location='/admin_view_agency'</script>''')


def feedback_list_view(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    feedbacks = Feedback.objects.all().order_by('-id')
    return render(request, 'admin/view feedback.html', {'feedbacks': feedbacks})



from django.shortcuts import render
from .models import Feedback, Agency  # Make sure to import the necessary models


def feedback_list_view_search(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()  # Get the agency name from the POST request

        # Filter feedbacks based on the agency name
        feedbacks = Feedback.objects.filter(AGENCY__name__icontains=name)  # Using icontains for case-insensitive search

        return render(request, 'admin/view feedback.html', {'feedbacks': feedbacks})
    else:
        feedbacks = Feedback.objects.all()  # If no search, return all feedbacks
        return render(request, 'admin/view feedback.html', {'feedbacks': feedbacks})


def complaint_list_view(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    complaints = Complaints.objects.all().order_by('-id')
    return render(request, 'admin/compla.html', {'complaints': complaints})

def complaint_list_view_search(request):
    name=request.POST['name']

    complaints = Complaints.objects.filter(USER__name__icontains=name)
    return render(request, 'admin/compla.html', {'complaints': complaints})

def send_reply(request,id):
    a=Complaints.objects.get(id=id)
    return render(request, 'admin/sendreply.html', {'data': a})

def sendreply_post(request):
    id=request.POST['id']
    reply=request.POST['reply']

    a=Complaints.objects.get(id=id)
    a.reply=reply
    a.save()
    return HttpResponse('''<script>alert("Replied ");window.location='/complaint_list_view'</script>''')


def view_scrap(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    items = Scrap.objects.all().order_by('-id')
    return render(request, 'admin/view scrap.html', {'items': items})



def agency_reg(request):
    if 'submit' in request.POST:
        name=request.POST['name']
        place=request.POST['place']
        email=request.POST['email']
        phone=request.POST['phone']
        post=request.POST['post']
        password=request.POST['Password']


        aa=Login.objects.filter(username=email)
        if aa.exists():
            return HttpResponse('''<script>alert("Already Exists ");window.location='/agency_reg'</script>''')

        a=Login()
        a.username=email
        a.password=password
        a.type='pending'
        a.save()


        b=Agency()
        b.LOGIN=a
        b.name=name
        b.phone=phone
        b.place=place
        b.post=post
        b.email=email
        b.status='pending'
        b.save()
        return HttpResponse('''<script>alert("Success ");window.location='/'</script>''')
    return render(request,'agency/register.html')

def agency_home(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    s=Scrap.objects.filter(AGENCY__LOGIN_id=request.session['lid'])
    scount=s.count()
    request.session['scount']=scount

    u=User.objects.all()
    ucount=u.count()
    request.session['ucount']=ucount

    a = Feedback.objects.filter(AGENCY__LOGIN_id=request.session['lid'])
    acount = a.count()
    request.session['acount'] = acount


    return render(request,'agency/agency_home.html',{'scount':scount,'ucount':ucount,'acount':acount})

def view_profile(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    A=Agency.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'agency/profile.html',{'profile':A})


def add_scrap(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Category.objects.all()
    if 'submit' in request.POST:
        CATEGORY=request.POST['CATEGORY']
        name=request.POST['name']
        price=float(request.POST['price'])
        description=request.POST['description']

        c=Scrap()
        c.AGENCY=Agency.objects.get(LOGIN_id=request.session['lid'])
        c.CATEGORY=Category.objects.get(id=CATEGORY)
        c.name=name
        c.price=price
        c.description=description
        c.save()
        return HttpResponse('''<script>alert("Success ");window.location='/add_scrap'</script>''')

    return render(request,'agency/Add scrap.html',{'data':a})


def agency_view_scrap(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Scrap.objects.filter(AGENCY__LOGIN_id=request.session['lid'])
    return render(request,'agency/view scrap.html',{'data':a})


def delete_scrap(request,id):
    a=Scrap.objects.get(id=id)
    a.delete()
    return HttpResponse('''<script>alert("Deleted ");window.location='/agency_view_scrap'</script>''')


def agency_view_feedback(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Feedback.objects.filter(AGENCY__LOGIN_id=request.session['lid'])
    return render(request,'agency/view feedback.html',{'data':a})


def agency_view_request(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Request.objects.filter(SCRAP__AGENCY__LOGIN_id=request.session['lid'])
    return render(request,'agency/view request.html',{'data':a})

def accept_request(request,id):
    a=Request.objects.filter(id=id).update(status='Accept')
    return HttpResponse('''<script>alert("Accepted ");window.location='/agency_view_request'</script>''')
def reject_request(request,id):
    a=Request.objects.filter(id=id).update(status='Rejected')
    return HttpResponse('''<script>alert("Rejected ");window.location='/agency_view_request'</script>''')



def edit_scrap(request,id):
    b=Category.objects.all()
    a=Scrap.objects.get(id=id)
    return render(request,'agency/edit scrap.html',{'data':a,'data1':b})

def edit_scrap_post(request):
    id = request.POST['id']
    CATEGORY = request.POST['CATEGORY']
    name = request.POST['name']
    price = request.POST['price']
    description = request.POST['description']

    c = Scrap.objects.get(id=id)
    c.AGENCY = Agency.objects.get(LOGIN_id=request.session['lid'])
    c.CATEGORY = Category.objects.get(id=CATEGORY)
    c.name = name
    c.price = price
    c.description = description
    c.save()
    return HttpResponse('''<script>alert("Success ");window.location='/agency_view_scrap'</script>''')


def edit_profile(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Agency.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'agency/edit profile.html',{'data':a})


# def edit_profile_post(request):
#     id=request.POST['id']
#     name = request.POST['name']
#     place = request.POST['place']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     post = request.POST['post']
#
#     b = Agency.objects.get(id=id)
#     b.name = name
#     b.phone = phone
#     b.place = place
#     b.post = post
#     b.email = email
#     b.save()
#     return HttpResponse('''<script>alert("Success ");window.location='/view_profile'</script>''')


from django.http import HttpResponse
from .models import Agency, Login

def edit_profile_post(request):
    id = request.POST['id']
    name = request.POST['name']
    place = request.POST['place']
    email = request.POST['email']
    phone = request.POST['phone']
    post = request.POST['post']

    # Get the agency instance
    agency = Agency.objects.get(id=id)

    # Update agency details
    agency.name = name
    agency.phone = phone
    agency.place = place
    agency.post = post
    agency.email = email

    # Save the updated agency instance
    agency.save()

    # Update the corresponding Login username if it changes
    if agency.LOGIN.username != email:
        login = agency.LOGIN
        login.username = email
        login.save()

    return HttpResponse('''<script>alert("Success ");window.location='/view_profile'</script>''')

def user_home(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Scrap.objects.all()
    return render(request,'user/userindex.html',{'scrap':a})


def user_reg(request):
    if 'submit' in request.POST:
        name=request.POST['name']
        place=request.POST['place']
        email=request.POST['email']
        phone=request.POST['phone']
        post=request.POST['post']
        password=request.POST['Password']


        aa=Login.objects.filter(username=email)
        if aa.exists():
            return HttpResponse('''<script>alert("Already Exists ");window.location='/user_reg'</script>''')

        a=Login()
        a.username=email
        a.password=password
        a.type='user'
        a.save()


        b=User()
        b.LOGIN=a
        b.name=name
        b.phone=phone
        b.place=place
        b.post=post
        b.email=email
        b.save()
        return HttpResponse('''<script>alert("Success ");window.location='/'</script>''')
    return render(request,'user/userregister.html')


def user_view_profile(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    A=User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'user/profile.html',{'profile':A})


def user_edit_profile(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    A=User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'user/edit profile.html',{'profile':A})

def user_edit_profile_post(request):
    id = request.POST['id']
    name = request.POST['name']
    place = request.POST['place']
    email = request.POST['email']
    phone = request.POST['phone']
    post = request.POST['post']

    # Get the agency instance
    agency = User.objects.get(id=id)

    # Update agency details
    agency.name = name
    agency.phone = phone
    agency.place = place
    agency.post = post
    agency.email = email

    # Save the updated agency instance
    agency.save()

    # Update the corresponding Login username if it changes
    if agency.LOGIN.username != email:
        login = agency.LOGIN
        login.username = email
        login.save()

    return HttpResponse('''<script>alert("Success ");window.location='/user_view_profile'</script>''')
def user_view_agency(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    users = Agency.objects.filter(status='Approved').order_by('-id')  # Fetch all users from the database
    return render(request, 'user/view_agency.html', {'users': users})

def user_view_scarp(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    users = Scrap.objects.all().order_by('-id')  # Fetch all users from the database
    return render(request, 'user/view_scrap.html', {'users': users})


def user_view_more(request,id):
    a=Scrap.objects.get(id=id)
    return render(request,'user/more.html',{'user':a})


def user_send_request(request,id):
    aa=Scrap.objects.get(id=id)

    return render(request,'user/qty.html',{'data':aa})


def user_send_request_post(request):
    id=request.POST['id']
    qty=float(request.POST['qty'])
    c=Scrap.objects.get(id=id)
    am=float(c.price)
    total=am*qty

    r=Request.objects.filter(SCRAP_id=id,USER__LOGIN_id=request.session['lid'])
    if r.exists():
        return HttpResponse('''<script>alert("Already Requested ");window.location='/user_view_scarp'</script>''')

    a = Request()
    a.USER = User.objects.get(LOGIN_id=request.session['lid'])
    a.SCRAP = c
    a.date = datetime.datetime.now().today().date()
    a.status = 'requested'
    a.qty=qty
    a.amount=total
    a.save()
    return HttpResponse('''<script>alert("Requested ");window.location='/user_view_scarp'</script>''')


def user_view_request(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Request.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request,'user/user view request.html',{'data':a})


def user_send_feedback(request, id):
    o = Agency.objects.get(id=id)
    if 'submit' in request.POST:
        rating = request.POST['rating']
        review = request.POST['review']  # Ensure this matches the form field name

        a = Feedback()
        a.USER = User.objects.get(LOGIN_id=request.session['lid'])
        a.date = datetime.datetime.now().today().date()
        a.rating = rating
        a.AGENCY = o  # Correctly assigning the Agency instance
        a.feedback = review
        a.save()
        return HttpResponse('''<script>alert("Feedback Sent ");window.location='/user_home'</script>''')

    return render(request, 'user/send feedback.html', {'data': o})

def send_complaint(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    if 'submit' in request.POST:
        compl=request.POST['com']
        a=Complaints()
        a.USER=User.objects.get(LOGIN_id=request.session['lid'])
        a.date = datetime.datetime.now().today().date()
        a.reply='pending'
        a.complaint=compl
        a.save()
        return HttpResponse('''<script>alert(" Sent ");window.location='/user_home'</script>''')

    return render(request,'user/send complaints.html')

def user_view_complaint(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert("Logout successfully ");window.location='/'</script>''')

    a=Complaints.objects.filter(USER__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request,'user/view compla.html',{'data':a})