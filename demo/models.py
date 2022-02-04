from django.db import models

# Create your models here.

# 31省份本土现有确诊
class Bentuxianyou31(models.Model):
    address = models.TextField(blank=True, null=True)
    addqz = models.BigIntegerField(blank=True, null=True)
    xyqz = models.BigIntegerField(blank=True, null=True)
    fxqy = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bentuxianyou31'


# 历史数据
class Gnlssj(models.Model):
    year = models.BigIntegerField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    confirm = models.BigIntegerField(blank=True, null=True)
    dead = models.BigIntegerField(blank=True, null=True)
    heal = models.BigIntegerField(blank=True, null=True)
    confirm_add = models.TextField(blank=True, null=True)
    confirm_cuts = models.TextField(blank=True, null=True)
    dead_cuts = models.TextField(blank=True, null=True)
    now_confirm_cuts = models.TextField(blank=True, null=True)
    heal_cuts = models.TextField(blank=True, null=True)
    newconfirm = models.BigIntegerField(db_column='newConfirm', blank=True, null=True)  
    newheal = models.BigIntegerField(db_column='newHeal', blank=True, null=True)  
    newdead = models.BigIntegerField(db_column='newDead', blank=True, null=True)  
    description = models.TextField(blank=True, null=True)
    wzz = models.BigIntegerField(blank=True, null=True)
    wzz_add = models.BigIntegerField(blank=True, null=True)
    dateid = models.TextField(db_column='dateId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gnlssj'

# 每日数据
class Mrsj(models.Model):
    confirmedcount = models.BigIntegerField(db_column='confirmedCount', blank=True, null=True)  
    confirmedincr = models.BigIntegerField(db_column='confirmedIncr', blank=True, null=True)  
    curedcount = models.BigIntegerField(db_column='curedCount', blank=True, null=True)  
    curedincr = models.BigIntegerField(db_column='curedIncr', blank=True, null=True)  
    currentconfirmedcount = models.BigIntegerField(db_column='currentConfirmedCount', blank=True, null=True)  
    currentconfirmedincr = models.BigIntegerField(db_column='currentConfirmedIncr', blank=True, null=True)  
    dateid = models.BigIntegerField(db_column='dateId', blank=True, null=True)  
    deadcount = models.BigIntegerField(db_column='deadCount', blank=True, null=True)  
    deadincr = models.BigIntegerField(db_column='deadIncr', blank=True, null=True)  
    highdangercount = models.BigIntegerField(db_column='highDangerCount', blank=True, null=True)  
    middangercount = models.BigIntegerField(db_column='midDangerCount', blank=True, null=True)  
    suspectedcount = models.BigIntegerField(db_column='suspectedCount', blank=True, null=True)  
    suspectedcountincr = models.BigIntegerField(db_column='suspectedCountIncr', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'mrsj'

# 实时热点
class Ssrd(models.Model):
    eventdescription = models.TextField(db_column='eventDescription', blank=True, null=True)  
    eventtime = models.TextField(db_column='eventTime', blank=True, null=True)  
    eventurl = models.TextField(db_column='eventUrl', blank=True, null=True)  
    homepageurl = models.TextField(db_column='homepageUrl', blank=True, null=True)  
    item_avatar = models.TextField(blank=True, null=True)
    sitename = models.TextField(db_column='siteName', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'ssrd'

# 现有疫情
class Xyyq(models.Model):
    provincename = models.TextField(db_column='provinceName', blank=True, null=True)  # Field name made lowercase.
    cityname = models.TextField(db_column='cityName', blank=True, null=True)  # Field name made lowercase.
    currentconfirmedcount = models.TextField(db_column='currentConfirmedCount', blank=True, null=True)  # Field name made lowercase.
    confirmedcount = models.TextField(db_column='confirmedCount', blank=True, null=True)  # Field name made lowercase.
    curedcount = models.TextField(db_column='curedCount', blank=True, null=True)  # Field name made lowercase.
    deadcount = models.TextField(db_column='deadCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'xyyq'

# 近两月新增
class J2Yxz(models.Model):
    dead = models.BigIntegerField(blank=True, null=True)
    heal = models.BigIntegerField(blank=True, null=True)
    importedcase = models.BigIntegerField(db_column='importedCase', blank=True, null=True)  # Field name made lowercase.
    infect = models.BigIntegerField(blank=True, null=True)
    localinfectionadd = models.BigIntegerField(blank=True, null=True)
    localconfirmadd = models.BigIntegerField(db_column='localConfirmadd', blank=True, null=True)  # Field name made lowercase.
    suspect = models.BigIntegerField(blank=True, null=True)
    deadrate = models.TextField(db_column='deadRate', blank=True, null=True)  # Field name made lowercase.
    healrate = models.TextField(db_column='healRate', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(blank=True, null=True)
    y = models.TextField(blank=True, null=True)
    confirm = models.BigIntegerField(blank=True, null=True)
    dateid = models.TextField(db_column='dateId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'j2yxz'


# 近两月累计
class J2Ylj(models.Model):
    confirm = models.BigIntegerField(blank=True, null=True)
    nowconfirm = models.BigIntegerField(db_column='nowConfirm', blank=True, null=True)  
    nowsevere = models.BigIntegerField(db_column='nowSevere', blank=True, null=True)  
    noinfecth5 = models.BigIntegerField(db_column='noInfectH5', blank=True, null=True)  
    local_acc_confirm = models.BigIntegerField(blank=True, null=True)
    dead = models.BigIntegerField(blank=True, null=True)
    healrate = models.TextField(db_column='healRate', blank=True, null=True)  
    deadrate = models.TextField(db_column='deadRate', blank=True, null=True)  
    localconfirm = models.BigIntegerField(db_column='localConfirm', blank=True, null=True)  
    suspect = models.BigIntegerField(blank=True, null=True)
    heal = models.BigIntegerField(blank=True, null=True)
    importedcase = models.BigIntegerField(db_column='importedCase', blank=True, null=True)  
    date = models.TextField(blank=True, null=True)
    y = models.TextField(blank=True, null=True)
    noinfect = models.BigIntegerField(db_column='noInfect', blank=True, null=True)  
    localconfirmh5 = models.BigIntegerField(db_column='localConfirmH5', blank=True, null=True)
    dateid = models.TextField(db_column='dateId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'j2ylj'
