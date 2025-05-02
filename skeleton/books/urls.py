from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:book_pk>/", views.detail, name="detail"),
    path('<int:book_pk>/thread/create', views.thread_create, name='thread_create'),
    path(
        '<int:book_pk>/thread/<int:thread_pk>/',
        views.thread_detail,
        name='thread_detail',
    ),
    path(
        '<int:book_pk>/thread/<int:thread_pk>/update/',
        views.thread_update,
        name='thread_update',
    ),
    path(
        '<int:book_pk>/thread/<int:thread_pk>/delete/',
        views.thread_delete,
        name='thread_delete',
    ),
    path(
        '<int:book_pk>/thread/<int:thread_pk>/likes/',
        views.likes,
        name='likes',
    ),
     path(
        '<int:book_pk>/comment/<int:thread_pk>/create/',
        views.create_comment,
        name='create_comment',
    ),
    path(
        '<int:book_pk>/comment/<int:comment_pk>/delete/',
        views.delete_comment,
        name='delete_comment',
    ),
    path("filter-category/", views.filter_category, name="filter_category"),
]
