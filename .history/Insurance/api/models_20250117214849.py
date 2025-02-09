from django.db import models

class Insurance(models.Model):
    MALE = 0
    FEMALE = 1
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    SOUTHEAST = 0
    SOUTHWEST = 1
    NORTHEAST = 2
    NORTHWEST = 3
    REGION_CHOICES = (
        (NORTHWEST, 'Northwest'),
        (NORTHEAST, 'Northeast'),
        (SOUTHWEST, 'Southwest'),
        (SOUTHEAST, 'Southeast'),
    )

    age = models.FloatField()
    sex = models.IntegerField(choices=SEX_CHOICES)
    bmi = models.FloatField()
    children = models.FloatField()
    smoker = models.IntegerField(choices=((0, 'Smoker'), (1, 'Non-Smoker')))
    region = models.IntegerField(choices=REGION_CHOICES)
    
    def __str__(self):
        return f"Insurance Info: {self.age} years, {self.get_sex_display()}, {self.get_region_display()}"
