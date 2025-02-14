from rest_framework import serializers
from Users.models import Voter, Candidate, Constituency
from .models import Vote

class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(
        queryset=Voter.objects.all(),         
        error_messages={'does_not_exist': 'Missing User Data.'}
    )
    
    candidate = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(),
        error_messages={'does_not_exist': 'Candidate with the provided ID does not exist.'}
    )
    
    constituency = serializers.PrimaryKeyRelatedField(
        queryset=Constituency.objects.all(),
        error_messages={'does_not_exist': 'Constituency with the provided ID does not exist.'}
    )

    class Meta:
        model = Vote
        fields = ['voter', 'candidate', 'constituency']

    def validate(self, data):
        voter = data.get('voter')
        candidate = data.get('candidate')
        constituency = data.get('constituency')

        # Check that the voter is verified
        # if not voter.verified:
        #     raise serializers.ValidationError({'voter': 'Voter is not verified.'})

        # Check that the candidate and constituency are valid
        if candidate.constituency != constituency:
            raise serializers.ValidationError({'candidate': 'Candidate does not belong to the specified constituency.'})

        # Check that the voter's constituency matches the candidate's constituency
        if voter.constituency != constituency:
            raise serializers.ValidationError({'voter': 'Voter does not belong to the specified constituency.'})

        # Check that the voter has not already cast a vote
        if Vote.objects.filter(voter=voter).exists():
            raise serializers.ValidationError({'voter': 'Voter has already cast a vote.'})

        return data

    def create(self, validated_data):
        vote = Vote.objects.create(**validated_data)
        voter = validated_data.get('voter')
        voter.voted = True
        voter.save()
        return vote