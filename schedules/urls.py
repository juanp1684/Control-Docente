from django.urls import path
from.views import ScheduleView, ReportView, LoginView, AdminLoginView,home,login_out,login_user


urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule_list'),
    path('id/<int:id>', ScheduleView.as_view(), name='schedule_updates'),
    path('report/', ReportView.as_view(), name='report_creation'),
    path('login/', LoginView.as_view(), name='session login'),
    path('admin1/login/', AdminLoginView.as_view(), name='admin session login'),
  
    path('home/',home, name="home"),
    path('admin1/login/',login_user,name="login2"),
    path('user/logout/', login_out,name="logout"),
    
]
