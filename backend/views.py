from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from .models import UserInfo, Permission
from rest_framework.permissions import BasePermission


# 手动创建token
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CheckPermission(BasePermission):
    '''
    接口权限验证
    '''

    @classmethod
    def get_permission_from_role(self, request):
        try:
            perms = request.user.roles.values(
                'permissions__url'
            ).distinct()
            return [p['permissions__url'] for p in perms]
        except AttributeError:
            return None

    message = {
        'data': {
            'data': {
                'message': 1111
            },
            'code': 403,
            'message': 2222
        },
        'message': 33333
    }

    def has_permission(self, request, view):
        """
        判断是否有权限访问当前请求
        Return `True` if permission is granted, `False` otherwise.
        :param request:
        :param view:
        :return: True有权限；False无权限
        """
        perms = self.get_permission_from_role(request)
        current_path = request.path
        if current_path in perms:
            perms_method_type = request.user.roles.filter(permissions__url=current_path).values(
                'permissions__method_type')
            if request.method in [m['permissions__method_type'] for m in perms_method_type]:
                return True


class UserAuthView(APIView):
    '''用户认证获取token'''

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token, 'code': 20000})
        else:
            return Response({'message': '用户名或密码错误', 'code': 400})


class UserInfoView(APIView):
    '''获取用户信息'''

    def get(self, request):
        if request.user.id is not None:
            data = {
                'id': request.user.id,
                'name': request.user.username,
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'introduction': 'I am a super administrator',
                'is_active': request.user.is_active,
                'createTime': request.user.date_joined,
                'email': request.user.email,
                'roles': ['admin']  # TODO 权限角色设计
            }
            return Response({'data': data, 'code': 20000})
        else:
            return Response({'message': '请登录后访问', 'code': 50008})


# class UserLogoutView(APIView):
#     '''用户登出'''
#     def post(self,request,*args, **kwargs):

class UserHandlerView(APIView):
    '''用户管理'''

    def get(self, request, *args, **kwargs):
        page_size = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        value = request.query_params.get('title', None)
        key = request.query_params.get('type', None)
        limit_start = (page_size - 1) * limit
        if key and value:
            count = UserInfo.objects.filter(**{key: value}).count()
            user_info = UserInfo.objects.filter(**{key: value}).order_by('id')[limit_start:limit]
            serializer = UserInfoSerializer(user_info, many=True)
        else:
            count = UserInfo.objects.all().count()
            user_info = UserInfo.objects.all()[limit_start:limit]
            serializer = UserInfoSerializer(user_info, many=True)
        return Response({
            'data': serializer.data,
            'code': 20000,
            'count': count
        })

    def post(self, request, *args, **kwargs):
        isActive = request.data.get('is_active')
        if isActive == '激活':
            request.data['is_active'] = 1
        else:
            request.data['is_active'] = 0
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'code': 20000,
            })
        return Response({
            'message': serializer.errors,
            'code': 400
        })

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        if user_id:
            user_info = UserInfo.objects.get(id=user_id)
            if user_info.roles.all()[0].name == 'admin':
                return Response({
                    'message': '系统管理员无法删除',
                    'code': 400
                })
            try:
                user_info.delete()
            except Exception as e:
                return Response({
                    'message': "数据删除失败:" + e,
                    'code': 400
                })
            return Response({
                'code': 20000,
                'data': 'success'
            }
            )

    def put(self, request, *args, **kwargs):
        isActive = request.data.get('is_active')
        if isActive == '激活':
            request.data['is_active'] = 1
        else:
            request.data['is_active'] = 0
        print(request.data)
        user_id = request.data.get('id', None)
        if user_id:
            user_info = UserInfo.objects.get(id=user_id)
            serializer = UserModifySerializer(user_info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'code': 20000,
                })
            return Response({
                'message': serializer.errors,
                'code': 400
            })


class FuncHandlerView(APIView):
    '''
    权限管理
    '''
    permission_classes = [CheckPermission, ]

    def get(self, request, *args, **kwargs):
        page_size = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        value = request.query_params.get('title', None)
        key = request.query_params.get('type', None)
        limit_start = (page_size - 1) * limit
        limit_end = page_size * limit
        if key and value:
            count = Permission.objects.filter(**{key: value}).count()
            perm_info = Permission.objects.filter(**{key: value}).order_by('id')[limit_start:limit_end]
            serializer = PermissionSerializer(perm_info, many=True)
        else:
            count = Permission.objects.all().count()
            perm_info = Permission.objects.all()[limit_start:limit_end]
            serializer = PermissionSerializer(perm_info, many=True)
        return Response({
            'data': serializer.data,
            'code': 20000,
            'count': count
        })

    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'code': 20000,
            })
        return Response({
            'message': serializer.errors,
            'code': 400
        })

    def put(self, request, *args, **kwargs):
        func_id = request.data.get('id', None)
        if func_id:
            func_info = Permission.objects.get(id=func_id)
            serializer = PermissionSerializer(func_info, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'code': 20000,
                })
            return Response({
                'message': serializer.errors,
                'code': 400
            })

    def delete(self, request, *args, **kwargs):
        func_id = request.data.get('func_id', None)
        if func_id:
            func_info = Permission.objects.get(id=func_id)
            try:
                func_info.delete()
            except Exception as e:
                return Response({
                    'message': "数据删除失败:" + e,
                    'code': 400
                })
            return Response({
                'code': 20000,
                'data': 'success'
            }
            )
