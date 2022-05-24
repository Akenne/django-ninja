import uuid
from django.db import models
import requests

class Loss(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    company_id = models.CharField(max_length=256)
    company_name = models.CharField(max_length=512)
    scenario = models.IntegerField()
    total = models.DecimalField(max_digits=100, decimal_places=50)
    hurricane = models.DecimalField(max_digits=100, decimal_places=50)
    flood = models.DecimalField(max_digits=100, decimal_places=50)
    storm = models.DecimalField(max_digits=100, decimal_places=50)
    wildfire = models.DecimalField(max_digits=100, decimal_places=50)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.company_name
        