from .models import *
from rest_framework import serializers
import re

class UserInfoSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    tel = serializers.CharField(max_length=11,allow_blank=True)

    class Meta:
        model = UserInfo
        fields = ['id','username','is_superuser','email',
                  'is_active','roles','department','tel',
                  'password'
                  ]

    def validate_username(self, username):
        if UserInfo.objects.filter(username=username):
            raise serializers.ValidationError('账号已存在')
        return username

    def validate_mobile(self, tel):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, tel):
            raise serializers.ValidationError("手机号码不合法")
        if UserInfo.objects.filter(tel=tel):
            raise serializers.ValidationError("手机号已经被注册")
        return tel

    def create(self, validated_data):
        instance = super(UserInfoSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserModifySerializer(serializers.ModelSerializer):
    '''
    修改用户的序列化
    '''
    tel = serializers.CharField(max_length=11, allow_blank=True)

    class Meta:
        model = UserInfo
        fields = ['id','username','is_superuser','email',
                  'is_active','roles','department','tel',
                  'password'
                  ]

    def validate_mobile(self, tel):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, tel):
            raise serializers.ValidationError("手机号码不合法")
        return tel

class PermissionSerializer(serializers.ModelSerializer):
    '''
    权限序列化
    '''
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    class Meta:
        model = Role
        fields = '__all__'