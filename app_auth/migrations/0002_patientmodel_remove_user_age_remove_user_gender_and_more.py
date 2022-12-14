# Generated by Django 4.1.4 on 2022-12-14 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='کدملی')),
            ],
            options={
                'verbose_name': 'بیمار',
                'verbose_name_plural': 'بیماران',
                'ordering': ['-id'],
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=0, max_length=20, verbose_name='شماره تلفن'),
        ),
        migrations.CreateModel(
            name='ManagerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مدیر',
                'verbose_name_plural': 'مدیران',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_code', models.BigIntegerField(verbose_name='کد نظام پزشکی')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پزشک',
                'verbose_name_plural': 'پزشکان',
                'ordering': ['-id'],
            },
        ),
    ]