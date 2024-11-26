# Import necessary Django modules for rendering, HTTP responses, and URL redirection
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import student, Extended  # Import the models for student and extended user data
import jwt  # JSON Web Token for creating secure activation links
from .form import MovieForm # it will import moview form model

# ---- General Views ----

def homepage(request):
    """View function for the homepage."""
    return render(request, 'rift_edge.html')


# ---- Authentication Views ----

def mylogin(request):
    """Login view function - manages user login requests."""
    if request.method == 'POST':  # Only process POST requests
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user by email to get the username
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            # If email not found, render login page with error message
            return render(request, 'rift_login.html', {'mes': 'Email not found'})

        # Authenticate user
        us = authenticate(username=username, password=password)
        if us is not None:
            login(request, us)  # Log in the user
            return redirect(reverse('admin_panel'))
        else:
            return render(request, 'rift_login.html', {'mes': 'Wrong Credentials'})

    if request.user.is_authenticated:
        return redirect(reverse('admin_panel'))
    else:
        return render(request, 'rift_login.html')


def mylogout(request):
    """Logout view function - logs out the user and redirects to login page."""
    logout(request)
    return redirect(reverse('mylogin'))


def signup(request):
    """Signup view function - handles user registration requests."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        img = request.FILES.get('img')  # Fetch the uploaded profile image

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        # Create a new inactive user
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        
        # Create an extended profile with an image
        ex = Extended(id=user, image=img)
        ex.save()

        # Encode user ID in JWT for account activation link
        enc = jwt.encode({'encid': str(user.pk)}, 'secret', algorithm='HS256')
        link = f"{request.scheme}://{request.META['HTTP_HOST']}/activation/{enc}/"

        # Send the activation email
        em = EmailMessage(
            'Account Activation',
            f'Thanks for creating an account. Activate it here:\n{link}',
            from_email='buildingnewcareer@gmail.com',
            to=[email]
        )
        try:
            em.send()
        except Exception as e:
            return HttpResponse(f'Error sending email: {e}')

        # Render signup page with success message
        return render(request, 'signup.html', {'mes': 'Account created successfully! Check your email for activation.'})

    return render(request, 'signup.html')


def activation(request, id):
    """Account activation view function."""
    try:
        # Decode JWT token to retrieve user ID
        dec = jwt.decode(id, 'secret', algorithms=['HS256'])
        user_id = int(dec['encid'])
        us = User.objects.get(pk=user_id)

        # Activate user if not already active
        if not us.is_active:
            us.is_active = True
            us.save()

        return redirect(reverse('mylogin'))
    except jwt.ExpiredSignatureError:
        return HttpResponse("Activation link expired. Please request a new activation email.")
    except jwt.DecodeError:
        return HttpResponse("Invalid activation link.")
    except User.DoesNotExist:
        return HttpResponse("User not found. Activation failed.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


# ---- Restricted Views ----

@login_required(login_url='/mylogin/')
def admin_panel(request):
    """Admin panel view function - requires login."""
    return render(request, 'rift_admin_panel.html')


# ---- CRUD Operations for Student Model ----

def data(request):
    """Data view function - displays list of students."""
    students = student.objects.all()
    return render(request, 'data.html', {'stds': students})


def formdata(request):
    """Form data view function - handles new student data submission."""
    if request.method == 'POST':
        name = request.POST.get('n')
        age = request.POST.get('a')
        marks = request.POST.get('m')
        course = request.POST.get('c')

        # Create new student record
        std = student(name=name, age=age, marks=marks, course=course)
        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not saved')
    return HttpResponse('GET method received')


def movie_form(request):
    if request.method== 'POST':
        form = MovieForm(request.POST)
        
        if form.is_valid():
             form.save()
             return HttpResponse('Data Save...')
         
        else:
            return HttpResponse(f'{form.errors}')
             
    fmovie= MovieForm()
      
    return render(request, 'form.html', {'fmovie': fmovie})
    
    
    
    





def delete_std(request, id):
    """Delete student view function - removes a student by ID."""
    std = student.objects.get(pk=id)
    std.delete()
    return redirect(reverse('data'))


def update_std(request, id):
    """Update student view function - updates existing student data."""
    if request.method == 'POST':
        name = request.POST.get('n')
        age = request.POST.get('a')
        marks = request.POST.get('m')
        course = request.POST.get('c')

        std = student.objects.get(pk=id)
        std.name = name
        std.age = age
        std.marks = marks
        std.course = course

        try:
            std.save()
            return redirect(reverse('data'))
        except:
            return HttpResponse('Data not saved')

    std = student.objects.get(pk=id)
    return render(request, 'form.html', {'std': std})


from .models import Movie
from .serializers import Movieserializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def movie_data(request):
    if request.method == 'GET':
        data = Movie.objects.all()
        sr = Movieserializer(data, many=True)
        # return JsonResponse(sr.data, safe=False)
        return Response(sr.data)
    if request.method == 'POST':
        sr = Movieserializer(data=request.data)
        if sr.is_valid():
            sr.save()
            data = Movie.objects.all()
        sr = Movieserializer(data, many=True)
        # return JsonResponse(sr.data, safe=False)
        return Response(sr.data)
    
    # after this we can test post request is running or not by opening url and adding additional entry

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_movie_data(request, id):
    try:
        movie_obj = Movie.objects.get(pk=id)
    except:
        return Response({'detail': f'Movie object not found'}, status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        sr = Movieserializer(movie_obj, status= status.HTTP_302_FOUND)
        return Response(sr.data)
    
    if request.method == 'PUT':
        sr = Movieserializer(movie_obj, data= request.data)
        if sr.is_valid():
            sr.save()
            return Response(sr.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'Movie data is not Valid {sr.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
    if request.method == 'DELETE':
        movie_obj.delete()
        return Response({'detail': f'Movie object not found or may be deleted'}, status=status.HTTP_204_NO_CONTENT)