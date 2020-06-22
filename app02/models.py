from django.db import models


class Host(models.Model):
    """
    主机表
    """
    name = models.CharField(verbose_name='主机名称', max_length=64)
    ip = models.GenericIPAddressField(verbose_name='主机ip地址')

    def __str__(self):
        return self.ip

