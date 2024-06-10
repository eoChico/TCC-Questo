"""
URL configuration for Questo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard import views




urlpatterns = [
    path('',views.home,name="home"),
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),

    path('accounts/flashcards/', views.flashcards, name='flashcards'),
    path('accounts/flashcards_details/<int:deck_id>/', views.flashcards_details, name='flashcards_details'),
    path('flashcards/delete/<int:deck_id>/', views.delete_deck, name='delete_deck'),
    path('flashcards/edit/<int:deck_id>/', views.edit_deck, name='edit_deck'),
    path('flashcard/delete/<int:id>/', views.delete_flashcard, name='delete_flashcard'),
    path('flashcard/edit/<int:id>/', views.edit_flashcard, name='edit_flashcard'),

    path('accounts/calendar/', views.calendar, name='calendar'),
    path('detalhes_event/', views.detalhes_event, name='detalhes_event'),
    path('edit_event/', views.edit_event, name='edit_event'),
    path('delete_event/', views.delete_event, name='delete_event'),

    path('accounts/exams/', views.exams, name='exams'),
    path('vestibulares/<int:pk>/', views.vestibulares, name='vestibulares'),
    path('provas/<int:pk>/', views.provas, name='provas'),

    path('accounts/planner/', views.planner, name='planner'),
    path('deletar-planejamentos/', views.deletar_planejamentos, name='deletar_planejamentos'),

    path('accounts/funcionalidades/', views.funcionalidades, name='funcionalidades'),

   
]
