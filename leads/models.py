from django.db import models
from datetime import date, datetime, timezone
# Create your models here.
import datetime


class Leads(models.Model):
    STATUS = (
        ('Active Leads', 'Active'),
        ('Dead Leads', 'Dead'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10, default=None, null=True, blank=True)
    csv_file = models.FileField()

    email = models.EmailField()

    country = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default='Active Leads',choices=STATUS)
    is_deleted = models.BooleanField(default=False)
    # def __str__(self):
    #     return (f"{self.first_name} {self.last_name}")

    class Meta:
        db_table = "leads_leads"
        verbose_name = "leads"
