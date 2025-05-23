# Generated by Django 5.1.4 on 2025-01-21 19:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_course_students_course_students_month_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Javob', 'verbose_name_plural': 'Javoblar'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Kurs', 'verbose_name_plural': 'Kurslar'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Dars', 'verbose_name_plural': 'Darslar'},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'verbose_name': 'Modul', 'verbose_name_plural': 'Modullar'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Savol', 'verbose_name_plural': 'Savollar'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Test', 'verbose_name_plural': 'Testlar'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Fan', 'verbose_name_plural': 'Fanlar'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name="To'g'ri"),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question', verbose_name='Savol'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='value_1',
            field=models.TextField(blank=True, null=True, verbose_name='Qiymat 1'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='value_2',
            field=models.TextField(blank=True, null=True, verbose_name='Qiymat 2'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(verbose_name='Kurs haqida qisqacha'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='images/courses', verbose_name='Rasmi'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.IntegerField(verbose_name='Narxi'),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject', verbose_name='Fan'),
        ),
        migrations.AlterField(
            model_name='course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi"),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.IntegerField(default=60, verbose_name='Davomiyligi'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='finishers',
            field=models.ManyToManyField(blank=True, null=True, related_name='lesson_finishers', to=settings.AUTH_USER_MODEL, verbose_name='Tugatganlar'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.module', verbose_name='Modul'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_lesson', to='courses.lesson', verbose_name='Keyingi dars'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='previous',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_lesson', to='courses.lesson', verbose_name='Oldingi dars'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.quiz', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='resource',
            field=models.FileField(blank=True, null=True, upload_to='files/lessons', verbose_name='Manbaa'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='type',
            field=models.CharField(choices=[('lesson', 'Dars'), ('quiz', 'Test')], max_length=100, verbose_name='Turi'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.URLField(blank=True, null=True, verbose_name='Video link (YouTubue)'),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Kurs'),
        ),
        migrations.AlterField(
            model_name='module',
            name='finishers',
            field=models.ManyToManyField(blank=True, null=True, related_name='module_finishers', to=settings.AUTH_USER_MODEL, verbose_name='Bitirganlar'),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='module',
            name='required',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.module', verbose_name='Talab qilinadi'),
        ),
        migrations.AlterField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='module_students', to=settings.AUTH_USER_MODEL, verbose_name='Talabalar'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(verbose_name='Savol matni'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('one_select', 'Bitta javob tanlash'), ('many_select', "Ko'p javob tanlash"), ('writable', 'Yoziladigan'), ('matchable', 'Mos keladigan')], max_length=100, verbose_name='Savol turi'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nomi'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(related_name='quiz_questions', to='courses.question', verbose_name='Savollar'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='image',
            field=models.ImageField(upload_to='images/subjects', verbose_name='Rasmi'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nomi'),
        ),
    ]
