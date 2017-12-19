from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

#============================================================#
#                       RENDER METHODS                       #
#============================================================#

def index(request):
    return render (request, 'user_login/index.html')


def success(request):
    try: 
        request.session['user_id']
    except KeyError:
        return redirect('/')  
    
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'user_login/success.html', context)

#============================================================#
#                      PROCESS METHODS                       #
#============================================================#


#New User Validation & Registration 
def registration (request):
    # Register a new user 
    if request.method == "POST":

        result = User.objects.validate_registration(request.POST)
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) #using the predifined function error
                #print (tag, error_item)

        else:
            request.session['user_id'] = result.id 
            messages.success(request, 'You have succesfully registered.') 
            return redirect('/success')  
 
    return redirect ('/')

def login(request):   

    if request.method == "POST":

        result = User.objects.validate_login(request.POST)
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) #using the predifined function error
                #print (tag, error_item)

        else:
            request.session['user_id'] = result.id 
            messages.success(request, 'You have succesfully logged in.') 
            return redirect('/success')  
 
    return redirect ('/')


    '''
        email = request.POST['email']
        password = request.POST['password']

        crt_user=User.objects.filter(email=email)
        if len(crt_user) == 1: # because crt_user is a list with 1 element 
            hashpassdb = crt_user[0].password
            print "hashpassdb:", hashpassdb
            if bcrypt.checkpw(password.encode(), hashpassdb.encode()):
                request.session['user_id'] = crt_user[0].id 
                messages.success(request, 'You have succesfully logged in.') 
                return redirect('/success')
            else:
                messages.error(request, 'Invalid login ' )
                return redirect ('/')

        else:
            messages.error(request, 'Invalid login ')
            return redirect ('/')
    '''

def logout(request):
    request.session.clear()
    return redirect('/')
