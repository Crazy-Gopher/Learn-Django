from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('book_ticket/book/', views.book, name='book'),
    path('cancel_ticket/', views.cancel_ticket, name='cancel_ticket'),
    path('cancel_ticket/cancel/', views.cancel, name='cancel'),
    path('print_booked_ticket/', views.print_booked_ticket, name = 'print_booked_ticket'),
    path('print_available_ticket/', views.print_available_ticket, name = 'print_available_ticket'),
]
