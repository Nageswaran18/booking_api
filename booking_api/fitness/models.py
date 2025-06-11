from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Client', 'Client'),
        ('Instructor', 'Instructor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class UserDetail(models.Model):
    GENDER_STATUS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER_STATUS, max_length=10)
    profile_picture = models.ImageField(blank=True, null=True)
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructor_classes')
    max_capacity = models.IntegerField(default=5)
    available_slot = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    # @property
    # def available_slots(self):
    #     return self.max_capacity - self.booking_set.filter(status='confirmed').count()



class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Waitlisted', 'Waitlisted'),
    ]
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.CharField(max_length=100)
    number_of_slots = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return str(self.id)




