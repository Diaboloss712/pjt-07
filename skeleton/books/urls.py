from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    # Index 페이지
    path("", views.index, name="index"),
    
    # 도서 상세 페이지
    path("<int:book_pk>/", views.detail, name="detail"),
    
    # 쓰레드 생성
    path('<int:book_pk>/thread/create/', views.thread_create, name='thread_create'),
    
    # 쓰레드 상세 페이지
    path(
        '<int:book_pk>/thread/<int:thread_pk>/',
        views.thread_detail,
        name='thread_detail',
    ),
    
    # 쓰레드 수정
    path(
        '<int:book_pk>/thread/<int:thread_pk>/update/',
        views.thread_update,
        name='thread_update',
    ),
    
    # 쓰레드 삭제
    path(
        '<int:book_pk>/thread/<int:thread_pk>/delete/',
        views.thread_delete,
        name='thread_delete',
    ),
    
    # 좋아요 처리
    path(
        '<int:book_pk>/thread/<int:thread_pk>/likes/',
        views.likes,
        name='likes',
    ),
    
    # 댓글 생성
    path(
        '<int:book_pk>/comment/<int:thread_pk>/create/',
        views.create_comment,
        name='create_comment',
    ),
    
    # 댓글 삭제
    path(
        '<int:book_pk>/comment/<int:comment_pk>/delete/',
        views.delete_comment,
        name='delete_comment',
    ),
    
    # 장르별 필터링
    path("filter-category/", views.filter_category, name="filter_category"),
]
