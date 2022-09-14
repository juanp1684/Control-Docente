from django.views import View
from .models import Schedule
from .models import User
from .models import Report
from django.contrib.auth.hashers import check_password
from django.http.response import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from datetime import datetime
import json
import pytz
import sys
import jwt
sys.path.append("..") # Adds higher directory to python modules path.
from control_API.settings import EMAIL_HOST_USER, SECRET
from .choices import DAY_CHOICES

# Create your views here.

SCHEDULES_MISSING_MESSAGE = "Schedule missing"
UNRELATED_SCHEDULE_MESSAGE = "Schedule not related to this user"
REPORTS_MISSING_MESSAGE = "Report missing"
USER_NOT_FOUND_MESSAGE = "User not found"
INCORRECT_PASSWORD_MESSAGE = "Incorrect password"
REPORT_MAIL_SUBJECT = "Aplicacion control docente"
MISSED_REPORT_MAIL_MESSAGE = "Se detecto la omision de una clase y se genero el respectivo reporte.\nSi desea presentar un motivo para esta falta debe informar que el id asociado a este reporte es el nro. {}\nHorario: {} a {} dia: {}"
FAILED_REPORT_MAIL_MESSAGE = "Parece que tuvo problemas para completar la tarea de control, ya se realizo el reporte correspondiente.\nDe ser este un problema consistente un administrador se contactara con usted"
BOLIVIA_TIMEZONE = pytz.timezone('America/La_Paz')

def failed_auth_response(message="You are not authenticated"):
    failed_auth_response = JsonResponse({'message': message})
    failed_auth_response.status_code = 401
    return failed_auth_response

def bad_request_response(message="Invalid or missing data"):
    bad_request_response = JsonResponse({'message': message})
    bad_request_response.status_code = 400
    return bad_request_response

class ScheduleView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        request_codsis = request.GET.get('codsis')
        if request_codsis != None:
            schedules = list(Schedule.objects.filter(user_id=request_codsis).order_by(
                'day_of_week', 'start_time').values())
            if len(schedules) > 0:
                response = {'message': f"Found Schedules for: {request_codsis}", 'schedules': schedules}
                user = User.objects.get(codsis=request_codsis)
                user.last_connection = datetime.now(BOLIVIA_TIMEZONE)
                user.save()
            else:
                return bad_request_response(f"Schedules missing for codsis: {request_codsis}")
        else:
            schedules = list(Schedule.objects.order_by(
                'day_of_week', 'start_time').values())
            if len(schedules) > 0:
                response = {'message': "Schedules found",
                            'schedules': schedules}
            else:
                response = {'message': SCHEDULES_MISSING_MESSAGE}
        return JsonResponse(response)

    def post(self, request):
        rb = json.loads(request.body)
        users = list(User.objects.filter(codsis=rb['codsis']).values())
        response = {'message': "Invalid codsis, no related user found"}
        if len(users) > 0:
            Schedule.objects.create(user_id=rb['codsis'],
                                    start_time=rb['start_time'], end_time=rb['end_time'], day_of_week=rb['day_of_week'])
            response = {'message': "success"}
        return JsonResponse(response)

    def put(self, request):
        id_to_be_updated = request.GET.get('id')
        rb = json.loads(request.body)
        schedule_found = Schedule.objects.filter(id=id_to_be_updated).first()
        response = {'message': SCHEDULES_MISSING_MESSAGE}
        if schedule_found is not None:
            schedule_found.codsis = rb['codsis']
            schedule_found.start_time = rb['start_time']
            schedule_found.end_time = rb['end_time']
            schedule_found.day_of_week = rb['day_of_week']
            schedule_found.save()
            response = {'message': "Success update"}

        return JsonResponse(response)

    def delete(self, request):
        id_to_be_deleted = request.GET.get('id')
        schedule_found = Schedule.objects.filter(id=id_to_be_deleted).first()
        response = {'message': SCHEDULES_MISSING_MESSAGE}
        if schedule_found is not None:
            schedule_found.delete()
            response = {'message': "Success delete"}

        return JsonResponse(response)


class ReportView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        codsis = request.GET.get('codsis')
        response = {'message': REPORTS_MISSING_MESSAGE}
        if codsis is not None:
            reports = list(Report.objects.filter(user_id=codsis).values())
            if len(reports) > 0:
                response = {'message': "Reports found",
                            'reports': reports}
        else:
            response = {'message': USER_NOT_FOUND_MESSAGE}
        return JsonResponse(response)

    def post(self, request):
        rb = json.loads(request.body)
        reported_user = User.objects.filter(codsis=rb['codsis']).first()
        reported_schedule = Schedule.objects.filter(id=rb['schedule_id'], user_id=rb['codsis']).first()
        if reported_user is None:
            return bad_request_response(USER_NOT_FOUND_MESSAGE)
        if reported_schedule is None:
            return bad_request_response(UNRELATED_SCHEDULE_MESSAGE)

        report = Report.objects.create(user_id=rb['codsis'], schedule_id=rb['schedule_id'],
                        attempts=rb['attempts'], report_type=rb['report_type'], report_time=datetime.now(BOLIVIA_TIMEZONE))
        response = {'message': "success"}
        if (rb['report_type'] == "fallido"):
            send_mail(subject=REPORT_MAIL_SUBJECT,
                message=FAILED_REPORT_MAIL_MESSAGE, recipient_list=[reported_user.contact_mail],
                from_email=EMAIL_HOST_USER)
        elif (rb['report_type'] == "omision"):
            send_mail(subject=REPORT_MAIL_SUBJECT,
                message=MISSED_REPORT_MAIL_MESSAGE.format(report.pk, reported_schedule.start_time, reported_schedule.end_time, DAY_CHOICES[reported_schedule.day_of_week][1]),
                recipient_list=[reported_user.contact_mail], from_email=EMAIL_HOST_USER)
        reported_user.last_connection = datetime.now(BOLIVIA_TIMEZONE)
        reported_user.save()
        return JsonResponse(response)

    def put(self, request):
        pass # Unnecesary for now

    def delete(self, request):
        pass # Unnecesary for now


class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        rb = json.loads(request.body)
        codsis = rb['codsis']
        password = rb['password']
        
        user = User.objects.get(codsis=codsis)

        if user is None:
            return failed_auth_response(message=USER_NOT_FOUND_MESSAGE)

        if user.password is None:
            user.password = password
            user.save()
        elif not check_password(password=password, encoded=user.password):
            return failed_auth_response(message=INCORRECT_PASSWORD_MESSAGE)
        
        payload = {
            'codsis': codsis
        }

        token = jwt.encode(payload, SECRET)

        response = JsonResponse({'message': "success"})
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response

    def get (self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return failed_auth_response()
        try:
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return failed_auth_response()
        return HttpResponse(payload['codsis'])
