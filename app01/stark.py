#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：6/20/2020  9:30 AM 
# 文件名称   ：stark.py
from app01 import models
from stark_component.service.v1 import site, StarkHandler


site.register(models.UserInfo)


class DepartmentStark(StarkHandler):
    list_display = ['id', 'title']


site.register(models.Department, DepartmentStark)
