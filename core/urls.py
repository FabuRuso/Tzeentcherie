from django.urls import path

from core.views.hello import hello as views_hello

from core.views.register import register as views_register
from core.views.login import login as views_login
from core.views.profile import profile as views_profile
from core.views.debug import release_debug_placeholders as views_debug_rphs
from core.views.ruled import           \
    owned_act     as views_owned_act, \
    not_owned_act as views_not_owned_act, \
    users_act as views_users_act, \
    role_set as views_role_set, \
    role_act as views_role_act, \
    full_list as views_full_list

urlpatterns = [
    path('hello/', views_hello),
    path('register/', views_register),
    path('login/', views_login),
    path('profile/', views_profile),
    path('tzeentcherie/own/<str:title>/', views_owned_act),
    path('tzeentcherie/<str:title>/', views_not_owned_act),
    path('users/<str:email>/', views_users_act),
    path('users/<str:email>/role/', views_role_set),
    path('users/roles/<str:role_name>/', views_role_act),
    path('tzeentcherie/list/', views_full_list),
    path('debug/release/', views_debug_rphs)
]