from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from elections.models import Election, Position, Candidate, Vote
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer, VoteSerializer


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated  # extend for role checking


class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.AllowAny]


class VoteViewSet(viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsStudent]

    @action(detail=False, methods=['post'])
    def cast(self, request):
        """
        Payload: { "election": id, "position": id, "candidate": id }
        """
        user = request.user
        election_id = request.data.get('election')
        position_id = request.data.get('position')
        candidate_id = request.data.get('candidate')

        # Basic validation
        try:
            election = Election.objects.get(pk=election_id)
            position = Position.objects.get(pk=position_id, election=election)
            candidate = Candidate.objects.get(pk=candidate_id, position=position)
        except (Election.DoesNotExist, Position.DoesNotExist, Candidate.DoesNotExist):
            return Response({"detail": "Invalid election/position/candidate"}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        if not (election.start <= now <= election.end):
            return Response({"detail": "Election not active"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already voted for this position (unique_together enforces but we catch earlier)
        if Vote.objects.filter(election=election, position=position, voter=user).exists():
            return Response({"detail": "You have already voted for this position"}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.create(
            election=election,
            position=position,
            candidate=candidate,
            voter=user if not election.anonymous else None
        )
        return Response(self.get_serializer(vote).data, status=status.HTTP_201_CREATED)
