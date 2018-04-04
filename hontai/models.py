from django.db import models

# Create your models here.


class Circle(models.Model):
    '''サークルのモデル。

    ここでいう「運動系」に「テニサー」は含まないので注意。
    '''
    class Meta(object):
        verbose_name = 'サークル'
        verbose_name_plural = 'サークル'

    def __str__(self):
        return self.name
    name = models.CharField(
        verbose_name='サークル名',
        max_length=30
    )

    kind_choices = (
        ('文化系', '文化系'),
        ('運動系', '運動系'),
        ('テニサー', 'テニサー')
    )

    kind = models.CharField(
        verbose_name='種別',
        max_length=4,
        choices=kind_choices
    )


class Tadameshi(models.Model):
    '''タダ飯情報のモデル。

    サークルをForeignKeyで指定する。
    '''
    class Meta(object):
        verbose_name = 'タダ飯'
        verbose_name_plural = 'タダ飯'

    def __str__(self):
        strings = self.circle.name
        return strings

    circle = models.ForeignKey(
        'hontai.Circle',
        verbose_name='サークル',
        on_delete=models.CASCADE
    )

    date = models.DateField(
        verbose_name='開催日'
    )

    time = models.TimeField(
        verbose_name='集合時刻'
    )

    place = models.CharField(
        verbose_name='集合場所',
        max_length=30
    )

    choices = (
        ('OK', 'OK'),
        ('NG', 'NG'),
        ('不明', '不明')
    )

    male = models.CharField(
        verbose_name='男性',
        choices=choices,
        default='OK',
        max_length=2
    )

    female = models.CharField(
        verbose_name='女性',
        choices=choices,
        default='OK',
        max_length=2
    )

    tobiiri = models.CharField(
        verbose_name='飛び入り参加可能',
        choices=choices,
        default='不明',
        max_length=2
    )

    note = models.TextField(
        verbose_name='イベント名/会食場所/備考',
        max_length=100,
        null=True,
        blank=True
    )

    recommend = models.BooleanField(
        verbose_name='おすすめ',
        default=False
    )
