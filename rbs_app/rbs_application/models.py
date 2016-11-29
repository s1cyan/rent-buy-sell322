from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileField

class UserProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='user')
    photo = FileField(verbose_name=_("Profile Picture"),
                      upload_to=upload_to("main.UserProfile.photo", "profiles"),
                      format="Image", max_length=255, null=True, blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    balance = models.CharField(max_length=50, default='', blank=True)
    num_of_transactions = models.CharField(max_length=50, default='', blank=True)
    num_of_suspensions = models.CharField(max_length=50, default='', blank=True)
    status = models.TextField(default='', blank=True)
    credit_card = models.IntegerField(max_length=19, blank=True, default='')
    products = models.ForeignKey(Product)
    def __str__(self):
        return self.user_id

class Ratings(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
        return self.ratings

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=30)

    class Meta:
            ordering = ["category_id", "category_name"]

    def __str__(self):
        return self.category_id

class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    category_id = models.ForeignKey(Category)
    category_name = models.CharField(Category)
    title = models.CharField(max_length=128)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="product_images", blank=True)
    status = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["category_id", "category_name", "title", "description", "image", "price", "quantity", "status"]

    def __str__(self):
            return self.product_id

class Orders(models.Model):
    #assuming order number does not repeat...
    order_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(UserProfile)
    product_id = models.ForeignKey(Products)
    def __str__(self):
        return self.order_id

class Complaints(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    pub_date = models.DateTimeField('date published', auto_now_add = True)
    start_date = models.DateField()
    end_date = models.DateField()
    user_id = models.ForeignKey(UserProfile)
    def __str__(self):
        return self.complaint_id

class ShoppingCart(models.Model):
    user_id = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)
