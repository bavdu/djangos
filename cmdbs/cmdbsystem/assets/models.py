# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


# 资产情况
class Assets(models.Model):
    """
        all assets tables of SQLite
    """

    assets_type_choices = (
        ('server device', '服务器'),
        ('network device', '网络设备'),
        ('strong device', '存储设备'),
        ('security device', '安全设备'),
        ('software', '软件资产')
    )

    assets_status = (
        (0, 'online'),
        (1, 'offline'),
        (2, 'unknown'),
        (3, 'error'),
        (4, 'backup')
    )

    # 资产类型字段
    Asset_Type = models.CharField(
        verbose_name='资产类型',
        default='server device',
        max_length=64,
        choices=assets_type_choices
    )

    # 资产名称字段(不可重复)
    Asset_Name = models.CharField(
        verbose_name='资产名称',
        max_length=64,
        unique=True
    )

    # 资产序列号字段(不可重复)
    Asset_Serial_Number = models.CharField(
        verbose_name='资产序列号',
        max_length=128,
        unique=True
    )

    # 资产所属的业务线(多对一的关系);可以不属于任何业务 -->> 比如刚上线的新机器
    Asset_Of_Business = models.ForeignKey(
        to='Business',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # 资产状态
    Asset_Status = models.SmallIntegerField(
        verbose_name='资产状态',
        default=0,
        choices=assets_status
    )

    # 资产制造商
    Asset_Manufacturer = models.ForeignKey(
        to='Manufacturer',
        verbose_name='资产制造商',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # 资产的标签
    Asset_Tags = models.ManyToManyField(
        to='Tags',
        verbose_name='资产标签',
        blank=True
    )

    # 资产的管理员
    Asset_Managers = models.ForeignKey(
        to=User,
        verbose_name='资产管理者',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='admin'
    )

    # 资产的管理IP地址
    Manage_IP = models.GenericIPAddressField(
        verbose_name='管理IP地址',
        null=True, blank=True
    )

    # 资产所在机房
    Asset_IDC = models.ForeignKey(
        to='IDC',
        verbose_name='所属机房',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # 资产购买日期
    Asset_Purchase = models.DateField(
        verbose_name='购买日期',
        null=True, blank=True
    )

    # 资产过保日期
    Asset_Expire = models.DateField(
        verbose_name='过保日期',
        null=True, blank=True
    )

    # 资产价格
    Asset_Price = models.FloatField(
        verbose_name='资产价格',
        null=True, blank=True
    )

    # 资产审批人员
    Asset_Approved = models.ForeignKey(
        to=User,
        verbose_name='资产审计者',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved'
    )

    # 资产审批日期
    Asset_Ratify = models.DateTimeField(
        verbose_name='批准日期',
        auto_now_add=True
    )

    # 资产更新日期
    Asset_Update = models.DateTimeField(
        verbose_name='更新日期',
        auto_now=True
    )

    # 备注信息
    Remark_Info = models.TextField(
        verbose_name='备注',
        null=True, blank=True
    )

    def __str__(self):
        return '{}:{}'.format(self.Asset_Name, self.Asset_Serial_Number)
    
    class Meta:
        verbose_name = '资产总表',
        ordering = ['-Asset_Ratify']


# 服务器信息
class Servers(models.Model):
    """
        servers information
    """

    server_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机')
    )

    create_type_choice = (
        ('auto', '自动添加'),
        ('manual', '手动添加')
    )

    # 设置资产列表一对一
    Asset = models.OneToOneField(Assets, on_delete=models.CASCADE)

    # 服务器类型
    server_type = models.SmallIntegerField(
        verbose_name='服务器类型',
        choices=server_type_choice,
        default=0
    )

    # 创建方式
    create_type = models.CharField(
        verbose_name='创建类型',
        choices=create_type_choice,
        default='auto',
        max_length=32
    )

    # 服务器型号
    model_serial = models.CharField(
        verbose_name='服务器型号',
        max_length=128,
        null=True, blank=True
    )

    # 服务器RAID类型
    raid_type = models.CharField(
        verbose_name='RAID类型',
        max_length=512,
        null=True, blank=True
    )

    # 操作系统类型
    os_type = models.CharField(
        verbose_name='操作系统类型',
        max_length=64,
        null=True, blank=True
    )

    # 操作系统发行商
    os_publisher = models.CharField(
        verbose_name='系统发行商',
        max_length=64,
        null=True, blank=True
    )

    # 操作系统版本
    os_release = models.CharField(
        verbose_name='系统版本',
        max_length=64,
        null=True, blank=True
    )

    def __str__(self):
        return '{0}-{1}-{2} <Serial:{3}>'.format(
            self.Asset.Asset_Name, self.server_type,
            self.model_serial, self.Asset.Asset_Serial_Number
        )

    class Meta:
        verbose_name = '服务器'


# 网络设备
class NetworkDevice(models.Model):
    """
        network device
    """

    network_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备')
    )

    Asset = models.OneToOneField(Assets, on_delete=models.CASCADE)

    # 网络设备类型
    network_type = models.SmallIntegerField(
        verbose_name='网络设备类型',
        choices=network_type_choice,
        default=0
    )

    # VLAN的IP地址
    vlan_ip = models.GenericIPAddressField(
        verbose_name='LAN区的IP地址',
        null=True, blank=True
    )

    # 内网IP地址
    intranet_ip = models.GenericIPAddressField(
        verbose_name='内网IP地址',
        null=True, blank=True
    )

    # 设备型号
    model_number = models.CharField(
        verbose_name='设备型号',
        default='unknown',
        max_length=128
    )

    # 设备固件号
    firmware_number = models.CharField(
        verbose_name='设备固件号',
        max_length=128,
        null=True, blank=True
    )

    # 端口数量
    port_number = models.SmallIntegerField(
        verbose_name='端口数量',
        null=True, blank=True
    )

    # 设备详细配置
    device_detail = models.TextField(
        verbose_name='配置信息',
        null=True, blank=True
    )

    def __str__(self):
        return '{0}-{1}-{2} <Serial:{3}>'.format(
            self.Asset.Asset_Name, self.network_type,
            self.firmware_number, self.Asset.Asset_Serial_Number
        )

    class Meta:
        verbose_name = '网络设备'


# 存储设备
class StrongDevice(models.Model):
    """
        strong device
    """

    strong_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机')
    )

    Asset = models.OneToOneField(Assets, on_delete=models.CASCADE)

    # 设备类型
    strong_type = models.SmallIntegerField(
        verbose_name='设备类型',
        choices=strong_type_choice,
        default=0
    )

    # 设备型号
    model_number = models.CharField(
        verbose_name='设备型号',
        max_length=128,
        default='unknown'
    )

    def __str__(self):
        return '<{0}:{1}>'.format(self.Asset.Asset_Name, self.model_number)

    class Meta:
        verbose_name = '存储设备'


