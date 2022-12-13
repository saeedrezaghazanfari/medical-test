from django.contrib import admin
from .models import ExprementModel, DoctorModel, ExprimentResultModel


admin.site.register(ExprementModel)
admin.site.register(DoctorModel)
admin.site.register(ExprimentResultModel)