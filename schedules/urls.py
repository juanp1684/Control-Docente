from django.urls import path
from.views import ScheduleView, ReportView, LoginView, AdminLoginView,home,login_out,login_user, teacher_report


urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule_list'),
    path('id/<int:id>', ScheduleView.as_view(), name='schedule_updates'),
    path('report/', ReportView.as_view(), name='report_creation'),
    path('login/', LoginView.as_view(), name='session login'),
    #path('admin/login/', AdminLoginView.as_view(), name='admin session login'), #no need for this view
    path('home/', home, name="home"),
    path('admin/login/',login_user,name="login2"),
    path('user/logout/', login_out,name="logout"),
    path('docente/',teacher_report, name="reporte"),
    
   
    
]
