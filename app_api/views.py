from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel, User, ManagerModel, DoctorModel
# from rest_framework.permissions import AllowAny
from .serializers import (
    LabResultSerializer, 
    SonographyResultSerializer, 
    SonographyCenterSerializer,
    LabSerializer,
    UserSerializer,
    LabResultCategorySerializer,
    LabResultSUBCategorySerializer,
    LabResultRegisterSerializer,
    SonographyResultRegisterSerializer,
    ManagerSerializer,
    DoctorSerializer,
    PatientSerializer,
    LabDATASerializer,
    SonographyCenterDATASerializer,
)
from .models import (
    SonographyCenterModel,
    LabModel,
    LabResultCategoryModel,
    LabResultSUBCategoryModel,
    LabResultModel, 
    SonographyResultModel,
)


# url: /api/v1/patient/results/sono/
class GetPatientSono(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if not request.data.get('code'):
            return Response({'status': 400})

        patient = get_object_or_404(PatientModel, username=request.data.get('code'))
        sonography_res = list()

        if request.data.get('from_data') and request.data.get('to_data'):
            from_data = request.data.get('from_data')
            to_data = request.data.get('to_data')
            sonography_res = SonographyResultModel.objects.filter(patient=patient, data__gte=from_data, data__lte=to_data).all()

        else:
            sonography_res = SonographyResultModel.objects.filter(patient=patient).all()
        
        response_data =  {
            'sonography_res': SonographyResultSerializer(sonography_res, many=True).data, 
            'status': 200
        }
        return Response(response_data)
    

# url: /api/v1/patient/results/lab/
class GetPatientLab(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if not request.data.get('code'):
            return Response({'status': 400})

        patient = get_object_or_404(PatientModel, username=request.data.get('code'))
        lab_res = list()

        if request.data.get('from_data') and request.data.get('to_data'):
            from_data = request.data.get('from_data')
            to_data = request.data.get('to_data')
            lab_res = LabResultModel.objects.filter(patient=patient, data__gte=from_data, data__lte=to_data).all()

        else:
            lab_res = LabResultModel.objects.filter(patient=patient).all()

        response_data =  {
            'lab_res': LabResultSerializer(lab_res, many=True).data, 
            'status': 200
        }
        return Response(response_data)
    

# url: /api/v1/patient/exists/
class IsPatient(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if not request.data.get('code'):
            return Response({'status': 400})

        if PatientModel.objects.filter(username=request.data.get('code')).exists():
            return Response({'status': 200, 'is_exists': True})
        return Response({'status': 200, 'is_exists': False})


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
                'is_sono': is_sono, 
                'is_lab': is_lab, 
                'is_doctor': is_doctor, 
                'is_manager': is_manager, 
                'is_admin': user.is_superuser, 
                'status': 200
            }

            if is_sono:
                sono_serializer = SonographyCenterDATASerializer(user.sonographycentermodel_set.first())
                response_data['data'] = sono_serializer.data

            elif is_lab:
                lab_serializer = LabDATASerializer(user.labmodel_set.first())
                response_data['data'] = lab_serializer.data

            elif is_doctor:
                response_data['medical_code'] = user.doctormodel_set.first().medical_code
                response_data['data'] = user_serializer.data

            elif is_manager:
                response_data['data'] = user_serializer.data

            else:
                response_data['data'] = user_serializer.data

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

            user_created = None
            new_sonography_center = None

            if not User.objects.filter(username=request.data.get('code')).exists():
                user_created = User.objects.create_user(
                    username=request.data.get('code'),
                    password=request.data.get('password'),
                    permission=request.data.get('permission'),
                )
            else:
                user_created =  User.objects.get(username=request.data.get('code'))

            if not SonographyCenterModel.objects.filter(code=request.data.get('code')).exists():
                new_sonography_center = SonographyCenterModel.objects.create(
                    user=user_created,
                    title=request.data.get('title'),
                    code=request.data.get('code'),
                    pos=request.data.get('pos'),
                    phone=request.data.get('phone'),
                )

            else:
                return Response({'status': 400})
            
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

            user_created = None
            new_lab_center = None

            if not User.objects.filter(username=request.data.get('code')).exists():
                user_created = User.objects.create_user(
                    username=request.data.get('code'),
                    password=request.data.get('password'),
                    permission=request.data.get('permission'),
                )
            else:
                user_created = User.objects.get(username=request.data.get('code'))

            if not LabModel.objects.filter(code=request.data.get('code')).exists():
                new_lab_center = LabModel.objects.create(
                    user=user_created,
                    title=request.data.get('title'),
                    code=request.data.get('code'),
                    pos=request.data.get('pos'),
                    phone=request.data.get('phone'),
                )

            else:
                return Response({'status': 400})
            
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
                    return Response({'msg': _('شما دسترسی لازم را برای ثبت دسته بندی آزمایش ندارید.'), 'status': 400})

            serializer = LabResultCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_lab_category = None
            
            if not LabResultCategoryModel.objects.filter(title_fa=request.data.get('title_fa')).exists():
                new_lab_category = LabResultCategoryModel.objects.create(
                    title_fa=request.data.get('title_fa'),
                    title_en=request.data.get('title_en'),
                )
            else:
                return Response({'status': 400})
            
            response_data =  { 
                'new_lab_category': LabResultCategorySerializer(new_lab_category).data,
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab-subcategory/
class CreateLabSUBCategory(APIView):

    # permission_classes = [AllowAny]

    def post(self, request):

        if request.user:

            if not request.user.managermodel_set.filter(is_active=True).exists():
                if not request.user.is_superuser:
                    return Response({'msg': _('شما دسترسی لازم را برای ثبت زیر دسته بندی آزمایش ندارید.'), 'status': 400})

            serializer = LabResultSUBCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_lab_subcategory = None
            
            if not LabResultSUBCategoryModel.objects.filter(title=request.data.get('title')).exists():
                new_lab_subcategory = LabResultSUBCategoryModel.objects.create(
                    title=request.data.get('title'),
                    category=get_object_or_404(LabResultCategoryModel, title=request.data.get('category')),
                )
            else:
                return Response({'status': 400})
            
            response_data =  { 
                'new_lab_subcategory': LabResultSUBCategorySerializer(new_lab_subcategory).data,
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

            user = None

            if request.data.get('username') and User.objects.filter(username=request.data.get('username')).exists():
                user = User.objects.get(username=request.data.get('username'))

            else:
                if not request.data.get('username'):
                    return Response({'msg': 'username is required.', 'status': 400})
                if not request.data.get('password'):
                    return Response({'msg': 'password is required.', 'status': 400})
                if not request.data.get('first_name'):
                    return Response({'msg': 'first_name is required.', 'status': 400})
                if not request.data.get('last_name'):
                    return Response({'msg': 'last_name is required.', 'status': 400})
                if not request.data.get('email'):
                    return Response({'msg': 'email is required.', 'status': 400})
                if not request.data.get('phone'):
                    return Response({'msg': 'phone is required.', 'status': 400})
                if not request.data.get('permission'):
                    return Response({'msg': 'permission is required.', 'status': 400})

                user = User.objects.create_user(
                    username=request.data.get('username'),
                    password=request.data.get('password'),
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    email=request.data.get('email'),
                    phone=request.data.get('phone'),
                    permission=request.data.get('permission'),
                )

            if not ManagerModel.objects.filter(user=user).exists():
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

            user = None

            if request.data.get('username') and User.objects.filter(username=request.data.get('username')).exists():
                user = User.objects.get(username=request.data.get('username'))

            else:
                if not request.data.get('username'):
                    return Response({'msg': 'username is required.', 'status': 400})
                if not request.data.get('password'):
                    return Response({'msg': 'password is required.', 'status': 400})
                if not request.data.get('first_name'):
                    return Response({'msg': 'first_name is required.', 'status': 400})
                if not request.data.get('last_name'):
                    return Response({'msg': 'last_name is required.', 'status': 400})
                if not request.data.get('email'):
                    return Response({'msg': 'email is required.', 'status': 400})
                if not request.data.get('phone'):
                    return Response({'msg': 'phone is required.', 'status': 400})
                if not request.data.get('permission'):
                    return Response({'msg': 'permission is required.', 'status': 400})
                
                user = User.objects.create_user(
                    username=request.data.get('username'),
                    password=request.data.get('password'),
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    email=request.data.get('email'),
                    phone=request.data.get('phone'),
                    permission=request.data.get('permission'),
                )

            if not DoctorModel.objects.filter(user=user).exists():
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

            if not PatientModel.objects.filter(username=request.data.get('username')).exists():
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
                sub_category=request.data.get('sub_category_title'),
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
    

# url: /api/v1/list/categories/
class CategoriesList(APIView):

    # permission_classes = [AllowAny]

    def get(self, request):
        categories = LabResultCategoryModel.objects.all()
        response_data =  {
            'categories': LabResultCategorySerializer(categories, many=True).data, 
            'status': 200
        }
        return Response(response_data)


# url: /api/v1/list/sub-categories/
class SubCategoriesList(APIView):

    # permission_classes = [AllowAny]

    def get(self, request):
        subcategories = LabResultSUBCategoryModel.objects.all()
        response_data =  {
            'sub_categories': LabResultSUBCategorySerializer(subcategories, many=True).data, 
            'status': 200
        }
        return Response(response_data)
