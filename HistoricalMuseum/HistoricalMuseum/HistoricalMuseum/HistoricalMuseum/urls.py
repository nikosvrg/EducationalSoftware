from django.contrib import admin
from django.urls import path,  include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from HistoryMuseum import views
import nested_admin
from users.views import register, profile

urlpatterns = [

    path('', views.homepage, name='homepage'),

    #admin and auth pages
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('nested_admin', include('nested_admin.urls')),

    #work on theory
    path('hero/', views.HeroPageView.as_view(), name='hero'),
    path('hero/<int:hero_id>', views.TheoryPageView.as_view(), name='hero_theory'),
    path('hero/', views.HeroRedirectView.as_view, name='hero-main'),
    path('hero/test/', views.TestRedirectView.as_view(), name='test-main'),
    path('hero/test/<int:id>', views.TestPageView.as_view(), name='test'),
    path('hero/passed/', views.PassedView.as_view(), name='passed'),
    path('hero/not_passed/', views.NotPassedView.as_view(), name='not_passed')
    ] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)