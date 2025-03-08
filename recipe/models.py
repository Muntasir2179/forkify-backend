from django.db import models
import random, string

# Create your models here.

class Unit(models.Model):
    unit_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.unit_name

class Ingredient(models.Model):
    quantity = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='unit')
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return f'{self.quantity} {self.unit} {self.description}'


def generate_unique_id():
    """Generate a unique 24-character alphanumeric ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

class Recipes(models.Model):
    id = models.CharField(max_length=24, primary_key=True, unique=True, default=generate_unique_id, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cooking_time = models.IntegerField()
    image_url = models.URLField()
    publisher = models.CharField(max_length=50)
    servings = models.IntegerField()
    source_url = models.URLField()
    title = models.CharField(max_length=100)
    key = models.TextField(max_length=500, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    
    class Meta:
        verbose_name_plural = 'Recipes'
    
    def __str__(self):
        return self.title
