from .models import *
from rest_framework import serializers
from django.utils.timezone import localtime


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
    instructor_id = serializers.PrimaryKeyRelatedField(
        source='instructor', queryset=CustomUser.objects.all(), write_only=True
    )
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'instructor', 'instructor_id', 'max_capacity', 'available_slot']


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['start_time'] = localtime(instance.start_time).isoformat() if instance.start_time else None
        rep['end_time'] = localtime(instance.end_time).isoformat() if instance.end_time else None
        return rep

class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

