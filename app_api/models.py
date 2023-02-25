import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel, User
from translated_fields import TranslatedField


class LabModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    code = models.CharField(max_length=255, unique=True, verbose_name=_('کد'))
    pos = models.CharField(max_length=255, verbose_name=_('موقعیت'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آزمایشگاه')
        verbose_name_plural = _('آزمایشگاه ها')

    def __str__(self):
        return self.title


class LabResultModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    category = models.ForeignKey(to='LabResultCategoryModel', on_delete=models.SET_NULL, null=True, verbose_name=_('دسته بندی'))
    sub_category = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('زیر دسته بندی'))
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    lab = models.ForeignKey(to=LabModel, on_delete=models.SET_NULL, null=True, verbose_name=_('آزمایشگاه'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان آزمایش'))
    result = models.CharField(max_length=255, verbose_name=_('جواب آزمایش'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('جواب آزمایش')
        verbose_name_plural = _('جواب آزمایش ها')

    def __str__(self):
        return str(self.patient)


class LabResultCategoryModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('عنوان')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی آزمایش')
        verbose_name_plural = _('دسته بندی آزمایش ها')

    def __str__(self):
        if get_language() == 'fa':
            return str(self.title_fa)
        elif get_language() == 'en':
            return str(self.title_en)


class LabResultSUBCategoryModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))
    category = models.ForeignKey(to=LabResultCategoryModel, null=True, on_delete=models.SET_NULL, verbose_name=_('دسته بندی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زیر دسته بندی آزمایش')
        verbose_name_plural = _('زیر دسته بندی آزمایش ها')

    def __str__(self):
        return self.title


class SonographyCenterModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    code = models.CharField(max_length=255, unique=True, verbose_name=_('کد'))
    pos = models.CharField(max_length=255, verbose_name=_('موقعیت'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('مرکز سونوگرافی')
        verbose_name_plural = _('مراکز سونوگرافی')

    def __str__(self):
        return self.title


class SonographyResultModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    center = models.ForeignKey(to=SonographyCenterModel, on_delete=models.SET_NULL, null=True, verbose_name=_('مرکز سونوگرافی'))
    title = models.CharField(max_length=255, null=True, verbose_name=_('عنوان آزمایش'))
    result = models.CharField(max_length=255, verbose_name=_('جواب آزمایش'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نتیجه سونوگرافی')
        verbose_name_plural = _('نتایج سونوگرافی ها')

    def __str__(self):
        return str(self.patient)


