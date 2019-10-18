from django.db import models
from django.contrib.auth.models import AbstractUser


class Permission(models.Model):
    '''
    权限表
    '''
    name = models.CharField(max_length=30, unique=True, verbose_name='权限名称')
    url = models.CharField(max_length=200,null=True,blank=True,verbose_name='url地址')
    method_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='方法类型')
    status = models.CharField(max_length=5, default='0',verbose_name='状态')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

class Component(models.Model):
    '''
    组件表
    '''
    name = models.CharField(max_length=60,unique=True,verbose_name='组件名称')
    status = models.CharField(max_length=5,default='0',verbose_name='状态')

    class Meta:
        verbose_name = '组件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

class Munu(models.Model):
    '''
    菜单
    '''
    name = models.CharField(max_length=60, unique=True, verbose_name='菜单名称')
    status = models.CharField(max_length=5, default='0', verbose_name='状态')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

class Role(models.Model):
    '''
    角色
    '''
    name = models.CharField(max_length=32,unique=True,verbose_name='角色名')
    permissions = models.ManyToManyField('Permission',blank=True,verbose_name='权限')
    components = models.ManyToManyField('Component',blank=True,verbose_name='前端组件')
    menus = models.ManyToManyField('Munu',blank=True,verbose_name='菜单')
    status = models.CharField(max_length=5, default='0', verbose_name='状态')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

class UserInfo(AbstractUser):
    """
    用户信息表
    """
    avatar = models.ImageField(upload_to="avatar", null=True, verbose_name='头像')
    introduction = models.CharField(max_length=128,blank=True,null=True,verbose_name='个人说明')
    roles = models.ManyToManyField("Role",verbose_name='角色',blank=True)
    department = models.CharField(max_length=32, blank=True, null=True, verbose_name='部门')
    tel = models.CharField(max_length=11,default='',verbose_name='手机号',blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        ordering = ['id']

    def __str__(self):
        return self.username
