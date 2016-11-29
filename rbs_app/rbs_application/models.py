from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserProfile(models.Model):
    user_auto_increment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='user')
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    balance = models.CharField(max_length=50, default='', blank=True)
    num_of_transactions = models.PositiveIntegerField(default='', blank=True)
    num_of_suspensions = models.CharField(max_length=50, default='', blank=True)
    status = models.TextField(default='', blank=True)
    credit_card = models.PositiveIntegerField(blank=True, default='')

    def __str__(self):
        return self.user_auto_increment_id


class Rating(models.Model):
    user_auto_increment_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
        return self.ratings

class Category(models.Model):
    category_auto_increment_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20, blank=True, default='')

    class Meta:
            ordering = ["category_auto_increment_id",]

    def __str__(self):
        return self.category_auto_increment_id

class Product(models.Model):
    seller = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    product_auto_increment_id = models.AutoField(primary_key=True)
    category_auto_increment_id = models.ForeignKey(Category)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="product_images", blank=True)
    status = models.CharField(max_length=100, blank=True)

    def post(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Order(models.Model):
    #assuming order number does not repeat...
    order_auto_increment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile)
    product_id = models.ForeignKey(Product)
    def __str__(self):
        return self.order_auto_increment_id

class Complaint(models.Model):
    complaint_id = models.PositiveIntegerField(primary_key=True)
    pub_date = models.DateTimeField('date published', auto_now_add = True)
    start_date = models.DateField()
    end_date = models.DateField()
    user_id = models.ForeignKey(UserProfile)
    def __str__(self):
        return self.complaint_id

class ShoppingCart(models.Model):
    user_auto_increment_id = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)
