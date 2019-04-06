from django.urls import path, include
from django.conf.urls import url

from rest_framework import routers

from . import views



router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'groups',views.GroupViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'), #Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [    
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [  
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [  
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]



# URLs for the REST API http://127.0.0.1:8000/catalog/api/

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns += [
    #path('api/', views.author_list),
    #url(r'^api/(?P<pk>[0-9]+)/$', views.author_detail),
]

#urlpatterns = format_suffix_patterns(urlpatterns)