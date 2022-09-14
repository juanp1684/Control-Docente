from django.urls import path
from.views import ScheduleView, ReportView, LoginView

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule_list'),
    path('id/<int:id>', ScheduleView.as_view(), name='schedule_updates'),
    path('report/', ReportView.as_view(), name='report_creation'),
    path('login/', LoginView.as_view(), name='session login')
]
