from django.urls import path
from . import views


app_name = 'repositories'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('lockers/', views.lockers, name='lockers'),
    path('locker/new/', views.LockerCreateView.as_view(), name='locker_new'),
    path('locker/<int:pk>/edit/', views.LockerUpdateView.as_view(), name='locker_edit'),
    path('locker/<int:pk>/delete/', views.LockerDeleteView.as_view(), name='locker_delete'),
    path('locker/<int:pk>/detail/', views.LockerDetailView.as_view(), name='locker_detail'),

    path('locker/<int:locker_pk>/folders/', views.FoldersView.as_view(), name='folders'),
    path('locker/<int:locker_pk>/folder/new/', views.FolderView.as_view(), name='folder_new'),
    path('locker/<int:locker_pk>/folder/<int:pk>/edit/', views.FolderView.as_view(), name='folder_edit'),
    path('locker/<int:locker_pk>/folder/<int:pk>/delete', views.FolderDeleteView.as_view(), name='folder_delete'),

    path('locker/<int:locker_pk>/folder/<int:folder_pk>/documents/', views.DocumentsView.as_view(), name='documents'),
    path('locker/<int:locker_pk>/folder/<int:folder_pk>/document/new/', views.DocumentView.as_view(), name='document_new'),
    path('locker/<int:locker_pk>/folder/<int:folder_pk>/document/<int:pk>/edit/', views.DocumentView.as_view(), name='document_edit'),
    path('locker/<int:locker_pk>/folder/<int:folder_pk>/document/<int:pk>/delete/', views.DocumenteDeleteView.as_view(), name='document_delete'),
]
