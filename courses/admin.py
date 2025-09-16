from unfold import admin as uadmin
from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Module,
    Subject,
    Permission,
    Video,
    Resource,
    Test,
    Banner,
    Notification,
)



@admin.register(Banner)
class BannerModelAdmin(uadmin.ModelAdmin):
    list_display = ["title", "link", ]


@admin.register(Notification)
class NotificationModelAdmin(uadmin.ModelAdmin):
    list_display = ["title", "description",]


@admin.register(Test)
class TestModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "url", ]


class LessonTabularInline(uadmin.StackedInline):
    model = Lesson
    extra = 0


class ModuleTabularInline(uadmin.StackedInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "price", "count_students", "created", ]
    inlines = [ModuleTabularInline]


@admin.register(Module)
class ModuleModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "course", "required", ]
    inlines = [LessonTabularInline]


# @admin.register(Question)
# class QuestionModelAdmin(uadmin.ModelAdmin):
#     list_display = ["question", "type", ]
#     inlines = [AnswerTabulrInline]


@admin.register(Subject)
class SubjectModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", ]

# @admin.register(Quiz)
# class QuizModelAdmin(uadmin.ModelAdmin):
#     list_display = ["name", ]


@admin.register(Lesson)
class LessonModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "type", ]


@admin.register(Permission)
class PermissionModelAdmin(uadmin.ModelAdmin):
    list_display = ["user", "course", "type", "ended"]


@admin.register(Video)
class VideoModelAdmin(uadmin.ModelAdmin):
    list_display = ["lesson", "name", ]


@admin.register(Resource)
class ResourceModelAdmin(uadmin.ModelAdmin):
    list_display = ["lesson", "name", ]

