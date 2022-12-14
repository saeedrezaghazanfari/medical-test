from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel


class LabModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    code = models.CharField(max_length=255, unique=True, verbose_name=_('کد'))
    pos = models.CharField(max_length=255, verbose_name=_('موقعیت'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آزمایشگاه')
        verbose_name_plural = _('آزمایشگاه ها')

    def __str__(self):
        return self.title


class LabResultModel(models.Model):
    category = models.ForeignKey(to='LabResultCategoryModel', on_delete=models.SET_NULL, null=True, verbose_name=_('دسته بندی'))
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
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی آزمایش')
        verbose_name_plural = _('دسته بندی آزمایش ها')

    def __str__(self):
        return str(self.title)


class SonographyCenterModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    code = models.CharField(max_length=255, unique=True, verbose_name=_('کد'))
    pos = models.CharField(max_length=255, verbose_name=_('موقعیت'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('مرکز سونوگرافی')
        verbose_name_plural = _('مراکز سونوگرافی')

    def __str__(self):
        return self.title


class SonographyResultModel(models.Model):
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    center = models.ForeignKey(to=SonographyCenterModel, on_delete=models.SET_NULL, null=True, verbose_name=_('مرکز سونوگرافی'))
    result = models.CharField(max_length=255, verbose_name=_('جواب آزمایش'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نتیجه سونوگرافی')
        verbose_name_plural = _('نتایج سونوگرافی ها')

    def __str__(self):
        return str(self.patient)


