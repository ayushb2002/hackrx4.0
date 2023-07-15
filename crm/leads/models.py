from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'New Lead'),
        ('engaged', 'Engaged Lead'),
        ('qualified', 'Qualified Lead'),
        ('converted', 'Converted Lead'),
        ('lost', 'Lost Lead'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    score = models.IntegerField(default=0)

    # Add other fields as needed for lead information

    def __str__(self):
        return self.name
