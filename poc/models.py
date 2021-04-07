from django.db import models

# Create your models here.


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # JSON-serialized (text) version of skills
    skills = models.TextField(null=True)
    email = models.EmailField(max_length=254)

    #degree = models.TextField(null=True)
    #field = models.TextField(null=True)

    class Meta:
        db_table = "candidate"
