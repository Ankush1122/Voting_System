from django.db import models
from Users.models import Voter, Candidate, Constituency

class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE, primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"Vote by {self.voter.name} for {self.candidate.name} in {self.constituency.name}"
