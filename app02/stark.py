#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：6/20/2020  9:31 AM 
# 文件名称   ：stark.py
from stark_component.service.v1 import site, StarkHandler
from app02 import models


site.register(models.Host)
