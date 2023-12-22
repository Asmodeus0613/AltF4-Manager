from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home', views.home, name='home'),
    path('car', views.cars, name='cars'),
    path('about/', views.about, name='about'),
    path('login/', LoginView.as_view(template_name='RentACar/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('api/get-username/', views.get_username, name='get-username'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cart/<int:car_id>/', views.cart, name='cart'),
    path('carman.html', views.car_management, name='car_management'),
    path('car/add/', views.add_car, name='add_car'),
    path('update_car/<int:car_id>/', views.update_car, name='update_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('create_order/', views.create_order, name='create_order'),
    path('reserve/<int:car_id>/', views.reserve_car, name='reserve_car'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_tracker/', views.order_tracker, name='order_tracker'),
    path('update_order/', views.update_order, name='update_order'),
    path('check_order_status/', views.check_order_status, name='check_order_status'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)