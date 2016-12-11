from .models import *
from datetime import date,time


def update_all():
    '''
    Calls all active products in our db and runs through every single active one to check if their date is past due
    if it is - set the item to inactive
    ('############', datetime.date(2016, 12, 18), '^^^^^^', datetime.time(10, 28, 24, 73668))

    :return:
    '''
    active_items = Product.objects.filter(is_active = True)
    for item in active_items:
        takedown_daymonth = item.takedown_date
        takedown_time = item.takedown_time
        if takedown_daymonth < date.today():
            item.is_active = False
        elif takedown_daymonth == date.today():

            if takedown_time.hour <= datetime.now().time().hour and takedown_time.minute <= datetime.now().time().minute:
                item.is_active = False
                item.save()

