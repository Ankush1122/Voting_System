from django.contrib import admin

from .models import UserCredentials, Constituency, Voter, Candidate, VotingOfficer

admin.site.register(UserCredentials)
admin.site.register(Constituency)
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(VotingOfficer)