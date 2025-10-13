from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import decorators
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from courses.models import Rating, Lesson
from courses.serializers import RatingSerializer

from .models import User, Contact
from .serializers import UserSerializer


def index(request):
    return render(request, "index.html")


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    phone = request.data.get("phone", "")
    password = request.data.get("password", "")
    user = User.objects.filter(phone=phone)
    if not user:
        return Response({
            "status": "error",
            "code": "login-001", # phone not found
            "data": None
        })
    user = user.first()

    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "login-003", # password didnot match
            "data": None
        })

    tokens = Token.objects.filter(user=user)
    tokens.delete()

    token = Token.objects.get_or_create(user=user)
    return Response({
        "status": "success",
        "code": "login-004", # login success
        "data": {
            "token": token[0].key
        }
    })


@decorators.api_view(http_method_names=["POST"])
def signup(request: HttpRequest):
    phone = request.data.get("phone")
    full_name = request.data.get("full_name")
    password = request.data.get("password")

    if not phone:
        return Response({
            "status": "error",
            "code": "phone_is_required",
            "data": None
        })

    user = User.objects.filter(phone=phone)
    if user:
        return Response({
            "status": "error",
            "code": "signup-001", # email already exists
            "data": None
        })
    
    user = User.objects.create(
        phone=phone,
        full_name=full_name,
    )
    user.set_password(password)
    user.save()

    return Response({
        "status": "success", # signup success
        "code": "signup-002",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def logout(request: HttpRequest):
    user = request.user
    user.delete()
    return Response({
        "status": "success",
        "code": "logout-001",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def change_password(requset: HttpRequest):
    user = requset.user
    phone = requset.data.get("phone")
    password = requset.data.get("password")
    if user.is_authenticated:
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "change-password-001", # success
            "data": None
        })
    else:
        user = User.objects.get(phone=phone)
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "change-password-002", # success (with email, password)
            "data": None
        })


@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def profile(request: HttpRequest):
    user: User = request.user
    rating_obj = Rating.objects.filter(user=user)
    rating = RatingSerializer(rating_obj, many=True)
    lessons = Lesson.objects.filter(finishers=user).aggregate(**{ "duration": Sum("duration") })

    image = user.image
    
    if image:
        image = request.build_absolute_uri(image.url)
    else:
        image = None

    return Response({
        "status": "success",
        "code": "profile-001", # success
        "data": {
            "phone": user.phone,
            "full_name": user.full_name,
            "duration": lessons.get("duration"),
            "image": image,
            "rating": rating.data,
        }
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def edit_profile(request: HttpRequest):
    user_obj = request.user
    user = UserSerializer(user_obj, data=request.data, partial=True)
    if user.is_valid():
        user.save()
        return Response({
            "status": "success",
            "code": "edit-profile-001", # success
            "data": None
        })
    else:
        return Response({
            "status": "error",
            "code": "edit-profile-002", # fill the required fields
            "data": None
        })


@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def contact(request: HttpRequest):
    contact = Contact.objects.first()
    if contact:
        return Response({
            "status": "success",
            "code": "contact-001", # success
            "data": {
                "name": contact.name,
                "phone": contact.phone,
                "telegram": contact.telegram,
            }
        })
    else:
        return Response({
            "status": "success",
            "code": "contact-002", # success (with default)
            "data": {
                "name": "OzTech",
                "phone": "",
                "telegram": "",
            }
        })
