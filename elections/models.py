from django.conf import settings
from django.db import models


class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    anonymous = models.BooleanField(default=True)  # if False, keep audit trail

    def __str__(self):
        return self.title


class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=200)
    max_choices = models.PositiveSmallIntegerField(default=1)  # allow multiple-choice positions

    def __str__(self):
        return f"{self.election.title} - {self.name}"


class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.position.name})"


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('election', 'position', 'voter')  # prevents duplicate votes per position per voter

    def __str__(self):
        return f"Vote: {self.election} / {self.position} -> {self.candidate}"