# 安全设备
class SecurityDevice(models.Model):
    """
        security device
    """

    security_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    Asset = models.OneToOneField('Assets', on_delete=models.CASCADE)

    # 安全设备类型
    security_type = models.SmallIntegerField(
        verbose_name='安全设备类型',
        choices=security_type_choice,
        default=0
    )

    # 设备型号
    model_number = models.CharField(
        verbose_name='设备型号',
        max_length=128,
        default='unknown'
    )

    def __str__(self):
        return '<{0}:{1}>'.format(self.Asset.Asset_Name, self.model_number)

    class Meta:
        verbose_name = '安全设备'


# 软件信息
class Software(models.Model):
    """
        software info
    """

    software_type_choice = (
        (0, '操作系统'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )

    # 软件类型
    software_type = models.SmallIntegerField(
        verbose_name='软件类型',
        choices=software_type_choice,
        default=0
    )

    # 授权数量
    licence_number = models.SmallIntegerField(
        verbose_name='授权数量',
        default=1
    )

    # 版本信息
    version_info = models.CharField(
        verbose_name='版本信息',
        max_length=64, unique=True,
        help_text='example: RedHat Enterprise 7.4 release'
    )

    def __str__(self):
        return '<{0}:{1}>'.format(self.software_type, self.version_info)

    class Meta:
        verbose_name = '软件信息'


# 其他
class Business(models.Model):
    """
        business info
    """

    business_name = models.CharField(
        verbose_name='业务线名',
        unique=True,
        max_length=64
    )

    remark = models.CharField(
        verbose_name='备注',
        max_length=64,
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.business_name)

    class Meta:
        verbose_name = '业务线'


class Manufacturer(models.Model):
    """
        Manufacturer info
    """

    manufacturer_name = models.CharField(
        verbose_name='服务器厂商',
        max_length=64,
        unique=True
    )

    manufacturer_phone = models.CharField(
        verbose_name='支持电话',
        max_length=30,
        null=True, blank=True
    )

    remark = models.TextField(
        verbose_name='备注',
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.manufacturer_name)

    class Meta:
        verbose_name = '服务器厂商信息'


class Tags(models.Model):
    """
        tags info
    """

    tags_name = models.CharField(
        verbose_name='标签',
        unique=True,
        max_length=30
    )

    create_Date = models.DateField(
        verbose_name='创建日期',
        auto_now_add=True
    )

    def __str__(self):
        return '{}'.format(self.tags_name)

    class Meta:
        verbose_name = '标签'


class IDC(models.Model):
    """
        IDC info
    """

    idc_name = models.CharField(
        verbose_name='IDC机房名称',
        max_length=64,
        unique=True
    )

    remark = models.CharField(
        verbose_name='备注',
        max_length=128,
        null=True, blank=True
    )

    def __str__(self):
        return "{}".format(self.idc_name)

    class Meta:
        verbose_name = 'IDC机房'


# CPU, Memory, Disk, Network of get info.
class Cpu(models.Model):
    """
        cpu info
    """

    Asset = models.OneToOneField('Assets', on_delete=models.CASCADE)

    # cpu型号
    cpu_model = models.CharField(
        verbose_name='cpu型号',
        max_length=128,
        null=True, blank=True
    )

    # cpu数量
    cpu_count = models.PositiveSmallIntegerField(
        verbose_name='cpu数量',
        default=1
    )

    # cpu核心数
    cpu_core_count = models.PositiveSmallIntegerField(
        verbose_name='cpu核心数',
        default=1
    )

    def __str__(self):
        return '<{0}:{1}>'.format(self.Asset.Asset_Name, self.cpu_model)

    class Meta:
        verbose_name = 'cpu信息'


class Memory(models.Model):
    """
        memory info
    """

    Asset = models.ForeignKey('Assets', on_delete=models.CASCADE)

    # 设备号
    serial_number = models.CharField(
        verbose_name='内存设备号',
        max_length=128,
        null=True, blank=True
    )

    # 型号
    model_number = models.CharField(
        verbose_name='内存型号',
        max_length=128,
        blank=True, null=True
    )

    # 内存制造商
    manufacturer = models.CharField(
        verbose_name='内存制造商',
        max_length=128,
        blank=True, null=True
    )

    # 内存插槽
    slot = models.CharField(
        verbose_name='插槽',
        max_length=64
    )

    # 内存大小
    size = models.IntegerField(
        verbose_name='单位GB',
        blank=True, null=True
    )

    def __str__(self):
        return '{}-{}-{}-{}'.format(
            self.Asset.Asset_Name, self.model_number,
            self.slot, self.size
        )

    class Meta:
        verbose_name = '内存信息'
        unique_together = ('Asset', 'slot')


class Disk(models.Model):
    """
        disk info
    """

    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    Asset = models.ForeignKey('Assets', on_delete=models.CASCADE)

    # 磁盘序列号
    serial_number = models.CharField(
        verbose_name='磁盘序列号',
        max_length=128
    )

    # 磁盘槽位
    slot = models.CharField(
        verbose_name='磁盘插槽',
        max_length=64,
        null=True, blank=True
    )

    # 磁盘型号
    model_number = models.CharField(
        verbose_name='磁盘型号',
        max_length=128,
        null=True, blank=True
    )

    # 磁盘制造商
    manufacturer = models.CharField(
        verbose_name='磁盘制造商',
        max_length=128,
        null=True, blank=True
    )

    # 磁盘大小
    size = models.CharField(
        verbose_name='磁盘大小',
        blank=True, null=True
    )

    # 接口类型
    interface_type = models.CharField(
        verbose_name='磁盘接口类型',
        max_length=16,
        choices=disk_interface_type_choice,
        default='unknown'
    )

    def __str__(self):
        return '<{}:{}:{}>'.format(self.Asset.Asset_Name, self.model_number, self.slot)

    class Meta:
        verbose_name = '磁盘信息'
        unique_together = ('Asset', 'serial_number')


class Nic(models.Model):
    """
        network info
    """

    Asset = models.ForeignKey('Asset', on_delete=models.CASCADE)

    # 网卡名称
    nic_name = models.CharField(
        verbose_name='网卡名称',
        max_length=64,
        null=True, blank=True
    )

    # 网卡型号
    nic_model_number = models.CharField(
        verbose_name='网卡型号',
        max_length=128
    )

    # 网卡MAC地址
    nic_mac = models.CharField(
        verbose_name='网卡MAC地址',
        max_length=64
    )

    # 网卡IP地址
    nic_ip = models.GenericIPAddressField(
        verbose_name='网卡IP地址',
        blank=True, null=True
    )

    # 网卡掩码
    nic_prefix = models.CharField(
        verbose_name='网卡掩码',
        max_length=64,
        blank=True, null=True
    )

    # 网卡绑定地址
    bond_ip = models.CharField(
        verbose_name='绑定地址',
        max_length=64,
        null=True, blank=True
    )

    def __str__(self):
        return '<{}:{}:{}>'.format(self.Asset.Asset_Name, self.nic_model_number, self.nic_mac)

    class Meta:
        verbose_name = '网卡'
        unique_together = ('Asset', 'nic_model_number', 'nic_mac')


class Eventlog(models.Model):
    """
        eventlog write
    """

    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )

    event_name = models.CharField(
        verbose_name='事件名字',
        max_length=128
    )

    Asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)
    new_asset = models.ForeignKey('NewAssets', blank=True, null=True, on_delete=models.SET_NULL)

    event_type = models.SmallIntegerField(
        verbose_name='事件类型',
        choices=event_type_choice,
        default=4
    )

    component = models.CharField(
        verbose_name='事件子项',
        max_length=256,
        null=True, blank=True
    )

    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人',
                             on_delete=models.SET_NULL)
    remark = models.TextField('备注', blank=True, null=True)


class NewAssets(models.Model):
    """
        New asset
    """

    asset_type_choice = (
        ('server', '服务器'),
        ('network device', '网络设备'),
        ('storage device', '存储设备'),
        ('security device', '安全设备'),
        ('software', '软件资产'),
    )

    serial_number = models.CharField('资产序列号', max_length=128, unique=True)
    asset_type = models.CharField(
        verbose_name='资产类型',
        choices=asset_type_choice,
        default='server',
        max_length=64,
        blank=True, null=True
    )

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model_number = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField('CPU物理数量', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核心数量', blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_type = models.CharField('系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本号', max_length=64, blank=True, null=True)
    data = models.TextField('资产数据')
    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = '新上线待批准资产'
        ordering = ['-c_time']

