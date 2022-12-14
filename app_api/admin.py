from django.contrib import admin
from .models import (
    LabModel, 
    LabResultModel, 
    LabResultCategoryModel, 
    SonographyCenterModel, 
    SonographyResultModel,
)


admin.site.register(LabModel)
admin.site.register(LabResultModel)
admin.site.register(LabResultCategoryModel)

admin.site.register(SonographyCenterModel)
admin.site.register(SonographyResultModel)