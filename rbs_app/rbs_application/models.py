from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    bio = models.TextField(default='', blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_("Phone number"),
                             validators=[phone_regex],
                             blank=True,
                             default='2126507000',
                             max_length=10)
    address = models.CharField("Street Address", max_length=40)
    address2 = models.CharField("Apt / Floor", max_length=40, null=True)
    city = models.CharField("City", max_length=25, default='New York')
    state = models.CharField("State", max_length=20, default='NY')
    zipcode = models.CharField("ZIP code", max_length=5, default="10031")
    country = models.CharField(max_length=50, default='USA', blank=True)
    # city = models.CharField(max_length=50, default='New York', blank=True)
    balance = models.DecimalField(max_digits=7,
                                  decimal_places=2,
                                  default='0.00', )
    transactions = models.PositiveIntegerField(_("Number of transactions"), default='0', blank=True)
    suspensions = models.PositiveIntegerField(_("Number of suspensions"), default='0')
    strikes = models.PositiveIntegerField(_("Number of strikes"), default=0)
    credit_card = models.CharField(max_length=16, blank=True, default='1234999912348888')
    verified_by_admin = models.BooleanField(_("RBS Verified User"), default=False, editable=True)
    rbs_rating = models.DecimalField(max_digits= 3, decimal_places=2,default='5.00', blank= True)
    rbs_vip_user = models.BooleanField(_("RBS VIP User"), default=False, editable=True)

    class Meta:
        verbose_name = "User Profile"

    def __str__(self):
        return str(self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Rating(models.Model):
    user = models.ForeignKey(UserProfile)
    rating = models.IntegerField( blank = True)
    # ratings = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return str(self.rating)


class Category(models.Model):
    name = models.CharField(max_length=20, default="Miscellaneous")

    class Meta:
        ordering = ["name", ]
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    (BUY, RENT, AUCTION) = ('B', 'R', 'A')
    SELL_CHOICES = (
        (BUY, 'Buy It Now'),
        (RENT, 'Rent'),
        (AUCTION, 'Auction'),
    )
    seller = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=200)
    # option: How the product is to be sold
    option = models.CharField(
        max_length=1,
        choices=SELL_CHOICES,
        default=BUY,
    )
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    takedown_date = models.DateField(blank=False, null=False, default=datetime.today().date() + timedelta(days=7))
    takedown_time = models.TimeField(blank=False, null=False, default=datetime.now().time())
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(max_length=100, blank=True, default=True)
    # below is only for auction items
    current_bidder = models.PositiveIntegerField(blank = True, null = True ,default= None)

    def post(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Complaint(models.Model):
    # complaint_id = models.PositiveIntegerField(primary_key=True)
    # pub_date = models.DateTimeField("Date published", auto_now_add=True)
    # start_date = models.DateField()
    # end_date = models.DateField()
    user_id = models.ForeignKey(UserProfile)
    complaint = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="No details",
    )

    def __str__(self):
        return str(self.complaint)


class ShoppingCart(models.Model):
    user = models.OneToOneField(UserProfile)
    products = models.ManyToManyField(Product)
    # is_current = models.BooleanField(default=True)
    # creation_date = models.DateTimeField(_("Created on"))
    # checked_out = models.BooleanField(_("Transaction Complete"), default=False)

    def __str__(self):
        return "%s's Shopping Cart" % self.user

    class Meta:
        # pass
        verbose_name = _('Shopping Cart')
        verbose_name_plural = _('Shopping Carts')
        # ordering = ['-creation_date', ]


class Order(models.Model):
    user = models.ForeignKey(UserProfile)
    products = models.ManyToManyField(Product)
    # creation_date = models.DateTimeField(_("Ordered on"))

    def __str__(self):
        return "{0}'s Order# {1} ".format(self.user, self.id)


class Comment(models.Model):
    product = models.ForeignKey(Product)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
