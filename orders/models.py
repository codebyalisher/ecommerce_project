from django.db import models
from products.models import Product
from users.models import Userm

class Order(models.Model):
    user = models.ForeignKey(Userm, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped')], default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

    def calculate_total(self):
        """Recalculate the total price of the order"""
        self.total_price = sum([product.price for product in self.products.all()])
        self.save()
