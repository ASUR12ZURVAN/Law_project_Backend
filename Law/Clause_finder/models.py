from django.db import models

# Create your models here.


class Document_Text(models.Model):
    Text = models.CharField(max_length=1000000)
    Total_Clauses = models.IntegerField()
    Dangerous_Clauses = models.IntegerField()
    suggestions_generated = models.TextField()
    suggestions = models.IntegerField()
    Proofreading_score = models.IntegerField()

    
