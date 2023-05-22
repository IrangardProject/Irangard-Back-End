from django.db import models


EVENT_CATEGORIES = [
        ('0', 'هنری'),
        ('1', 'علمی'),
        ('2', 'فرهنگی'),
        ('3', 'ورزشی'),
        ('4', 'سیاسی'),
        ('5', 'اجتماعی'),
        ('6', 'مذهبی'),
        ('7', 'تجاری'),
        ('8', 'سایر'),
]

TOUR_TYPES = [
        ('0', 'فرهنگی'),
        ('1', 'ماجراجویی'),
        ('2', 'تفریحی'),
        ('3', 'حیات وحش'),
        ('4', 'آشپزی'),
        ('5', 'معنوی'),
        ('6', 'عکاسی'),
        ('7', 'تاریخی'),
        ('8', 'طبیعت گردی'),
        ('9', 'کویری'),
        ('10', 'قطاری'),
        ('11', 'یک روزه'),
        ('12', 'سایر'),
    ]

EVENT_TYPES = [
        ('0', 'همایش'),
        ('1', 'نمایشگاه'),
        ('2', 'نمایش'),
        ('3', 'کنسرت یا اجرا'),
        ('4', 'جشنواره'),
        ('5', 'مسابقه'),
        ('6', 'کنفرانس'),
        ('7', 'سمینار'),
        ('8', 'مجمع'),
        ('9', 'جشن'),
        ('10', 'مراسم'),
        ('11', 'سایر')
    ]

EMAIL_STATES = [
        ("0", "wait"),
        ("1", "sent"),
        ("2", "idle")
]

class StatusMode(models.TextChoices):
        ACCEPTED = 'AC'
        DENIED = 'DN'
        PENDING = 'PN'


class ActionDimondExchange():
        WRITING_EXPERIENCE = 100
        ATTENDG_IN_TOUR = 100
        ORGANIZING_TOUR = 250
        ADDING_PLACE = 50
        ADDING_EVENT = 50
        