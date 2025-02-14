from rest_framework import serializers
from .models import UserCredentials, Voter, VotingOfficer, Constituency, Candidate

class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ['mobile', 'password']

    def validate_mobile(self, value):
        if UserCredentials.objects.filter(mobile=value).exists():
            raise serializers.ValidationError('Mobile number already exists.')
        return value

    def validate_password(self, value):
        # Add password validation logic here (e.g., minimum length, complexity)
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        # Add additional password checks if necessary
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_credentials = UserCredentials(
            mobile=validated_data['mobile'],
            password=password  # Hash the password
        )
        user_credentials.save()
        return user_credentials

class VoterSerializer(serializers.ModelSerializer):
    user_credentials = UserCredentialsSerializer()
    constituency = serializers.PrimaryKeyRelatedField(queryset=Constituency.objects.all())

    class Meta:
        model = Voter
        fields = [
            'name',
            'aadhar_number',
            'user_credentials',
            'constituency',
            'voted',
            'age',
            'gender',
        ]

    def validate_aadhar_number(self, value):
        if Voter.objects.filter(aadhar_number=value).exists():
            raise serializers.ValidationError('Aadhar number already registered.')
        if len(value) != 12 or not value.isdigit():
            raise serializers.ValidationError('Aadhar number must be a 12-digit number.')
        return value

    def validate_gender(self, value):
        valid_genders = [choice[0] for choice in Voter.GENDER_CHOICES]
        if value not in valid_genders:
            raise serializers.ValidationError('Invalid gender.')
        return value

    def create(self, validated_data):
        user_credentials_data = validated_data.pop('user_credentials')

        # Create UserCredentials instance
        user_credentials_serializer = UserCredentialsSerializer(data=user_credentials_data)
        user_credentials_serializer.is_valid(raise_exception=True)
        user_credentials = user_credentials_serializer.save()

        # Create Voter instance
        voter = Voter.objects.create(
            user_credentials=user_credentials,
            **validated_data
        )
        return voter


class VoterListSerializer(serializers.ModelSerializer):
    constituency = serializers.StringRelatedField()
    class Meta:
        model = Voter
        fields = [
            'name',
            'aadhar_number',
            'constituency',
            'age',
            'gender',
            'voted',
        ]

class VotingOfficerSerializer(serializers.ModelSerializer):
    user_credentials = UserCredentialsSerializer()

    class Meta:
        model = VotingOfficer
        fields = [
            'name',
            'voting_officer_id',
            'user_credentials',
            'experience',
            'designation',
        ]
        read_only_fields = ['voting_officer_id']  # AutoField, so it's read-only

    def validate(self, data):
        # Add any additional validation for VotingOfficer here
        return data

    def create(self, validated_data):
        user_credentials_data = validated_data.pop('user_credentials')

        # Create UserCredentials instance
        user_credentials_serializer = UserCredentialsSerializer(data=user_credentials_data)
        user_credentials_serializer.is_valid(raise_exception=True)
        user_credentials = user_credentials_serializer.save()

        # Create VotingOfficer instance
        voting_officer = VotingOfficer.objects.create(
            user_credentials=user_credentials,
            **validated_data
        )
        return voting_officer
    
class VotingOfficerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingOfficer
        fields = [
            'name',
            'voting_officer_id',
            'experience',
            'designation',
        ]

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')

        if not mobile or not password:
            raise serializers.ValidationError('Both mobile and password are required.')

        try:
            user_credentials = UserCredentials.objects.get(mobile=mobile)
        except UserCredentials.DoesNotExist:
            raise serializers.ValidationError('User does not exists.')

        if password != user_credentials.password:
            raise serializers.ValidationError('Invalid password.')

        data['user_credentials'] = user_credentials
        return data
    
class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            'name',
            'constituency_id',
            'district',
            'state',
            'population',
        ]
        
class CandidateSerializer(serializers.ModelSerializer):
    constituency = serializers.StringRelatedField()
    class Meta:
        model = Candidate
        fields = [
            'name',
            'candidate_id',
            'constituency',
            'political_party',
            'age',
            'manifesto',
            'education',
            'gender',
        ]