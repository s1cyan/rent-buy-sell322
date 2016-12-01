''' Use this script to populate the datebase for rbs
    Type in: python populate_rbs.py and check the data in the admin site. '''
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      # 'rbs_app.settings')
# import django
# django.setup()


from django.core.management.base import BaseCommand
from rbs_application.models import Product, Category


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def clear_cat(self):
        cats = Category.objects.all()
        cats.delete()


    def clear_products(self):
        products = Product.objects.all()
        products.delete()


    def add_product(self, cat, title, price):
        p = Product.objects.get_or_create(category_id=cat, title=title, price=price)
        p.save()
        return p


    def add_cat(self, name):
        c = Category.objects.get_or_create(category_name=name)[0]
        c.save()
        return c


    def _populate(self):
        # First, we will create lists of dictionaries containing the Products
        # we want to add into each category.
        # Then we will create a dictionary of dictionaries for our categories.
        # This might seem a little bit confusing, but it allows us to iterate
        # through each data structure, and add the data to our models.

        clothing = [
            {"title": "Pink Chanel Suit",
             "price": 1000},
            {"title": "Bjork's Swan Dress",
             "price": 80},
            {"title": "Black Givenchy Dress",
             "price": 500}
        ]

        games = [
            {"title": "Cities: Skylines",
             "price": 7.99},
            {"title": "Counter-Strike: Global Offensive",
             "price": 10.04},
            {"title": "The Last of Us Remastered",
             "price": 14.99}
        ]

        books = [
            {"title": "Tango with Django",
             "price": 9.99},
            {"title": "The Annals of America",
             "price": 166.16},
            {"title": "Holy Bible, King James Version",
             "price": 1.00},
            {"title": "The Hitchhiker's Guide to the Galaxy",
             "price": 7.19},

        ]

        # Dictionary of categories
        cats = {"Clothing": {"products": clothing},
                "Games": {"products": games},
                "Books": {"products": books}}
        # If you want to add more categories or products, add them to the dictionaries above.



        # The code below goes through the cats dictionary, then adds each product,
        # and then adds all the associated products for that category.
        for cat, cat_data in cats.items():
            c = self.add_cat(cat)
            for p in cat_data["products"]:
                self.add_product(c, p["title"], p["price"])

        # for cat, cat_data in cats.items():
        #     c = self.add_cat(cat)
        #     for p in cat_data["type"]:
        #         print(p["title"])
        #     #     self.add_product(c, p["title"], p)

        # Print out the categories we have added.
        # for c in Category.objects.all():
        #     for p in Product.objects.filter(category_name=c):
        #         print("- {0} - {1}".format(str(c), str(p)))



    def handle(self, *args, **options):
        print("Starting RBS database population...")
        print("deleting categories...")
        self.clear_cat()
        print("filling in categories...")
        self._populate()

# Start execution here!
# if __name__ == '__main__':
#     print("Starting RBS population script...")
#     populate()
