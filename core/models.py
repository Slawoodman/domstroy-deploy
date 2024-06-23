from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone
from userauths.models import Manager
from ckeditor_uploader.fields import  RichTextUploadingField


STATUS_CHOICE = {
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
}

STATUS = {
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected','Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published')
}

PRODUCT_CHARACTER = {
    ('NEW', 'new'),
    ('USED', 'used')
}

RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)


def user_directory_path(instance, filename):
    return f'{instance.user.id}/{filename}'


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat')
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50"/>' % (self.image.url))
        
    def __str__(self):
        return str(self.name)


class PreCategory(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='precat')
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category", default="category.jpg")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "PreCategories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50"/>' % (self.image.url))
        
    def __str__(self):
        return str(self.name)


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Nestify")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
   

    class Meta:
        verbose_name_plural = "Vendors"


    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='prod')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    precategory = models.ForeignKey(PreCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags', null=True, blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="product", default="product.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=9999, decimal_places=2)
    old_price = models.DecimalField(max_digits=9999, decimal_places=2,  blank=True, null=True)

    

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    product_character = models.CharField(choices=PRODUCT_CHARACTER, max_length=10, default="new")

    date  = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(null=True, blank=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Products"
    
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" heigth="50"/>' % (self.image.url))
    

    def get_product_img(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


    def get_precentage(self):
        new_price = 100 - (self.price * 100) / self.old_price
        return new_price


    def get_reviews_count(self):
        return len(self.reviews.all())


    def average_rating(self):
        reviews_data = self.reviews.all()
        revs = reviews_data.aggregate(Avg('rating')).get('rating__avg')
        return revs if revs else 0


    def get_reviews_precentage(self):
        reviews_data = self.reviews.all()
        reviews_count = len(reviews_data)
        revs = 0
        for i in reviews_data:
            revs += i.rating
        try:
            return revs * 100 / (reviews_count * 5) 
        except:
            return 0
            
    
    def __str__(self):
        return str(self.title)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, related_name="product_info", on_delete=models.SET_NULL, null=True)
    parametrs = models.CharField(max_length=100, null=True, blank=True)
    parameter_description = models.CharField(max_length=200, null=True, blank=True)


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating
    

    def calculate_star_percentages(self):
        total_reviews = self.objects.count()

        if total_reviews == 0:
            return {
                '5 star': 0,
                '4 star': 0,
                '3 star': 0,
                '2 star': 0,
                '1 star': 0
            }

        reviews_5_star = self.objects.filter(rating=5).count()
        reviews_4_star = self.objects.filter(rating=4).count()
        reviews_3_star = self.objects.filter(rating=3).count()
        reviews_2_star = self.objects.filter(rating=2).count()
        reviews_1_star = self.objects.filter(rating=1).count()

        percentage_5_star = (reviews_5_star / total_reviews) * 100
        percentage_4_star = (reviews_4_star / total_reviews) * 100
        percentage_3_star = (reviews_3_star / total_reviews) * 100
        percentage_2_star = (reviews_2_star / total_reviews) * 100
        percentage_1_star = (reviews_1_star / total_reviews) * 100

        return {
            '5 star': round(percentage_5_star, 2),
            '4 star': round(percentage_4_star, 2),
            '3 star': round(percentage_3_star, 2),
            '2 star': round(percentage_2_star, 2),
            '1 star': round(percentage_1_star, 2)
        }
    

class Whishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"{self.user}'s cart")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price_sum = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price_sum = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(f"{self.product} product at  {self.cart.user} cart")


class OrderItem(models.Model):
    order_of_item = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # manager = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True, related_name='managers')
    address = models.CharField(max_length=250, default="")
    created = models.DateTimeField(auto_now_add=False, blank=True, null=True, default=timezone.now)
    updated = models.DateTimeField(auto_now_add=False, blank=True, null=True, default=timezone.now)
    file = models.FileField(default="", null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Processing")
    phone = models.CharField(max_length=20, default="")
    payment_method = models.CharField(max_length=20, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.full_name}"