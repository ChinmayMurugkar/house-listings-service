from django.db import models
from django.core.validators import MinValueValidator

# TODO: Create your models here.

class House(models.Model):
    area_unit = models.CharField(max_length=10)
    bathrooms = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    bedrooms = models.IntegerField(validators=[MinValueValidator(0)])
    home_size = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    home_type = models.CharField(max_length=50)
    last_sold_date = models.DateField(null=True, blank=True)
    last_sold_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    link = models.URLField()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    property_size = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    rent_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    rentzestimate_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    rentzestimate_last_updated = models.DateField(null=True, blank=True)
    tax_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    tax_year = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    zestimate_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    zestimate_last_updated = models.DateField(null=True, blank=True)
    zillow_id = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"

    class Meta:
        verbose_name = "House"
        verbose_name_plural = "Houses"
        ordering = ['-price']
