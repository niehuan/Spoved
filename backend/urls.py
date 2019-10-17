from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views
app_name = 'api'


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('user/login/', views.UserAuthView.as_view(),name='user_login'),
    path('user/info/', views.UserInfoView.as_view(), name='user_info'),
    # path('user/logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('mg/accounts/user/',views.UserHandlerView.as_view(),name='user_handler'),
    path('mg/accounts/user_all/',views.UserAllHandlerView.as_view(),name='userAll_handler'),
    path('mg/accounts/func/',views.FuncHandlerView.as_view(),name='func_handler'),
    path('mg/accounts/func_all/',views.FuncALLHandlerView.as_view(),name='funcAll_handler'),
    path('mg/accounts/role/',views.RoleHandlerView.as_view(),name='role_handler'),
    path('mg/accounts/role_func/',views.RoleFuncHandlerView.as_view(),name='roleFunc_handler'),
]

