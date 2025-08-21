from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db import models


class OpenDataUser(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    moderator_user = models.BooleanField(default=False)
    verified_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class OpenDataVersion(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=16, unique=True)

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.code})'


class OpenDataBaseModel(models.Model):
    slug = models.CharField(max_length=128, unique=True)
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.ForeignKey(OpenDataVersion, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class OpenDataUnit(OpenDataBaseModel):
    name = models.CharField(max_length=128, unique=True)
    plural_name = models.CharField(max_length=128, unique=True, blank=True)
    base_unit = models.CharField(max_length=128, blank=True,
                                 choices=(
                                     ('g', 'g'),
                                     ('kg', 'kg'),
                                     ('ounce', 'ounce'),
                                     ('pound', 'pound'),
                                     ('ml', 'ml'),
                                     ('l', 'l'),
                                     ('fluid_ounce', 'fluid_ounce'),
                                     ('pint', 'pint'),
                                     ('quart', 'quart'),
                                     ('gallon', 'gallon'),
                                     ('tbsp', 'tbsp'),
                                     ('tsp', 'tsp'),
                                     ('us_cup', 'US Cup'),
                                     ('imperial_fluid_ounce', 'imperial fluid ounce'),
                                     ('imperial_pint', 'imperial pint'),
                                     ('imperial_quart', 'imperial quart'),
                                     ('imperial_gallon', 'imperial gallon'),
                                     ('imperial_tbsp', 'imperial tbsp'),
                                     ('imperial_tsp', 'imperial tsp'),
                                 ))
    type = models.CharField(max_length=128, choices=(('WEIGHT', 'weight'), ('VOLUME', 'volume'), ('OTHER', 'other'),))

    def __str__(self):
        return f'{self.name}'


class OpenDataCategory(OpenDataBaseModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.name}'


class OpenDataStore(OpenDataBaseModel):
    name = models.CharField(max_length=128, unique=True)
    categories = models.ManyToManyField(OpenDataCategory, through='OpenDataStoreCategory')

    def __str__(self):
        return f'{self.name}'


class OpenDataStoreCategory(models.Model):
    store = models.ForeignKey(OpenDataStore, on_delete=models.CASCADE, related_name='category_to_store')
    category = models.ForeignKey(OpenDataCategory, on_delete=models.CASCADE, related_name='category_to_store')
    order = models.BigIntegerField(default=0, db_index=True, )

    class Meta:
        ordering = ['order']


class OpenDataProperty(OpenDataBaseModel):
    name = models.CharField(max_length=128, unique=True)
    unit = models.CharField(max_length=16, blank=True)
    fdc_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class OpenDataFoodProperty(models.Model):
    property = models.ForeignKey(OpenDataProperty, on_delete=models.PROTECT)
    property_amount = models.DecimalField(default=0, decimal_places=16, max_digits=32)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.property} {self.property_amount}'


class OpenDataFood(OpenDataBaseModel):
    name = models.CharField(max_length=128, unique=True)
    plural_name = models.CharField(max_length=128, unique=True)
    store_category = models.ForeignKey(OpenDataCategory, on_delete=models.PROTECT)
    preferred_unit_metric = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, null=True, blank=True, default=None, related_name='preferred_unit_metric')
    preferred_shopping_unit_metric = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, null=True, blank=True, default=None, related_name='preferred_shopping_unit_metric')
    preferred_unit_imperial = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, null=True, blank=True, default=None, related_name='preferred_unit_imperial')
    preferred_shopping_unit_imperial = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, null=True, blank=True, default=None,
                                                         related_name='preferred_shopping_unit_imperial')
    properties = models.ManyToManyField(OpenDataFoodProperty, blank=True)

    properties_food_amount = models.IntegerField(default=100, blank=True)
    properties_food_unit = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, blank=True, null=True)
    properties_source = models.TextField(blank=True)

    fdc_id = models.IntegerField(null=True, default=None, blank=True)

    # TODO add alias support

    def __str__(self):
        return f'{self.name}'


class OpenDataConversion(OpenDataBaseModel):
    food = models.ForeignKey(OpenDataFood, on_delete=models.PROTECT)
    base_amount = models.DecimalField(default=0, decimal_places=16, max_digits=32)
    base_unit = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, related_name='conversion_base_relation')
    converted_amount = models.DecimalField(default=0, decimal_places=16, max_digits=32)
    converted_unit = models.ForeignKey(OpenDataUnit, on_delete=models.PROTECT, related_name='conversion_converted_relation')
    source = models.TextField()

    def __str__(self):
        return f'{self.food} {self.base_unit} -> {self.converted_unit}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['base_unit', 'converted_unit', 'food'], name='f_unique_conversion_per_food')
        ]
