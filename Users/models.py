from django.db import models

class UserCredentials(models.Model):
    mobile = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=255)

    class Meta:
        verbose_name = "UserCredential"
        verbose_name_plural = "UserCredentials"

    def __str__(self):
        return self.mobile
    

class Constituency(models.Model):
    name = models.CharField(max_length=100)
    constituency_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    population = models.IntegerField(null=True, blank=True)    
    
    class Meta:
        verbose_name = "Constituency"
        verbose_name_plural = "Constituencies"

    def __str__(self):
        return f"{self.name}, {self.state}"


class Voter(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12, primary_key=True)
    user_credentials = models.OneToOneField(UserCredentials, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    class Meta:
        verbose_name = "Voter"
        verbose_name_plural = "Voters"
        
    def __str__(self):
        return f"{self.name} ({self.aadhar_number})"


class Candidate(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    candidate_id = models.AutoField(primary_key=True)
    user_credentials = models.OneToOneField(UserCredentials, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    political_party = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    manifesto = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.name} ({self.political_party})"


class VotingOfficer(models.Model):
    name = models.CharField(max_length=100)
    voting_officer_id = models.AutoField(primary_key=True)
    user_credentials = models.OneToOneField(UserCredentials, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(null=True, blank=True)
    designation = models.CharField(max_length=100, default="Voting Officer")
    
    class Meta:
        verbose_name = "VotingOfficer"
        verbose_name_plural = "VotingOfficers"

    def __str__(self):
        return f"{self.name} (ID: {self.voting_officer_id})"
