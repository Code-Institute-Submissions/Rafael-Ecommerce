from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField
import os
# Create your models here.
CATEGORY_CHOICES = (
    ("Women", "Women"),
    ("Men", "Men"),
    ("Kids", "Kids"),
    ("Accessories", "Accessories"),
    ("Cosmetics", "Cosmetics"),
)

ADMIN_CHOICES = (
    ("admin","admin"),
)

SIZE_CHOICES = (
    ("S","S"),
    ("M","M"),
    ("L","L"),
    ("XL","XL"),
)
# declaring a Category Model
class ProductInfo(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='1'
    )
    product_title = models.CharField(max_length=100)
    uploaded_by = models.CharField(
        max_length=20,
        choices=ADMIN_CHOICES,
        default='admin'
    )
    uploaded_at = models.DateField(default=timezone.now)
    size = MultiSelectField(
        choices=SIZE_CHOICES,
        default= 'S'
    )
    price = models.FloatField(default=0)
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("product_details", kwargs={
            "pk": self.pk
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })

    def __str__(self):
        return self.product_title + ", Category : "+self.category

class DataUpload(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    image = models.ImageField()

    def save(self):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = self.product_info.category+'/'+self.product_info.product_title
        super(DataUpload, self).save()

    def __str__(self):
        return str(self.product_info.product_title)+" - "+str(self.id)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product_info.product_title}"

    def get_total_item_price(self):
        return self.quantity * self.product_info.price

    def get_total_price(self):
        discount_amount = (self.product_info.discount_price * self.product_info.price) / 100
        total = (self.product_info.price - discount_amount) * self.quantity
        return int(total)

    def get_discount_item_price(self):
        return self.quantity * self.product_info.discount_price

    def get_amount_saved(self):
        return (self.product_info.discount_price * self.product_info.price) / 100

    def get_final_price(self):
        if self.product_info.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


