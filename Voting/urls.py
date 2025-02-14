from django.urls import path
from .views import CastVoteView, AnalyticsView

urlpatterns = [
    path('cast_vote/', CastVoteView.as_view(), name='cast_vote'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]