from django.db import models

# Create your models here.
class MailList(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'Name: {self.name} - Email: {self.email}'
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    date_seen = models.DateTimeField(null=True)

    def __str__(self):
        if self.seen:
            return f"Date Sent: {self.date_added}:Opened on {self.date_seen}  From- {self.name} Subject - {self.subject}"
        else:
            return f"Sent By - {self.name} Subject - {self.subject} Sent On {self.date_added} Status (Not Opened)"

class ShortEstimate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    service = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} requested an estimate for {self.service} on {self.date_added}.'
    
class LongEstimate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    service_frequency = models.CharField(max_length=100)
    publicity = models.CharField(max_length=100)
    comments = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} who heard about the company from {self.publicity} requested an estimate for {self.service} on {self.date_added}.'

class Question(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    question = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Question from {self.name} on {self.date_added}.'
