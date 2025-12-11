from rest_framework import serializers
from elections.models import Election, Position, Candidate, Vote


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'description']


class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = ['id', 'name', 'max_choices', 'candidates']


class ElectionSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start', 'end', 'anonymous', 'positions']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'election', 'position', 'candidate', 'voter', 'timestamp']
        read_only_fields = ['id', 'timestamp']
