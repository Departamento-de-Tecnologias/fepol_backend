from django.urls import path, include
from event.views import *
from institution.views import *
from user.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', include('api.routers')),
    path('organizacion/<str:pk>/miembros', AllMembersByOrgViewSet.as_view({'get': 'retrive'})),
    path('persona/', PersonList.as_view()),
    path('persona/manager/', PersonView.as_view()),
    path('persona/manager/<str:pk>/', PersonView.as_view()),
    path('profesor/', ProfessorList.as_view()),
    path('estudiante/', StudentList.as_view()),
    path('miembro/', MemberList.as_view()),
    path('rol/', MemberRoleList.as_view()),
    path('auth/login/', AuthToken.as_view()),
    path('auth/login/web/', AuthCookie.as_view()),
]

