from django.urls import path

from .analytics_reports import (
    TestReportView
)

app_name = "analytics"

urlpatterns = (
    path('matrix-report/',
         TestReportView.as_view(),
         name='matrix-report'),

)
