from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.EmailField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    stock_min = models.PositiveIntegerField(default=0)
    stock     = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/', null=True, blank=True)


    def __str__(self):
        return self.name



class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"IN: {self.product.name} ({self.quantity}) on {self.date}"
    
class StockOut(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
        date = models.DateField(auto_now_add=True)
        note = models.TextField(blank=True)

        def __str__(self):
            return f"OUT: {self.product.name} ({self.quantity}) on {self.date}"
