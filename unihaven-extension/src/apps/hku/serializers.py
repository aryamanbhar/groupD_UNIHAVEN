from rest_framework import serializers
from .models import (
    CedarsSpecialist, Accommodation, Student, Reservation,
    Contract, Rating
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
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = [
            "property_id", "property_name", "image", "type", "owner_info", "longitude", "latitude",
            "area", "distance", "price", "number_of_beds", "number_of_bedrooms",
            "availability_start", "availability_end", "create_date", "status",
            "room_number", "flat_number", "floor_number", "geo_address", "average_rating"
            # "cedars_specialist"
        ]
        read_only_fields = ["property_id"]

    def get_average_rating(self, obj):
        return obj.average_rating()  # <-- Call the method to get the value

class AccommodationRatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=0, max_value=5)

    def validate(self, data):
        # you can add extra validation if needed
        return data


class StudentSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Student
        fields = ["student_id", "name", "contact"]


class ReservationSerializer(serializers.ModelSerializer):

    # accept a student_id in payload instead of nested student object
    # student_id = serializers.CharField(write_only=True)

    name = serializers.CharField(source='student.name')
    contact = serializers.CharField(source='student.contact')
    student_id = serializers.CharField(source='student.student_id')
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = ['reservation_id', 'name', 'contact', 'student_id', 'accommodation', 'start_date', 'end_date', 'status']
        # read_only_fields = ['student_id']

    def validate(self, data):
        # Check that reservation dates fall within accommodation availability
        accommodation = data.get('accommodation')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date < accommodation.availability_start or end_date > accommodation.availability_end:
            raise serializers.ValidationError(
                "Reservation dates must be within the accommodation's availability period."
            )
        if start_date > end_date:
            raise serializers.ValidationError(
                "Start date must be before or equal to end date."
            )
        return data

    def create(self, validated_data):
        # get or create the student by provided student_id
        student_data = validated_data.pop('student')
        sid = student_data['student_id']      
        name = student_data.get('name')
        contact = student_data.get('contact') 

        try:
            student = Student.objects.get(student_id=sid)
        except Student.DoesNotExist:
            # If student doesn't exist, create a new one
            student = Student.objects.create(student_id=sid, name=name, contact=contact)

        # student, _ = Student.objects.get_or_create(student_id=sid, defaults={'name': name, 'contact': contact})
        reservation = Reservation.objects.create(student=student, **validated_data)
        return reservation


class ContractSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = Contract
        fields = ["contract_id", "reservation", "date", "contract_status"]

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