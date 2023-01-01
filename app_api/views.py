from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel, User, ManagerModel, DoctorModel
from rest_framework.permissions import AllowAny
from .serializers import (
    LabResultSerializer, 
    SonographyResultSerializer, 
    SonographyCenterSerializer,
    LabSerializer,
    UserSerializer,
    LabResultCategorySerializer,
    ManagerSerializer
)
from .models import (
    SonographyCenterModel,
    LabModel,
    LabResultCategoryModel,
    LabResultModel, 
    SonographyResultModel
)


# url: /api/v1/get/patient/data/
class GetPatientData(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        code = request.POST.get('code')
        if code:

            if not DoctorModel.objects.filter(user=request.user, is_active=True).exists():
                return Response({'msg': _('برای نمایش اطلاعات بیمار باید پزشک باشید.'), 'status': 400})

            if PatientModel.objects.filter(username=code).exists():
                patient = PatientModel.objects.get(username=code)
                lab_res = LabResultModel.objects.filter(patient=patient).all()
                sonography_res = SonographyResultModel.objects.filter(patient=patient).all()
                
                lab_res_serializer = LabResultSerializer(lab_res, many=True)
                sonography_res_serializer  = SonographyResultSerializer(sonography_res, many=True)
                
                response_data =  {
                    'lab_res': lab_res_serializer.data, 
                    'sonography_res': sonography_res_serializer.data, 
                    'status': 200
                }
                return Response(response_data)
            return Response({'status': 400})
        return Response({'status': 400})


# url: /api/v1/get/user/data/
class GetUserData(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        if request.user:
            user = User.objects.get(username=request.user.username)
            user_serializer = UserSerializer(user)

            is_sono = user.sonographycentermodel_set.filter(is_active=True).exists()
            is_lab = user.labmodel_set.filter(is_active=True).exists()
            is_doctor = user.doctormodel_set.filter(is_active=True).exists()
            is_manager = user.managermodel_set.filter(is_active=True).exists()
            
            response_data =  {
                'data': user_serializer.data,
                'is_sono': is_sono, 
                'is_lab': is_lab, 
                'is_doctor': is_doctor, 
                'is_manager': is_manager, 
                'is_admin': user.is_superuser, 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/sonography-center/
class CreateSonographyCenter(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت مرکز سونوگرافی ندارید.'), 'status': 400})

            new_sonography_center = SonographyCenterModel.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                pos=request.POST.get('pos'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )
            
            response_data =  { 
                'new_sono_center': SonographyCenterSerializer(new_sonography_center).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab/
class CreateLab(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = LabSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_lab_center = LabModel.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                pos=request.POST.get('pos'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )
            
            response_data =  { 
                'new_lab_center': LabSerializer(new_lab_center).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab-category/
class CreateLabCategory(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = LabResultCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            new_lab_category = LabResultCategoryModel.objects.create(
                title=request.POST.get('title'),
            )
            
            response_data =  { 
                'new_lab_category': LabResultCategorySerializer(new_lab_category).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/manager/
class CreateManager(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            if not request.user.is_superuser:
                return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = ManagerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )

            ManagerModel.objects.create(
                user=user,
                is_active=True
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})
