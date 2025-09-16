from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User, CRAssignment
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, CRAssignmentSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint."""
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def demo_login_view(request):
    """Demo login endpoint for prototype."""
    email = request.data.get('email', '').lower()
    
    # Validate email domain
    if not email.endswith('@giki.edu.pk'):
        return Response(
            {'error': 'Email must be from giki.edu.pk domain'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create user
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],  # Use email prefix as username
            'is_active': True,
        }
    )
    
    if created:
        user.set_password('demo123')  # Demo password
        user.save()
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile endpoint."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Admin Views for CR Management
class CRAssignmentListCreateView(generics.ListCreateAPIView):
    """List and create CR assignments (Admin only)."""
    queryset = CRAssignment.objects.all()
    serializer_class = CRAssignmentSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        """Create CR assignment with current admin as assigner."""
        serializer.save(assigned_by=self.request.user)


class CRAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete CR assignment (Admin only)."""
    queryset = CRAssignment.objects.all()
    serializer_class = CRAssignmentSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_cr_view(request):
    """Assign CR role to an email (Admin only)."""
    email = request.data.get('email', '').lower()
    
    if not email.endswith('@giki.edu.pk'):
        return Response(
            {'error': 'Email must be from giki.edu.pk domain'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if already assigned
    if CRAssignment.objects.filter(email=email, is_active=True).exists():
        return Response(
            {'error': 'This email is already assigned as CR'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create CR assignment
    cr_assignment = CRAssignment.objects.create(
        email=email,
        assigned_by=request.user
    )
    
    # Update existing user if exists
    try:
        user = User.objects.get(email=email)
        user.save()  # This will auto-assign CR role
    except User.DoesNotExist:
        pass  # User will get CR role when they sign up
    
    serializer = CRAssignmentSerializer(cr_assignment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def revoke_cr_view(request):
    """Revoke CR role from an email (Admin only)."""
    email = request.data.get('email', '').lower()
    
    try:
        cr_assignment = CRAssignment.objects.get(email=email, is_active=True)
        cr_assignment.is_active = False
        cr_assignment.save()
        
        # Update existing user if exists
        try:
            user = User.objects.get(email=email)
            user.save()  # This will auto-assign student role
        except User.DoesNotExist:
            pass
        
        return Response({'message': 'CR role revoked successfully'})
    except CRAssignment.DoesNotExist:
        return Response(
            {'error': 'CR assignment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def cr_assignments_view(request):
    """Get all CR assignments (Admin only)."""
    assignments = CRAssignment.objects.all()
    serializer = CRAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)
