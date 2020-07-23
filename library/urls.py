from django.conf.urls import url
from library import views

urlpatterns = [
    url(r'^publisher/', views.publisher_list, name='publisher'),
    url(r'^publisher_add/', views.publisher_add, name='pub_add'),
    url(r'^publisher_del/', views.publisher_del, name='pub_del'),
    url(r'^publisher_edit/(\d+)/', views.publisher_edit, name='pub_edit'),

    url(r'^book_list/', views.book_list, name='book'),
    url(r'^book_add/', views.book_add, name='book_add'),
    url(r'^book_del/', views.book_del, name='book_del'),
    url(r'^book_edit/', views.book_edit, name='book_edit'),

    url(r'^author_list/', views.author_list, name='author'),
    url(r'^author_add/', views.author_add, name='author_add'),
    url(r'^author_del/', views.author_del, name='author_del'),
    url(r'^author_edit/', views.author_edit, name='author_edit'),

    url(r'^(\w+)_del/(\d+)/', views.delete, name='del'),

    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout')
]