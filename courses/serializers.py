from datetime import date
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from .models import (
    Answer,
    Course,
    CourseRating,
    Lesson,
    Module,
    Question,
    Quiz,
    Rating,
    Subject,
    Permission,
    Video,
    Resource,
    Test,
)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("url", )


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("url", )


class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("url", )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name", "image", "courses")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", )

class AnswerGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("value_1", "value_2", "is_correct", )


class QuestionGETSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("answers_func")

    def answers_func(self, obj):
        answers_obj = Answer.objects.filter(question=obj)
        answers = AnswerGETSerializer(answers_obj, many=True)
        return answers.data

    class Meta:
        model = Question
        fields = ("question", "type", "answers", )


class QuizGETSerializer(serializers.ModelSerializer):
    questions = QuestionGETSerializer(Question, many=True)

    class Meta:
        model = Quiz
        fields = ("id", "name", "questions", )


class LessonGETLittleSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("check_open")

    def check_open(self, obj):
        request = self.context.get("request")
        print(request)
        if request:
            if (obj.has_previous()):
                if request.user in obj.previous.finishers.all():
                    return True
                else:
                    return False
            else:
                return True
        return True

    class Meta:
        model = Lesson
        fields = ("id", "name", "type", "duration", "is_open", )


class ModuleRequiredSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("is_open_func")
    lessons = serializers.SerializerMethodField("get_lessons")

    def get_lessons(self, obj):
        return LessonGETLittleSerializer(obj.lessons(), many=True, context=self.context).data
    

    def is_open_func(self, obj: Module):
        request = self.context.get("request")
        course = obj.course
        if course.modules().first() == obj:
            return True
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False
    class Meta:
        model = Module
        fields = ("id", "name", "is_open", "lessons", )


class LessonGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("check_open")
    previous = LessonGETLittleSerializer(Lesson.objects.all(), many=False)
    next = LessonGETLittleSerializer(Lesson.objects.all(), many=False)
    videos = serializers.SerializerMethodField("get_videos")
    resources = serializers.SerializerMethodField("get_resources")
    tests = serializers.SerializerMethodField("get_tests")
    
    def check_open(self, obj):
        request = self.context.get("request")
        if request:
            if (obj.has_previous()):
                if request.user in obj.previous.finishers.all():
                    return True
                else:
                    return False
            else:
                return True
        return True
    
    def get_videos(self, obj: Lesson):
        videos = Video.objects.filter(lesson=obj)
        return VideosSerializer(videos, many=True).data
    
    def get_resources(self, obj: Lesson):
        resources = Resource.objects.filter(lesson=obj)
        return ResourcesSerializer(resources, many=True).data
    
    def get_tests(self, obj: Lesson):
        tests = Test.objects.filter(lesson=obj)
        return TestSerializer(tests, many=True).data
    
    class Meta:
        model = Lesson
        fields = ("id", "name", "type", "videos", "duration", "resources", "tests", "previous", "next", "is_open", "created")


class ModuleGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    required = ModuleRequiredSerializer(Module.objects.all(), many=False)
    lessons = LessonGETLittleSerializer(Lesson.objects.all(), many=True)

    def is_open_func(self, obj):
        request = self.context.get("request")
        course = obj.course
        if course.modules().first() == obj:
            return True
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False
    

    class Meta:
        model = Module
        fields = ("id", "name", "required", "video_length", "count_students", "count_finishers", "count_lessons", "students", "lessons", "is_open")


class CoursesGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    percentage = serializers.SerializerMethodField("percentage_func")
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    rest = serializers.SerializerMethodField("rest_func")

    def rest_func(self, obj):
        request = self.context.get("request")
        permission = Permission.objects.filter(user=request.user, course=obj)
        if permission:
            permission = permission.first()
            return permission.ended
        return None

    def is_open_func(self, obj: Course):
        request = self.context.get("request")
        if request:
            obj.students.add(request.user)
            obj.save()
            permission = Permission.objects.filter(user=request.user, course=obj)
            if permission:
                permission = permission.first()
                now = date.today()
                if now == permission.ended:
                    permission.delete()
                return True
            return False
        return False

    def percentage_func(self, obj):
        request = self.context.get("request")
        user = request.user
        count = 0
        for module in obj.modules():
            count += module.finished_lessons(user=user)
        if obj.count_lessons() == 0:
            return 0
        return count * 100 / obj.count_lessons()

    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "percentage", "length", "count_modules", "count_lessons", "count_students", "is_open", "rest", "created", )


class CourseGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    percentage = serializers.SerializerMethodField("percentage_func")
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    modules = serializers.SerializerMethodField("modules_func")

    def is_open_func(self, obj: Course):
        request = self.context.get("request")
        if request:
            permission = Permission.objects.filter(user=request.user, course=obj)
            obj.students.add(request.user)
            obj.save()
            if permission:
                permission = permission.first()
                now = date.today()
                if now == permission.ended:
                    permission.delete()
                return True
            return False
        return False

    def modules_func(self, obj):
        modules_obj = Module.objects.filter(course=obj)
        modules = ModuleRequiredSerializer(modules_obj, many=True, context=self.context)
        return modules.data
    
    def percentage_func(self, obj):
        request = self.context.get("request")
        user = request.user
        count = 0
        for module in obj.modules():
            count += module.finished_lessons(user=user)
        if obj.count_lessons() == 0:
            return 0
        return count * 100 / obj.count_lessons()


    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "percentage", "length", "count_modules", "count_lessons", "count_students", "count_quizzes", "modules", "is_open", "created", )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", )


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ("id", "name", )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", )


class RatingSerializer(serializers.ModelSerializer):
    course = CourseSerializer(Course, many=False)
    module = ModuleSerializer(Module, many=False)
    lesson = LessonSerializer(Lesson, many=False)
    class Meta:
        model = Rating
        fields = ("course", "module", "lesson", "score", "percent", "created", )


class CourseRatingSerializer(serializers.ModelSerializer):
    course = CourseSerializer(Course, many=False)
    user = UserSerializer(User, many=False)
    class Meta:
        model = CourseRating
        fields = ("user", "course", "score", )