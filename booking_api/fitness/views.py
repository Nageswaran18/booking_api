from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, date
from .pagination import *
from dateutil.parser import parse

class UserRegisterApi(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        try:
            pDict = request.data
            print(pDict)

            user = CustomUser.objects.create(
                username=pDict['username'],
                email=pDict.get('email', ''),
                first_name=pDict.get('first_name', ''),
                last_name=pDict.get('last_name', ''),
                role=pDict['role'],
                password=make_password(pDict['password'])
            )

            UserDetail.objects.create(
                user=user,
                date_of_birth=pDict.get('date_of_birth'),
                phone_number=pDict['phone_number'],
                gender=pDict['gender'],
                profile_picture = request.FILES.get('profile_picture', None),
                address_line1=pDict['address_line1'],
                address_line2=pDict.get('address_line2', '')
            )

            return JsonResponse({
                "message": "User registered successfully",
                "result": True
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return JsonResponse({
                "message": "Validation error",
                "result": False,
                "errors": ve.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during registration",
                "result":False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserListApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        message = 'Success'
        result = True
        try:
            users = UserDetail.objects.select_related('user').all()
            serializer = UserDetailSerializer(users, many=True)
            return JsonResponse({
                "message": message,
                "result": result,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({
                "message": "An error occurred while fetching users",
                "result": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FitnessClassApi(APIView):

    def post(self, request):
        message = 'Success'
        result = True

        try:
            pDict = request.data
            print(pDict)
            serializer = FitnessClassSerializer(data=pDict)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "message":message,
                    "result":result,
                }, status=status.HTTP_200_OK)
            return JsonResponse({
                "message": "Validation error",
                "result": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
            return JsonResponse({
                "message": "An error occurred during registration",
                "result":False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request):
        message = 'Success'
        result = True

        try:
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            print(f"Start date string received: {start_date_str}")
            if not start_date_str:
                return JsonResponse({
                    "message": "start_date is required",
                    "result": False
                }, status=status.HTTP_400_BAD_REQUEST)

            start_date = parse(start_date_str).date()

            if start_date < date.today():
                return JsonResponse({
                    "message": "start_date cannot be a past date",
                    "result": False
                }, status=status.HTTP_400_BAD_REQUEST)

            if end_date_str:
                end_date = parse(end_date_str).date()

                if end_date < date.today():
                    return JsonResponse({
                        "message": "end_date cannot be a past date",
                        "result": False
                    }, status=status.HTTP_400_BAD_REQUEST)

                if end_date < start_date:
                    return JsonResponse({
                        "message": "end_date cannot be earlier than start_date",
                        "result": False
                    }, status=status.HTTP_400_BAD_REQUEST)

                fitness_objs = FitnessClass.objects.filter(start_time__date__range=[start_date, end_date])
            else:
                fitness_objs = FitnessClass.objects.filter(start_time__date=start_date)

            serializer = FitnessClassSerializer(fitness_objs, many=True)
            return JsonResponse({
                "message": message,
                "result": result,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except (ValueError, TypeError):
            return JsonResponse({
                "message": "Invalid date format. Acceptable formats: YYYY-MM-DD or ISO datetime.",
                "result": False
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during retrieval",
                "result": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    def put(self, request):
        message = 'Success'
        result = True

        try:
            uDict = request.data
            fitness_id = request.query_params.get('fitness_id')
            fitness_obj = FitnessClass.objects.get(id=fitness_id)
            serializer = FitnessClassSerializer(fitness_obj, data=uDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "message":message,
                    "result":result,
                }, status=status.HTTP_200_OK)
            return JsonResponse({
                "message": "Validation error",
                "result": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during registration",
                "result":False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingApi(APIView):
    def post(self, request):
        message = 'Success'
        result = True

        try:
            fitness_class_id = request.data.get('fitness_class')
            client_name = request.data.get('client_name')
            client_email = request.data.get('client_email')
            number_of_slots = int(request.data.get('number_of_slots', 1))

            if not all([fitness_class_id, client_name, client_email]):
                return JsonResponse({
                    "message": "All fields (fitness_class, client_name, client_email) are required.",
                    "result": False
                }, status=status.HTTP_400_BAD_REQUEST)

            if number_of_slots < 1:
                return JsonResponse({
                    "message": "Number of slots must be at least 1.",
                    "result": False
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                fitness_class = FitnessClass.objects.get(id=fitness_class_id)
            except FitnessClass.DoesNotExist:
                return JsonResponse({
                    "message": "Fitness class not found.",
                    "result": False
                }, status=status.HTTP_404_NOT_FOUND)

            if fitness_class.available_slot >= number_of_slots:
                status_value = 'Confirmed'
                fitness_class.available_slot -= number_of_slots
                fitness_class.save()
            else:
                status_value = 'Waitlisted'

            booking = Booking.objects.create(
                fitness_class=fitness_class,
                client_name=client_name,
                client_email=client_email,
                number_of_slots=number_of_slots,
                status=status_value
            )

            return JsonResponse({
                "message": f"Booking {status_value} successfully.",
                "result": result,
                "data": {
                    "booking_id": booking.id,
                    "status": booking.status,
                    "slots_requested": number_of_slots
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during booking",
                "result": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingHistoryApi(APIView):
    def get(self, request):
        message = "Success"
        result = True

        try:
            email = request.query_params.get('email')
            if not email:
                return JsonResponse({
                    "message": "Email is required.",
                    "result": False
                }, status=status.HTTP_400_BAD_REQUEST)

            booking_objs = Booking.objects.filter(client_email=email)

            if not booking_objs.exists():
                return JsonResponse({
                    "message": "No booking history found for this email.",
                    "result": False,
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(booking_objs, request)
            
            serializer = BookingSerializer(result_page, many=True)

            return paginator.get_paginated_response({
                "message": message,
                "result": result,
                "data": serializer.data
            })

        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during booking history retrieval",
                "result": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

