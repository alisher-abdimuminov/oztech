from django.urls import path

from .views import (
    get_courses_list,
    get_course,
    my_courses,
    get_module,
    get_lesson,
    get_subjects,
    end_lesson,
    get_course_ratings,
    save_time,
)

urlpatterns = [
    path("", get_courses_list, name="courses"),
    path("my/", my_courses, name="my_courses"),
    path("subjects/", get_subjects, name="subjects"),
    path("<int:pk>/", get_course, name="course"),
    path("<int:pk1>/modules/<int:pk2>/", get_module, name="lesson"),
    path("<int:pk1>/modules/<int:pk2>/lessons/<int:pk3>/", get_lesson, name="lesson"),
    path("<int:pk>/ratings/", get_course_ratings),

    path("end/", end_lesson, name="end_lesson"),
    path("<int:pk>/save/", save_time),
]
