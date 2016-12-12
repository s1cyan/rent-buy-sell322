from .models import UserProfile

def check_vip(profile):
    if profile.balance >= 5000.00 and profile.transactions >= 5 and profile.suspensions == 0 and profile.strikes == 0:
        profile.rbs_vip_user = True
        print(profile.rbs_vip_user)
        profile.save()
    else:
        profile.rbs_vip_user = False
        print("i made it --- false")
        print(profile.rbs_vip_user)
        profile.save()
