from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.SignupPage, name='signup'),
    #path('', views.home, name='home'),
    path('', views.LoginPage, name='login'),
    path('base/', views.dashboard, name='base'),
    # path('base/', views.status, name='base'),
    #path('base/login', views.dashboard, name='base'),
    path('leads/',views.leads,name='leads'),
    path('logout/', views.LogoutPage, name='logout'),
    # path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('delete', views.delete, name='delete'),
    path('add_record/', views.add_record, name='add_record'),

    path('import/',views.imp,name='import'),
    path('show/', views.show_csv, name='show'),
    path('csvSave/', views.csvSave, name='csvSave'),

    #path('show_csv/',views.show_csv,name='show_csv'),

]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
