from .models import *
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']

class UserDetailSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserDetail
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    userdetail = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'userdetail']

    def get_userdetail(self, obj):
        try:
            detail = UserDetail.objects.get(user=obj)
            return UserDetailSerializer(detail).data
        except UserDetail.DoesNotExist:
            return None

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = FitnessClass
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

