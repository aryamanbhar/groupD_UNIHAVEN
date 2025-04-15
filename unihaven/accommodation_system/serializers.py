from rest_framework import serializers
from .models import (
    User, CedarsSpecialist, Accommodation, Student, Reservation,
    Contract, Rating, Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "created_at"]

class CedarsSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CedarsSpecialist
        fields = ["id", "department"]

class AccommodationSerializer(serializers.ModelSerializer):
    # cedars_specialist = CedarsSpecialistSerializer()

    class Meta:
        model = Accommodation
        fields = [
            "id", "name", "image", "type", "owner_info", "longitude", "latitude",
            "area", "distance", "price", "number_of_beds", "number_of_bedrooms",
            "availability_start", "availability_end", "create_date", "status",
            # "cedars_specialist"
        ]

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ["id", "user", "name", "degree_type"]

class ReservationSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'

# class ReservationSerializer(serializers.ModelSerializer):
#     student = StudentSerializer()
#     accommodation = AccommodationSerializer()

#     class Meta:
#         model = Reservation
#         fields = ["id", "student", "accommodation", "status"]

class ContractSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = Contract
        fields = ["id", "reservation", "date", "document", "signed_at", "contract_status"]

class RatingSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    accommodation = AccommodationSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ["id", "student", "accommodation", "score", "comment", "photo", "created_at", "updated_at"]
        read_only_fields = ["student", "accommodation", "created_at"]
        
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cedars_specialist = CedarsSpecialistSerializer()

    class Meta:
        model = Notification
        fields = ["id", "user", "detail", "is_read", "cedars_specialist"]
