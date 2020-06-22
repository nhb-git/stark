#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：6/20/2020  9:29 AM 
# 文件名称   ：v1.py
from django.conf.urls import url
from django.shortcuts import HttpResponse, render


class StarkHandler:
    list_display = []

    def __init__(self, model_class, prev=None):
        self.model_class = model_class
        self.prev = prev

    def changelist_view(self, request):
        """
        查看列表页面
        :param request:
        :return:
        """
        # 生成表格的头部
        header_list = []
        if self.list_display:
            for field in self.list_display:
                verbose_name = self.model_class._meta.get_field(field).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)
        # 生成表格的数据
        data_list = self.model_class.objects.all()
        data_obj_list = []
        for data_obj in data_list:
            temp = []
            if self.list_display:
                for data_obj_attr in self.list_display:
                    temp.append(getattr(data_obj, data_obj_attr))
            else:
                temp.append(data_obj)
            data_obj_list.append(temp)
        return render(request, 'stark_component/changelist.html', {
                'data_list': data_list, 'header_list': header_list,
                'data_obj_list': data_obj_list})

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        return HttpResponse('添加页面')

    def change_view(self, request, pk):
        """
        修改页面
        :param request:
        :return:
        """
        return HttpResponse('修改页面')

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        return HttpResponse('删除页面')

    def get_url_name_str(self, action):
        """
        生成url的name
        :param action:
        :return:
        """
        app_name, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_name, model_name, self.prev, action)
        return '%s_%s_%s' % (app_name, model_name, action)

    @property
    def list_url_name(self):
        """
        列表url的别名
        :return:
        """
        self.get_url_name_str('list')

    @property
    def add_url_name(self):
        """
        添加url的别名
        :return:
        """
        self.get_url_name_str('add')

    @property
    def del_url_name(self):
        """
        删除url的别名
        :return:
        """
        self.get_url_name_str('del')

    @property
    def change_url_name(self):
        """
        编辑url的别名
        :return:
        """
        self.get_url_name_str('change')

    def get_urls(self):
        app_name = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        patterns = [
            url(r'list/$', self.changelist_view, name=self.list_url_name),
            url(r'add/$', self.add_view, name=self.add_url_name),
            url(r'change/(\d+)/$', self.change_view, name=self.change_url_name),
            url(r'delete/(\d+)/$', self.delete_view, name=self.del_url_name),
        ]
        patterns.extend(self.extra_url())
        return patterns

    def extra_url(self):
        return []


class StarkSite:
    """
    数据库操作组件类定义
    """
    def __init__(self):
        self._register = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler=None, prev=None):
        """
        注册model
        :param model_class: 数据库模型类
        :param handler: 处理数据库增删改查视图的类
        :return:
        """
        if not handler:
            handler = StarkHandler
        self._register.append({'model_class': model_class, 'handler': handler(model_class, prev), 'prev': prev})

    def get_urls(self):
        patterns = []
        for app in self._register:
            app_name = app['model_class']._meta.app_label
            model_name = app['model_class']._meta.model_name
            prev = app['prev']
            if prev:
                patterns.append(url(r'%s/%s/%s/' % (prev, app_name, model_name), (app['handler'].get_urls(), None, None)))
            else:
                patterns.append(url(r'%s/%s/' % (app_name, model_name), (app['handler'].get_urls(), None, None)))
        return patterns

    @property
    def urls(self):
        """
        返回所有model增删改查的url对象
        :return:
        """
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
