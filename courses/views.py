from datetime import datetime

from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response

from users.models import Date

from .models import (
    Course,
    Lesson,
    Subject,
    Module,
    CourseRating,
    Notification,
    Banner,
)
from .serializers import (
    CourseRatingSerializer,
    CoursesGETSerializer,
    CourseGETSerializer,
    LessonGETSerializer,
    SubjectSerializer,
    ModuleGETSerializer,
    NotificationSerializer,
    BannerSerializer,
)



@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def save_time(request: HttpRequest, pk: int):
    time = int(request.data.get("time", 0))
    course = Course.objects.filter(pk=pk)
    user = request.user

    if not course:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    
    course = course.first()

    course_rating = CourseRating.objects.filter(author=user, course=course)

    if not course_rating:
        course_rating = CourseRating.objects.create(
            author=user,
            course=course,
            time=int(time)
        )

    course_rating = course_rating.first()

    course_rating.time = time
    course_rating.save()

    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_notifications(request: HttpRequest):
    notifications = Notification.objects.filter(receivers=request.user)

    return Response(
        {
            "status": "success",
            "code": "000",
            "data": NotificationSerializer(notifications, many=True).data,
        }
    )


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_banners(request: HttpRequest):
    banners = Banner.objects.all()
    return Response(
        {
            "status": "success",
            "code": "000",
            "data": BannerSerializer(banners, many=True).data,
        }
    )


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_courses_list(request: HttpRequest):
    subject_pk = request.GET.get("subject", 0)
    is_free = request.GET.get("free", 0)

    courses_obj = Course.objects.all()

    if is_free == 1 or is_free == "1":
        courses_obj = courses_obj.filter(is_public=True)

    if subject_pk != 0:
        courses_obj = courses_obj.filter(subject_id=subject_pk)
    courses = CoursesGETSerializer(courses_obj, many=True, context={"request": request})
    return Response({"status": "success", "code": "200", "data": courses.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_course(request: HttpRequest, pk: int):
    course_obj = Course.objects.filter(pk=pk)
    if not course_obj:
        return Response({"status": "error", "code": "404", "data": None})
    course_obj = course_obj.first()

    date = Date.objects.filter(user=request.user, course=course_obj)
    if date:
        date = date.first()
        if datetime.now().date() == date.ended:
            return Response({"status": "error", "code": "000", "data": None})
    course = CourseGETSerializer(course_obj, many=False, context={"request": request})
    return Response({"status": "success", "code": "200", "data": course.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def my_courses(request: HttpRequest):
    user = request.user
    courses_obj = Course.objects.filter(students=user)
    courses = CoursesGETSerializer(courses_obj, many=True, context={"request": request})
    print("User", user)
    print("Course", courses_obj)
    return Response({"status": "success", "code": "200", "data": courses.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_module(request: HttpRequest, pk1: int, pk2: int):
    module_obj = Module.objects.filter(id=pk2)
    if not module_obj:
        return Response({"status": "error", "code": "404", "data": None})
    module_obj = module_obj.first()
    module = ModuleGETSerializer(module_obj, many=False)
    return Response({"status": "success", "code": "200", "data": module.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_lesson(request: HttpRequest, pk1: int, pk2: int, pk3: int):
    lesson_obj = Lesson.objects.get(pk=pk3)
    lesson = LessonGETSerializer(lesson_obj, many=False, context={"request": request})
    return Response({"status": "success", "code": "200", "data": lesson.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_subjects(self):
    subjects_obj = Subject.objects.all()
    subjects = SubjectSerializer(subjects_obj, many=True)
    return Response({"status": "success", "code": "200", "data": subjects.data})


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def get_course_ratings(request: HttpRequest, pk: int):
    course = Course.objects.filter(pk=pk)

    if not course:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    course = course.first()
    course_ratings = CourseRating.objects.filter(user=request.user, course=course).order_by("-time")

    return Response(
        {
            "status": "success",
            "code": "200",
            "data": CourseRatingSerializer(course_ratings, many=True).data,
        }
    )


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(
    authentication_classes=[authentication.TokenAuthentication]
)
def end_lesson(request: HttpRequest):
    lesson_id = request.data.get("lesson")
    lesson = Lesson.objects.get(pk=lesson_id)
    is_last_lesson = Lesson.objects.filter(module=lesson.module).last()
    print(is_last_lesson)
    if lesson.pk == is_last_lesson.pk:
        modules = Module.objects.filter(course=lesson.module.course)
        print(modules)
        finded = False
        for i in modules:
            print(i, lesson.module)
            if i.pk == lesson.module.pk:
                finded = True
                print("set", finded)
            elif finded:
                print("topildi")
                try:
                    i.students.add(request.user)
                    i.save()
                    finded = False
                    print(i, "saved")
                    break
                except Exception as e:
                    print(e)
                    pass
    lesson.finishers.add(request.user)
    return Response({"status": "success", "errors": {}, "data": {}})
