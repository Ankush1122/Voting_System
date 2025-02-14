from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserCredentials, Voter, VotingOfficer, Candidate, Constituency
from .serializers import LoginSerializer, VotingOfficerListSerializer, VoterSerializer, VoterListSerializer, ConstituencySerializer, CandidateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView


def get_user_details(mobile):
    """
    Returns a tuple (user_type, user_data) for the given mobile number.
    """
    try:
        user_credentials = UserCredentials.objects.get(mobile=mobile)
        # print(user_credentials)
    except UserCredentials.DoesNotExist:
        return None, None

    try:
        user = Voter.objects.get(user_credentials=user_credentials)
        # print(user)
        user_type = 'Voter'
        user_data = {
            'name': user.name,
            'aadhar_number': user.aadhar_number,
            'mobile': user_credentials.mobile,
            'constituency': user.constituency.constituency_id,
            'voted': user.voted,
            'age': user.age,
            'gender': user.gender,
        }
    except Voter.DoesNotExist:
        try:
            user = VotingOfficer.objects.get(user_credentials=user_credentials)
            user_type = 'VotingOfficer'
            user_data = {
                'name': user.name,
                'voting_officer_id': user.voting_officer_id,
                'mobile': user_credentials.mobile,
                'experience': user.experience,
                'designation': user.designation,
            }
        except VotingOfficer.DoesNotExist:
            user_type = None
            user_data = {}
    return user_type, user_data


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        # Check if any user is already authenticated in this session
        if 'mobile' in request.session:
            # User is already logged in on this device/session
            
            mobile = request.session['mobile']
            user_type, user_data = get_user_details(mobile)
            if user_type is None:
                return Response({'error': 'User associated data not found.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'User already logged in', 'user_type': user_type, 'user': user_data}, status=status.HTTP_200_OK)

        # No user is authenticated in this session, proceed with login
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            password = serializer.validated_data['password']

            # Authenticate the user
            try:
                user_credentials = UserCredentials.objects.get(mobile=mobile)
                if password != user_credentials.password:
                    return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
            except UserCredentials.DoesNotExist:
                return Response({'error': 'User does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Log in the user and create a session
            request.session['mobile'] = mobile  # Store the mobile number in session

            # Retrieve user details
            user_type, user_data = get_user_details(mobile)
            if user_type is None:
                return Response({'error': 'User associated data not found.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Login successful', 'user_type': user_type, 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        # print("\n\n\nlogout\n\n\n")
        # Check if any user is authenticated in this session
        if 'mobile' in request.session:
            # Log out the user and flush the session
            request.session.flush()  # Ensure all session data is cleared
            response= Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
            response.delete_cookie(settings.SESSION_COOKIE_NAME, path = '/')
            return response
        else:
            return Response({'error': 'Not logged in.'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class GetUserDetailsView(APIView):
    def get(self, request):
        # Check if any user is authenticated in this session
        if 'mobile' in request.session:
            mobile = request.session['mobile']
            user_type, user_data = get_user_details(mobile)
            if user_type is None:
                return Response({'error': 'User associated data not found.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'user_type': user_type, 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No active session for the user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
# Voter Registration View
class VoterRegistrationView(APIView):
    def post(self, request):
        serializer = VoterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Voter registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get Voters View
class GetVotersView(ListAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterListSerializer

# Get Candidates View
class GetCandidatesView(ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

# Get Constituencies View
class GetConstituenciesView(ListAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer

# Get Voting Officers View
class GetVotingOfficersView(ListAPIView):
    queryset = VotingOfficer.objects.all()
    serializer_class = VotingOfficerListSerializer