from django.urls import path
from .views import (
    LoginView, LogoutView, GetUserDetailsView, VoterRegistrationView,
    GetVotersView, GetCandidatesView, GetConstituenciesView, GetVotingOfficersView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_user_details/', GetUserDetailsView.as_view(), name='get_user_details'),
    path('register_voter/', VoterRegistrationView.as_view(), name='register_voter'),
    path('voters/', GetVotersView.as_view(), name='get_voters'),
    path('candidates/', GetCandidatesView.as_view(), name='get_candidates'),
    path('constituencies/', GetConstituenciesView.as_view(), name='get_constituencies'),
    path('voting_officers/', GetVotingOfficersView.as_view(), name='get_voting_officers'),
]