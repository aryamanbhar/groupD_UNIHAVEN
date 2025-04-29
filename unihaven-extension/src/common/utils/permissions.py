# permissions.py
from rest_framework.permissions import BasePermission

class IsHKU(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return university == "HKU"

class IsCUHK(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return university == "CUHK"
    
class IsHKUST(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return university == "HKUST"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return role == "admin"
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return role == "student"

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.payload.get("role")
        university = request.auth.payload.get("university")
        return role == "staff"
    
