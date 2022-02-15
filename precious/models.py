from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Asset(models.Model):
    """
    所有资产的共有数据表
    """

    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('memorydevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_status = (
        (0, 'online'),
        (1, 'outline'),
        (2, 'unknown'),
        (3, 'fault'),
        (4, 'backup'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
                                      on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商',
                                     on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin',
                              on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同', on_delete=models.SET_NULL)
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    price = models.FloatField(null=True, blank=True, verbose_name='价格')
    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by',
                                    on_delete=models.SET_NULL)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    def __str__(self):
        return '<%s> %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-c_time']


class Server(models.Model):
    """ 服务器设备 """

    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片服务器'),
        (2, '小型服务器'),
    )

    created_by_choice = (
        ('auto', '自动录入'),
        ('manual', '人工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_choice, default='auto', max_length=32, verbose_name='录入方式')
    host_on = models.ForeignKey('self', related_name='host_on_server', blank=True, null=True,
                                verbose_name='宿主机', on_delete=models.CASCADE)
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, null=True, blank=True, verbose_name='Raid类型')
    os_type = models.CharField(verbose_name='操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行商')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统版本')

    def __str__(self):
        return '%s--%s--%s <sn: %s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'


class SecurityDevice(models.Model):
    """ 安全设备 """

    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '漏洞扫描设备'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')
    model = models.CharField(max_length=128, default='unknown', verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + "id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = '安全设备'


class MemoryDevice(models.Model):
    """ 存储设备 """

    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (3, '磁带机'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')
    model = models.CharField(max_length=128, default='unknown', verbose_name='存储设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + "id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'


class NetworkDevice(models.Model):
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')
    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='内联网IP')
    model = models.CharField(max_length=128, default='unknown', verbose_name='网络设备型号')
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name='设备固件版本')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name='端口个数')
    device_detail = models.TextField(null=True, blank=True, verbose_name='详细设备')

    def __str__(self):
        return "%s--%s--%s <sn:%s>" % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'


class Software(models.Model):
    """ 只保存付费购买的软件 """
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='软件类型')
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(max_length=64, unique=True, help_text='example: RedHat release 7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return "%s--%s" % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = '软件/系统'


class IDC(models.Model):
    """ 机房 """

    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')
    memo = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'


class Manufacturer(models.Model):
    """ 厂商 """

    name = models.CharField(max_length=64, unique=True, verbose_name='厂商名称')
    telephone = models.CharField(max_length=30, blank=True, null=True, verbose_name='支持电话')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'


class BusinessUnit(models.Model):
    """ 业务线 """

    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level',
                                    on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线')
    memo = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = '业务线'


class Contract(models.Model):
    """ 合同 """

    sn = models.CharField(max_length=128, unique=True, verbose_name='合同号')
    name = models.CharField(max_length=64, verbose_name='合同名称')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    price = models.IntegerField(verbose_name='合同金额')
    detail = models.TextField(blank=True, null=True, verbose_name='合同详情')
    start_day = models.DateField(blank=True, null=True, verbose_name='生效日期')
    end_day = models.DateField(blank=True, null=True, verbose_name='失效日期')
    license_num = models.IntegerField(blank=True, null=True, verbose_name='Lincese数量')
    c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')
    m_day = models.DateField(auto_now_add=True, verbose_name='修改日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'


class Tag(models.Model):
    """ 标签 """

    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class CPU(models.Model):
    """ CPU组件 """

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')
    cpu_core_count = models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')

    def __str__(self):
        return self.asset.name + ": " + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'


class RAM(models.Model):
    """ 内存组件 """

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='内存型号')
    manufacturer = models.CharField(max_length=128, blank=True, null=True, verbose_name='内存制造商')
    slot = models.CharField(max_length=64, verbose_name='插槽')
    capacity = models.IntegerField(blank=True, null=True, verbose_name='内存大小(GB)')

    def __str__(self):
        return "%s: %s: %s: %sGB" % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = '内存'
        unique_together = ('asset', 'slot')


class Disk(models.Model):
    """ 硬盘设备 """

    disk_interface_type_choice = (
        (0, 'SATA'),
        (1, 'SAS'),
        (2, 'SCSI'),
        (3, 'SSD'),
        (4, 'unknown'),
    )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(max_length=128, verbose_name='硬盘SN号')
    slot = models.CharField(max_length=64, blank=True, null=True, verbose_name='所在插槽位')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='硬盘型号')
    manufacturer = models.CharField(max_length=128, blank=True, null=True, verbose_name='硬盘制造商')
    capacity = models.FloatField(blank=True, null=True, verbose_name='磁盘容量(GB)')
    disk_interface_type = models.CharField(max_length=16, choices=disk_interface_type_choice, default=4,
                                           verbose_name='接口类型')

    def __str__(self):
        return '%s: %s: %s: %sGB'

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'
        unique_together = ('asset', 'sn')


class NIC(models.Model):
    """ 网卡组件 """

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='网卡名称')
    model = models.CharField(max_length=256, verbose_name='网卡型号')
    mac = models.CharField(max_length=64, verbose_name='MAC地址')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    net_mask = models.CharField(max_length=64, blank=True, null=True, verbose_name='子网掩码')
    bonding = models.CharField(max_length=64, blank=True, null=True, verbose_name='绑定地址')

    def __str__(self):
        return '%s: %s: %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = '网卡'
        unique_together = ('asset', 'model', 'mac')


class EventLog(models.Model):
    """
    日志
    在关联对象被删除的时候，不能一并删除，需要保留日志
    故on_delete=model.SET_NULL
    """

    name = models.CharField(max_length=128, verbose_name='事件名称')
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线/更新/变更')
    )

    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField(choices=event_type_choice, default=4, verbose_name='事件类型')
    component = models.CharField(max_length=256, blank=True, null=True, verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True, verbose_name='事件时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人',
                             on_delete=models.SET_NULL)
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = '事件记录'


class NewAssetApprovalZone(models.Model):
    """ 新资产待审批区 """

    sn = models.CharField(max_length=128, unique=True, verbose_name='资产SN号')
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('memorydevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    manufacturer = models.CharField(max_length=64, null=True, blank=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.CharField(max_length=64, blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')
    cpu_core_count = models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')
    os_type = models.CharField(verbose_name='操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行商')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统版本')
    data = models.TextField(verbose_name='资产数据')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')
    approved = models.BooleanField(default=False, verbose_name='批准意见')

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = '新上线待批准资产'
        ordering = ['-c_time']
