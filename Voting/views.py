from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Users.models import UserCredentials, Voter, VotingOfficer, Constituency, Candidate
from .serializers import VoteSerializer
from .models import Vote

class CastVoteView(APIView):
    def post(self, request):
        # Check if the voter is logged in
        if 'mobile' not in request.session:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)

        mobile = request.session['mobile']

        # Get the voter instance
        try:
            user_credentials = UserCredentials.objects.get(mobile=mobile)
            voter = Voter.objects.get(user_credentials=user_credentials)
        except (UserCredentials.DoesNotExist, Voter.DoesNotExist):
            return Response({'error': 'Voter not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Include the voter in the data
        data = request.data.copy()
        data['voter'] = voter.pk

        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Vote cast successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class AnalyticsView(APIView):
    def get(self, request):
        # Check if user is logged in
        if 'mobile' not in request.session:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        mobile = request.session['mobile']
        
        # Check if user is a VotingOfficer
        try:
            user_credentials = UserCredentials.objects.get(mobile=mobile)
            voting_officer = VotingOfficer.objects.get(user_credentials=user_credentials)
        except (UserCredentials.DoesNotExist, VotingOfficer.DoesNotExist):
            return Response({'error': 'Access denied. Only Voting Officers can access this API.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Proceed to compute analytics
        analytics_data = []
        constituencies = Constituency.objects.all()
        
        for constituency in constituencies:
            constituency_data = {}
            constituency_data['constituency_id'] = constituency.constituency_id
            constituency_data['constituency_name'] = constituency.name
            constituency_data['district'] = constituency.district
            constituency_data['state'] = constituency.state
            
            # Candidates and their vote counts
            candidates = Candidate.objects.filter(constituency=constituency)
            candidate_data = []
            for candidate in candidates:
                vote_count = Vote.objects.filter(candidate=candidate).count()
                candidate_data.append({
                    'candidate_id': candidate.candidate_id,
                    'name': candidate.name,
                    'political_party': candidate.political_party,
                    'vote_count': vote_count
                })
            constituency_data['candidates'] = candidate_data
            
            # Total voters in the constituency
            total_voters = Voter.objects.filter(constituency=constituency).count()
            constituency_data['total_voters'] = total_voters
            
            # Number of votes cast
            votes_cast = Vote.objects.filter(constituency=constituency).count()
            constituency_data['votes_cast'] = votes_cast
            
            # Percentage voting (voter turnout)
            turnout_percentage = (votes_cast / total_voters * 100) if total_voters > 0 else 100
            constituency_data['voter_turnout_percentage'] = round(turnout_percentage, 2)
            
            # Male and Female voting percentages
            male_voters = Voter.objects.filter(constituency=constituency, gender='Male').count()
            female_voters = Voter.objects.filter(constituency=constituency, gender='Female').count()
            other_voters = Voter.objects.filter(constituency=constituency, gender='Other').count()
            
            male_votes = Vote.objects.filter(
                constituency=constituency,
                voter__gender='Male'
            ).count()
            female_votes = Vote.objects.filter(
                constituency=constituency,
                voter__gender='Female'
            ).count()
            other_votes = Vote.objects.filter(
                constituency=constituency,
                voter__gender='Other'
            ).count()
            
            male_voting_percentage = (male_votes / male_voters * 100) if male_voters > 0 else 100
            female_voting_percentage = (female_votes / female_voters * 100) if female_voters > 0 else 100
            other_voting_percentage = (other_votes / other_voters * 100) if other_voters > 0 else 100
            
            constituency_data['male_voting_percentage'] = round(male_voting_percentage, 2)
            constituency_data['female_voting_percentage'] = round(female_voting_percentage, 2)
            constituency_data['other_voting_percentage'] = round(other_voting_percentage, 2)
            
            # Votes cast in different age groups
            age_groups = [
                {'age_min': 18, 'age_max': 25, 'label': '18-25'},
                {'age_min': 26, 'age_max': 35, 'label': '26-35'},
                {'age_min': 36, 'age_max': 45, 'label': '36-45'},
                {'age_min': 46, 'age_max': 60, 'label': '46-60'},
                {'age_min': 61, 'age_max': 200, 'label': '61+'},
            ]
            age_group_data = []
            for group in age_groups:
                voters_in_group = Voter.objects.filter(
                    constituency=constituency,
                    age__gte=group['age_min'],
                    age__lte=group['age_max']
                ).count()
                
                votes_in_group = Vote.objects.filter(
                    constituency=constituency,
                    voter__age__gte=group['age_min'],
                    voter__age__lte=group['age_max']
                ).count()
                
                voting_percentage = (votes_in_group / voters_in_group * 100) if voters_in_group > 0 else 100
                
                age_group_data.append({
                    'age_group': group['label'],
                    'voting_percentage': round(voting_percentage, 2)
                })
            constituency_data['age_group_voting'] = age_group_data
            
            analytics_data.append(constituency_data)
        
        return Response(analytics_data, status=status.HTTP_200_OK)