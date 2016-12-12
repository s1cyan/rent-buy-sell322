from .models import *
from datetime import date,time
from check_vip import check_vip


def update_all():
    '''
    Calls all active products in our db and runs through every single active one to check if their date is past due
    if it is - sets the item to inactive
    :return:
    '''
    active_items = Product.objects.filter(is_active = True)
    for item in active_items:
        takedown_daymonth = item.takedown_date
        takedown_time = item.takedown_time
        if takedown_daymonth < date.today():
            if item.option == 'A':
                seller = UserProfile.objects.get(user = item.seller)
                seller.balance += item.price
                seller.transaction += 1
                seller.save()
            item.is_active = False
            item.save()
        elif takedown_daymonth == date.today():
            if takedown_time.hour <= datetime.now().time().hour and takedown_time.minute <= datetime.now().time().minute:
                if item.option == 'A':
                    seller = UserProfile.objects.get(user=item.seller)
                    seller.balance += item.price
                    seller.transaction += 1
                    seller.save()
                    check_vip(seller)
                item.is_active = False
                item.save()
