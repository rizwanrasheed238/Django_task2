
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404

from .models import Account
from django.contrib.auth import authenticate

from django.contrib import messages

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.tokens import default_token_generator


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            request.session['email'] = email

            if user.is_admin:
                return redirect('/admin/')

            elif user.is_staff:
                return redirect('/seller/')

            else:
                return redirect('home')

        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone_number = request.POST['phone']
        adrs = request.POST['adrs']
        city = request.POST['city']
        state = request.POST['state']
        pimg = request.FILES.get('pimg')
        pin = request.POST['pin']
        uname = request.POST['uname']

        cpassword = request.POST['cpassword']
        roles = request.POST['roles']
        is_user = is_staff = False

        if roles == 'Doctor':
            is_user = True
        else:
            is_staff = True

        if Account.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return redirect('login')
        elif password != cpassword:
            messages.error(request, 'password not matching')

            return redirect('login')


        else:
            user = Account.objects.create_user(email=email, password=password, fname=fname, lname=lname, roles=roles,
                                               phone_number=phone_number, Addres=adrs, city=city, state=state, pin=pin,
                                               username=uname, image=pimg, is_staff=is_staff, is_user=is_user)

            user.save()
            messages.success(request, 'you are registered')
            messages.success(request, 'Thank you for registering with us.')

            # current_site = get_current_site(request)
            # message = render_to_string('account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            #
            # send_mail(
            #     'Please activate your account',
            #     message,
            #     'medievalstore3@gmail.com',
            #     [email],
            #     fail_silently=False,
            # )
            #
            # return redirect('/login/?command=verification&email=' + email)
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def patient(request):
    return render(request,"patient.html")

def doctor(request):
    return render(request,"doctor.html")




def draft_list(request):
    drafts = blog.objects.filter(is_draft=True)
    return render(request, 'viewblog.html', {'drafts': drafts})

def vieworders(request):
    user = request.user
    blogpost=blog.objects.all()

    return render(request, "viewblog.html", {'blogpost': blogpost})

def blog(request):
    return render(request,"blog.html")

