from django.urls import path
from apps.analytics.views import (
    DashboardStatsView,
    WeeklyChartDataView,
    IntentAnalyticsView,
    MessageFeedbackView,
)

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard'),
    path('weekly-chart/', WeeklyChartDataView.as_view(), name='weekly-chart'),
    path('intents/', IntentAnalyticsView.as_view(), name='intents'),
    path('feedback/', MessageFeedbackView.as_view(), name='feedback'),
]
