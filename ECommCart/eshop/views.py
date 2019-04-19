import datetime
import hashlib
import random
import socket

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_control
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from eshop.serializers import *

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


class EmailAuthBackend(object):
    @staticmethod
    def authenticate(username=None, password=None):
        try:
            user_object = User.objects.get(email=username)
            if user_object.check_password(password):
                return user_object
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def home(request):
    return render(request, 'login.html')


def user_authentication(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        email_check = User.objects.filter(email=request.POST['email'])
        if email == '' or password == '':
            error = "Please Enter the Email Address and Password."
            return render(request, 'login.html', {'error_message': error})

        if len(email_check) == 0:
            email = str(email)
            error = "Email address %s is not registered with Samruddhi." % email
            return render(request, 'login.html', {'error_message': error})

        else:
            user_object = authenticate(username=email, password=password)
            if user:
                login(request, user_object)
                if request.user.is_active:

                    return HttpResponseRedirect('/Dashboard/')
                else:
                    error = "Your account is not activate yet."
                    return render(request, "login.html", {'error_message': error})
            else:
                error = "The Password you entered is invalid."
                return render(request, "login.html", {'error_message': error})

    else:
        return render(request, 'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_session_end(request):
    logout(request)
    return render(request, 'login.html')


@transaction.atomic`
def registration(request):
    if request.POST:
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        email = request.POST['email']
        company = request.POST['company']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        terms = request.POST['terms']

        if first_name == '' or last_name == '' or email == '' or company == '' or password == ''\
                or confirm_password == '' or terms == '':
            error_message = "Please fill all the fields, all fields are mandatory."
            return render(request, 'registration.html', {'error_message': error_message})

        if password != confirm_password:
            error_message = "Password and Confirm Password not matched."
            return render(request, 'registration.html', {'error_message': error_message})

        email_address_check = User.objects.filter(email=request.POST['email'])

        if len(email_address_check) == 0:
            # noinspection PyBroadException
            try:
                with transaction.atomic():
                    userdata = User(first_name=first_name, last_name=last_name, username=email, email=email,
                                    password=make_password(password), is_active=False)
                    userdata.save()
                    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                    activation_key = hashlib.sha1((salt + email).encode('utf-8')).hexdigest()
                    key_expires = datetime.datetime.today() + datetime.timedelta(2)
                    userprofiledata = UserProfile()
                    userprofiledata.user_id = userdata.id
                    userprofiledata.company = company
                    userprofiledata.terms_condition = terms
                    userprofiledata.activation_key = activation_key
                    userprofiledata.key_expires = key_expires
                    userprofiledata.save()
                    domain = socket.gethostbyname(socket.gethostname())
                    url = "http://" + domain + ":9000/confirm/%s" % activation_key
                    send_activation_mail(email, url, first_name, last_name)

                    mail = str(email)
                    message = "Registration has been successful and verification email has been sent to %s." % mail
                    return render(request, 'registration.html', {'success_message': message})
            except:
                message = "Sorry!, something went wrong please try after sometime."
                return render(request, 'registration.html', {'error_message': message})
        else:
            mail = str(email)
            message = " %s , Email is Already Registered with us." % mail
            return render(request, 'registration.html', {'error_message': message})

    else:
        return render(request, 'registration.html')


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/login/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it has then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render(request, 'registration.html')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    message = "%s, Your account is confirmed and activated. Please login to website using your id and password."\
              % user.first_name
    return render(request, 'login.html', {'success_message': message})


def send_activation_mail(email, url, fname, lname):
    from django.template.loader import get_template
    from django.template import Context
    from django.core.mail import EmailMultiAlternatives

    plaintext = get_template('email_template_user_registration')
    htmly = get_template('email.html')

    date = datetime.datetime.today().strftime("%B %d, %Y")
    d = Context({'date': date, 'url': url, 'fname': fname, 'lname': lname})

    subject = "Email Activation"
    from_email = 'account.activation@Samruddhi.com'
    to = [email]
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True


@login_required
def dashboard(request):
    if request.POST:
        prods = Product.objects.all()

        return render(request, 'dashboard.html', {'prods': prods})
    else:
        prods = Product.objects.all()
        return render(request, 'dashboard.html', {'prods': prods})


@login_required
def create_product(request):
    if request.POST:
        name = request.POST['prod_name']
        # date = request.POST['start_date_time']
        product_category = request.POST['product_category']
        cost_of_each = request.POST['cost_of_each']
        new_prod = Product(name=name, created_date=datetime.datetime.now(), prod_cat=product_category,
                           cost_of_each=cost_of_each, user_id=request.user.id)
        new_prod.save()
        return render(request, 'dashboard.html')
    else:
        return render(request, 'create_product.html')


class customer(APIView):
    @staticmethod
    def post(request):
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        password = request.data['password']
        terms = request.data['terms']
        if email and first_name and last_name and password and terms:
            email_address_check = User.objects.filter(email=request.data['email'])
            if len(email_address_check) == 0:
                userdata = User()
                userdata.email = request.data['email']
                userdata.first_name = request.data['first_name']
                userdata.last_name = request.data['last_name']
                userdata.username = request.data['email']
                userdata.password = make_password(request.data['password'])
                userdata.save()
                userprofiledata = UserProfile()
                userprofiledata.user_id = userdata.id
                userprofiledata.terms_condition = request.data['terms']
                userprofiledata.save()
                return Response(
                    {'success': 'Congratulations!! Registration has been successful', 'user_id': int(userdata.id)})
            else:
                return Response({'error': 'Username %s is already registered' % email})
        else:
            return Response({'error': 'Please fill all the mandatory details'})

    @staticmethod
    def delete(request):
        user_id = request.data['user_id']
        if user_id:
            # noinspection PyBroadException
            try:
                User.objects.get(id=user_id).delete()
                return Response({'success': 'User id {} has been deleted.'.format(int(user_id))})
            except:
                return Response({'error': 'User matching query does not exist for user id %s' % (int(user_id))})
        else:
            return Response({'error': 'User ID cannot be None:'})


# {"token":"3f60c15b38024cdf687376d461960377df92bed8"}


class product(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                name = request.data['product_name']
                category = request.data['product_category']
                cost = request.data['product_cost']
                if name and category and cost:
                    product_obj = Product()
                    user_obj = User.objects.get(id=request.user.id)
                    product_obj.user = user_obj
                    product_obj.name = name
                    product_obj.prod_cat = category
                    product_obj.cost_of_each = cost
                    product_obj.save()
                    return Response({'success': 'product added successfully'})
                else:
                    return Response({'error': 'provide all the details'})
            else:
                return Response({'error': 'Not having permission to add product'})
        else:
            return Response({'error': 'Not Authenticated'})

    @staticmethod
    def delete(request):
        if request.user.is_authenticated():
            if request.user.is_superuser:
                product_id = request.data['product_id']
                # noinspection PyBroadException
                try:
                    Product.objects.get(id=product_id).delete()
                    return Response({'success': 'Product id {} has been deleted.'.format(int(product_id))})
                except:
                    return Response(
                        {'error': 'Product matching query does not exist for product id %s' % (int(product_id))})
            else:
                return Response({'error': 'Not having permission to add product'})
        else:
            return Response({'error': 'Not Authenticated'})


class cart(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        if request.user.is_authenticated():
            product_id = request.data['product_id']
            quantity = request.data['quantity']
            if product_id and quantity:
                # noinspection PyBroadException
                try:
                    user_obj = User.objects.get(id=request.user.id)
                    product_obj = Product.objects.get(id=product_id)
                    cost_of_each = product_obj.cost_of_each
                    cart_object = Cart()
                    cart_object.user = user_obj
                    cart_object.prod_details = product_obj
                    cart_object.quantity = quantity
                    cart_object.sum_of_prod_cost = quantity * cost_of_each
                    cart_object.save()
                    return Response({'success': 'Items added to cart.'})
                except:
                    return Response(
                        {'error': 'Product matching query does not exist for product id %s' % (int(product_id))})
            else:
                return Response({'error': 'Please provide all the details'})
        else:
            return Response({'error': 'Not Authenticated'})

    @staticmethod
    def delete(request):
        if request.user.is_authenticated():
            cart_id = request.data['cart_id']
            # noinspection PyBroadException
            try:
                Cart.objects.get(id=cart_id).delete()
                return Response({'success': 'Product id {} has been deleted.'.format(int(cart_id))})
            except:
                return Response(
                    {'error': 'Product matching query does not exist for product id %s' % (int(cart_id))})
        else:
            return Response({'error': 'Not Authenticated'})

    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            cart_data = Cart.objects.all()
            final_data = []
            cart_serializer = CartSerializer(cart_data, many=True)
            true = {'success': True}
            final_data.extend([true, cart_serializer.data])
            return Response(final_data)
        else:
            return Response({'error': 'Not Authenticated'})
