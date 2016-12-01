from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    bio = models.TextField(default='', blank=True)
    phone = models.PositiveIntegerField(_("Phone number"), blank=True, default='')
    city = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default='0.00')
    transactions = models.PositiveIntegerField(_("Number of transactions"), default='0', blank=True)
    suspensions = models.PositiveIntegerField(_("Number of suspensions"), default='0')
    strikes = models.PositiveIntegerField(_("Number of strikes"), default=0)
    credit_card = models.CharField(blank=True, default='1234999912348888')

    def __str__(self):
        return str(self.user)


class Rating(models.Model):
    id = models.ForeignKey(UserProfile, primary_key=True, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return self.ratings

class Category(models.Model):
    name = models.CharField(max_length=20, required=True, default="Miscellaneous")

    class Meta:
        ordering = ["category_auto_increment_id",]
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    seller = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=100, blank=True)

    def post(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Order(models.Model):
    #assuming order number does not repeat...
    user = models.ForeignKey(UserProfile)
    products = models.ManyToManyField(Product)
    def __str__(self):
        return str(self.id)

class Complaint(models.Model):
    complaint_id = models.PositiveIntegerField(primary_key=True)
    pub_date = models.DateTimeField("Date published", auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user_id = models.ForeignKey(UserProfile)
    def __str__(self):
        return str(self.complaint_id)

class ShoppingCart(models.Model):
    user_auto_increment_id = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(_("Created on"))
    checked_out = models.BooleanField(_("Transaction Complete"), default=False)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ['-creation_date',]

    # def __unicode__(self):
    #     return unicode(self.creation_date)