
from django.urls import path

from . import views

urlpatterns = [
    # /
    path('', views.home, name='home'),
    # TEMPORARY
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),
    # path('calendar', views.calendar, name='calendar'),
    path('users', views.users, name='users'),
    path('approve', views.approve, name='approve'),
    path('email/users-report', views.email_users_report, name='users-report-email'),
    path('email/users-control-approve', views.email_users_control, name='users-control-email'),

]
