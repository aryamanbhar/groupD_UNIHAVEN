from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .utils.authentication import create_custom_token
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from apps.users.models import CustomUser

class LoginView(APIView):
    """
    Custom login view to authenticate users and generate a custom token
    with university and role information.
    """
    def post(self, request):
        # Extract username, password, and university from the request
        username = request.data.get('username')
        password = request.data.get('password')
        university = request.data.get('university')  # User-provided university
        role = request.data.get('role', 'student')  # Default role is 'student'

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username or password")

        # Validate the university
        if user.university != university:
            raise AuthenticationFailed("The provided university does not match the user's university")

        # Generate a custom token
        token = create_custom_token(user, university, role)

        # Return the token in the response
        return Response({"token": token})
    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        university = request.data.get('university')  


        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            university=university  # Save the university field
        )

        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

# class RatingCreateView(LoginRequiredMixin, CreateView):
#     model = Rating
#     form_class = RatingForm
#     template_name = 'ratings/create.html'

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         contract = Contract.objects.get(
#             accommodation=form.cleaned_data['accommodation'],
#             user=self.request.user,
#             status='signed'
#         )
#         rating = form.save(commit=False)
#         rating.user = self.request.user
#         rating.contract = contract
#         rating.save()
        
#         images = self.request.FILES.getlist('images')
#         for image in images:
#             UploadedImage.objects.create(rating=rating, image=image)
            
#         return redirect('rating-list')

# class RatingListView(ListView):
#     model = Rating
#     template_name = 'ratings/list.html'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         accommodation_id = self.request.GET.get('accommodation_id')
#         if accommodation_id:
#             queryset = queryset.filter(accommodation__property_id=accommodation_id)
#         return queryset.order_by('-created_at')
