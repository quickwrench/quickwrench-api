from django.db import models


class CarMake(models.Model):

    name: models.CharField = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
