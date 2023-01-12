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
    LabResultRegisterSerializer,
    SonographyResultRegisterSerializer,
    ManagerSerializer,
    DoctorSerializer,
    PatientSerializer
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

    # permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if code:

            if not request.user.doctormodel_set.filter(is_active=True).exists():
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

    # permission_classes = [AllowAny]

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

    # permission_classes = [AllowAny]

    def post(self, request):
        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت مرکز سونوگرافی ندارید.'), 'status': 400})

            user_created = User.objects.create_user(
                username=request.data.get('code'),
                password=request.data.get('phone')
            )

            new_sonography_center = SonographyCenterModel.objects.create(
                user=user_created,
                title=request.data.get('title'),
                code=request.data.get('code'),
                pos=request.data.get('pos'),
                phone=request.data.get('phone'),
                permission=request.data.get('permission'),
            )
            
            response_data =  { 
                'new_sono_center': SonographyCenterSerializer(new_sonography_center).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab/
class CreateLab(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = LabSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user_created = User.objects.create_user(
                username=request.data.get('code'),
                password=request.data.get('phone')
            )

            new_lab_center = LabModel.objects.create(
                user=user_created,
                title=request.data.get('title'),
                code=request.data.get('code'),
                pos=request.data.get('pos'),
                phone=request.data.get('phone'),
                permission=request.data.get('permission'),
            )
            
            response_data =  { 
                'new_lab_center': LabSerializer(new_lab_center).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab-category/
class CreateLabCategory(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = LabResultCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            new_lab_category = LabResultCategoryModel.objects.create(
                title=request.data.get('title'),
            )
            
            response_data =  { 
                'new_lab_category': LabResultCategorySerializer(new_lab_category).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/manager/
class CreateManager(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if request.user:

            if not request.user.is_superuser:
                return Response({'msg': _('شما دسترسی لازم را برای ساخت آزمایشگاه ندارید.'), 'status': 400})

            serializer = ManagerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = User.objects.create_user(
                username=request.data.get('username'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                permission=request.data.get('permission'),
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


# url: /api/v1/user/password/
# class ChangePassword(APIView):

#     # permission_classes = [AllowAny]

#     def post(self, request):
#         if request.user:

#             serializer = UserPasswordForm(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             request.user.set_password(request.data.get('new_password1'))
            
#             response_data =  {
#                 'msg': _('رمزعبور شما با موفقیت تغییر کرد.'),
#                 'status': 200
#             }
#             return Response(response_data)
#         return Response({'status': 400})



# url: /api/v1/create/doctor/
class CreateDoctor(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):
        if request.user:

            if not request.user.is_superuser and not request.user.managermodel_set.filter(is_active=True).exists():
                return Response({'msg': _('شما دسترسی لازم را برای ساخت پزشک ندارید.'), 'status': 400})

            serializer = DoctorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = User.objects.create_user(
                username=request.data.get('username'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                permission=request.data.get('permission'),
            )

            DoctorModel.objects.create(
                user=user,
                is_active=True,
                medical_code=request.data.get('medical_code'),
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/patient/
class CreatePatient(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):
        if request.user:

            if not request.user.is_superuser and \
                not request.user.managermodel_set.filter(is_active=True).exists() and \
                not request.user.labmodel_set.filter(is_active=True).exists() and \
                not request.user.sonographycentermodel_set.filter(is_active=True).exists():
                return Response({'msg': _('شما دسترسی لازم را برای ساخت بیمار ندارید.'), 'status': 400})

            serializer = PatientSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            PatientModel.objects.create(
                username=request.data.get('username')
            )

            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/patient/lab/
class PatientLab(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):
        if request.user:

            if not request.user.is_superuser and not request.user.labmodel_set.filter(is_active=True).exists():
                return Response({'msg': _('شما دسترسی لازم را برای ثبت آزمایش بیمار ندارید.'), 'status': 400})

            serializer = LabResultRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            category = None
            patient = None
            lab = None

            if LabResultCategoryModel.objects.filter(title=request.data.get('category_title')).exists():
                category = LabResultCategoryModel.objects.get(title=request.data.get('category_title'))
            else:
                return Response({'status': 400})

            if PatientModel.objects.filter(username=request.data.get('patinet_username')).exists():
                patient = PatientModel.objects.get(username=request.data.get('patinet_username'))
            else:
                return Response({'status': 400})

            if LabModel.objects.filter(code=request.data.get('lab_username')).exists():
                lab = LabModel.objects.get(code=request.data.get('lab_username'))
            else:
                return Response({'status': 400})

            LabResultModel.objects.create(
                category=category,
                patient=patient,
                lab=lab,
                title=request.data.get('title'),
                result=request.data.get('result')
            )

            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/patient/sonography/
class PatientSonography(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):
        if request.user:

            if not request.user.is_superuser and not request.user.sonographycentermodel_set.filter(is_active=True).exists():
                return Response({'msg': _('شما دسترسی لازم را برای ثبت سونوگرافی بیمار ندارید.'), 'status': 400})

            serializer = SonographyResultRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            patient = None
            sono = None

            if PatientModel.objects.filter(username=request.data.get('patinet_username')).exists():
                patient = PatientModel.objects.get(username=request.data.get('patinet_username'))
            else:
                return Response({'status': 400})

            if SonographyCenterModel.objects.filter(code=request.data.get('sono_username')).exists():
                sono = SonographyCenterModel.objects.get(code=request.data.get('sono_username'))
            else:
                return Response({'status': 400})

            SonographyResultModel.objects.create(
                patient=patient,
                center=sono,
                result=request.data.get('result')
            )

            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})