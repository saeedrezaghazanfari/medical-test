# Generated by Django 4.1.4 on 2023-02-01 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_api', '0001_initial'),
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sonographyresultmodel',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_auth.patientmodel', verbose_name='بیمار'),
        ),
        migrations.AddField(
            model_name='sonographypwmodel',
            name='sono',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_api.sonographycentermodel', verbose_name='سونوگرافی'),
        ),
        migrations.AddField(
            model_name='sonographycentermodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='labresultmodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_api.labresultcategorymodel', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='labresultmodel',
            name='lab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_api.labmodel', verbose_name='آزمایشگاه'),
        ),
        migrations.AddField(
            model_name='labresultmodel',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_auth.patientmodel', verbose_name='بیمار'),
        ),
        migrations.AddField(
            model_name='labpwmodel',
            name='lab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_api.labmodel', verbose_name='آزمایشگاه'),
        ),
        migrations.AddField(
            model_name='labmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
