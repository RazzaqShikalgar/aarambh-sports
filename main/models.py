from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
import datetime
from datetime import timezone
# Banner


class Banner(models.Model):
    img = models.ImageField(upload_to="banner_imgs/")
    alt_text = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = '1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural = '2. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Brand


class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural = '3. Brands'

    def __str__(self):
        return self.title

# Color


class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '4. Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size


class Size(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '5. Sizes'

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=400)
    detail = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateField(
        default=datetime.datetime.now(), blank=True, null=True)

    class Meta:
        verbose_name_plural = '6. Products'

    def __str__(self):
        return self.title

# Product Attribute


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="product_imgs/", null=True)

    class Meta:
        verbose_name_plural = '7. ProductAttributes'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


# Order
status_choice = (
    ('process', 'In Process'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=status_choice, default='process', max_length=150)

    class Meta:
        verbose_name_plural = '8. Orders'

# OrderItems


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


# Product Review
RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING, max_length=150)

    class Meta:
        verbose_name_plural = 'Reviews'

    def get_review_rating(self):
        return self.review_rating



# WishList


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wishlist'

# AddressBook


class UserAddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50, null=True)
    address = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'AddressBook'


class UserContact(models.Model):
    name = models.TextField()
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


# class Order(models.Model):
#     status_choices = (
#         (1, 'Not Packed'),
#         (2, 'Ready For Shipment'),
#         (3, 'Shipped'),
#         (4, 'Delivered')
#     )
#     payment_status_choices = (
#         (1, 'SUCCESS'),
#         (2, 'FAILURE'),
#         (3, 'PENDING'),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.IntegerField(choices=status_choices, default=1)

#     total_amount = models.FloatField()
#     payment_status = models.IntegerField(
#         choices=payment_status_choices, default=3)
#     order_id = models.CharField(
#         unique=True, max_length=100, null=True, blank=True, default=None)
#     datetime_of_payment = models.DateTimeField(default=datetime.datetime.now())
#     # related to razorpay
#     razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
#     razorpay_payment_id = models.CharField(
#         max_length=500, null=True, blank=True)
#     razorpay_signature = models.CharField(
#         max_length=500, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.order_id is None and self.datetime_of_payment and self.id:
#             self.order_id = self.datetime_of_payment.strftime(
#                 'PAY2ME%Y%m%dODR') + str(self.id)
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return self.user.email + " " + str(self.id)
