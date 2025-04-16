from rest_framework import serializers
from .models import (
    CedarsSpecialist, Accommodation, Student, Reservation,
    Contract, Rating, Notification
)

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "email", "phone", "created_at"]

class CedarsSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CedarsSpecialist
        fields = ["email","cedars_specialist_id"]

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
    # user = UserSerializer()

    class Meta:
        model = Student
        fields = ["student_id", "name", "degree_type"]

class ReservationSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    accommodation = serializers.PrimaryKeyRelatedField(queryset=Accommodation.objects.filter(status="available"), write_only=True)
    accommodation_name = serializers.StringRelatedField(source='accommodation', read_only=True)

    class Meta:
        model = Reservation
        fields = ["student_id", "accommodation", "status", "accommodation_name"]
        read_only_fields = ["status", "accommodation_name"]

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        student = Student.objects.get(id=student_id)
        
        reservation = Reservation.objects.create(
            student=student,
            status="reserved",
            accommodation=validated_data['accommodation']
        )
        return reservation

    def to_representation(self, instance):
        return {
            "student_id": instance.student.id,
            "status": instance.status,
            "accommodation_name": instance.accommodation.name
        }

    def validate(self, data):
        accommodation_name = data.get("accommodation")
        student_id = data.get("student_id")

        if accommodation_name.status != "available":
            raise serializers.ValidationError(
                {"accommodation": "This accommodation is not available for reservation."}
            )

        # Check if student exists
        if not Student.objects.filter(id=student_id).exists():
            raise serializers.ValidationError(
                {"student_id": "Student does not exist."}
            )

        # Check if accommodation already has a reservation
        if Reservation.objects.filter(accommodation=accommodation_name).exists():
            raise serializers.ValidationError(
                {"accommodation": "This accommodation is already reserved by another student."}
            )

        return data


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
    score = serializers.IntegerField(min_value=1, max_value=5)
    
    class Meta:
        model = Rating
        fields = "__all__"
        read_only_fields = ('student', 'accommodation', 'created_at', 'updated_at')
        
# class NotificationSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     cedars_specialist = CedarsSpecialistSerializer()

#     class Meta:
#         model = Notification
#         fields = ["id", "user", "detail", "is_read", "cedars_specialist"]
