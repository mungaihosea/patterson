from django.urls import path
from .views import homepage, form, timestamp, timestamp_list, login, dashboard, buttons, icons, table, generate_results, contact, view_reports, generate_reports, logout, profile, report_card, addstuff, student_registration

urlpatterns = [
    path('', homepage, name = "homepage"),
    path('timestamp/',timestamp, name = "timestamp" ),
    path('login/',login, name = "login" ),
    path('timestamp_list/', timestamp_list, name = "timestamp_list"),
    path('dash/', dashboard, name = "dashboard"),
    path('generate_results/', generate_results, name = "generate_results"),
    path('contact/', contact, name = "contact"),
    path('view_reports/', view_reports, name = "view_reports"),
    path('generate_reports/<int:id>/',generate_reports, name = 'generate_reports'),
    path('logout/', logout, name = 'logout'),
    path('profile/', profile, name = 'profile'),
    path('report_card/', report_card, name = 'report_card'),
    path('addstuff/', addstuff, name = 'addstuff'),
    path('student_registration/', student_registration, name = 'student_registration'),
    


    path('buttons/', buttons , name = "buttons"),
    path('form/',form, name = "forms" ),
    path('icons/',icons, name = "icons" ),
    path('table/',table, name = "table" ),
]