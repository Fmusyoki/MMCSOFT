from django.db import models
from django.contrib.auth.models import User

#tasks

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    #assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    due_date = models.DateField()

    class Meta:
        db_table = "tasks"
# clients
class Client(models.Model):
    client_name = models.CharField(max_length=200)
    project_name = models.TextField(blank=True, null=True)
    client_year = models.DateField()
    contact_person = models.TextField(blank=True, null=True)
    email =  models.CharField(max_length=200)
    phone_number = models.IntegerField()
    client_image = models.ImageField(blank=True, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)  # set only once on create
    #updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table = "clients"
#users
class User(models.Model):
    Username = models.CharField(max_length=200)
    Email =  models.CharField(max_length=200)
    Password =  models.CharField(max_length=200)

    class Meta:
        db_table = "users"
#TENDERS
class Tender(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('ongoing', 'Ongoing'),
    ]

    tender_name = models.CharField(max_length=255, verbose_name="Tender Name")
    ref_no = models.CharField(max_length=100, unique=True, verbose_name="Reference Number")
    issue_date = models.DateField(verbose_name="Issue Date")
    submission_date = models.DateField(verbose_name="Submission Date")
    #assigned_to = models.ForeignKey(
        #User,
       # on_delete=models.SET_NULL,
       # null=True,
       # blank=True,
       # related_name="tenders",
       # verbose_name="Assigned To"
   # )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    comments = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tenders"

#INVOICES

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('fully_paid', 'Fully Paid'),
        ('partially_paid', 'Partially Paid'),
        ('overdue', 'Overdue'),
    ]

    invoice_no = models.CharField(max_length=50, unique=True, verbose_name="Invoice NO")
    client = models.CharField(max_length=255, verbose_name="Client")
    project = models.CharField(max_length=255, verbose_name="Project")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='partially_paid')
    due_date = models.DateField(verbose_name="Due Date")

    class Meta:
        db_table = "invoices"

