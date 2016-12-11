from .models import Rating
from decimal import Decimal


def update_rating(seller_profile):
    rs = Rating.objects.filter(user = seller_profile)
    ratings = list(rs.values_list('rating', flat = True))
    overall_rating = float(float(sum(ratings))/float(len(ratings)))
    seller_profile.rbs_rating = Decimal(overall_rating)
    seller_profile.save()