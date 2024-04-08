from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password                    ## TO make encryption to the password
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.




@api_view(['POST'])
def register(request):
    data = request.data
    user = SingUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
            )
            return Response(
                {'details':'Your account registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'error':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)
    




# this view function returns information about the currently authenticated user in JSON format, but only if the user is authenticated. Otherwise, 
# it returns an unauthorized response. It's commonly used in APIs to provide endpoints for clients to access their own user information after authentication.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)






#  this view function handles updating user information based on the data received in a PUT request. It updates the user's first name, last name, 
# email, username,and password (if provided) and returns the updated user data in the response.
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.username = data['email']
    user.last_name = data['last_name']
    user.email = data['email']

    if data['password'] != "":
        user.password =  make_password(data['password'])

    user.save()
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)







# the protocol defines the rules for communication, while the host specifies the location of the resource being accessed. Both components are essential in identifying and accessing resources on the web.
# this function dynamically constructs the current host URL based on the protocol (HTTP or HTTPS) and the host extracted from the incoming request. This can be useful in Django applications for generating absolute URLs within views or templates, especially in scenarios where the application needs to provide links that include the current host.
def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)






# this view function handles the forgot password functionality by generating a password reset token, setting an expiry date for it, 
# sending a password reset email containing the reset link to the user, and returning a response confirming that the email has been sent.
@api_view(['POST'])
def forgot_password(request):
    data = request.data
    # This retrieves the user object associated with the provided email address. If no user is found with the given email, it returns a 404 Not Found response.
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})

 





@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None 
    user.profile.save() 
    user.save()
    return Response({'details': 'Password reset done '})