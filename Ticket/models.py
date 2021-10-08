from django.db import models
from myUser.models import User
from Category.models import Category

# Create your models here.
class Ticket(models.Model):
    subject = models.CharField(max_length=30)
    description = models.TextField(max_length=50,blank=True,null=True)
    category  = models.ForeignKey(Category,models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='ticket/',null=True,blank=True)
    status = models.BooleanField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ticketAssign(models.Model):
    ticketId    = models.ForeignKey(User,on_delete=models.CASCADE,null=True,)
    caretakerId = models.ForeignKey(User,on_delete=models.CASCADE,related_name='caretaker_id',null=True,blank=True)
    customerId  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer_id',null=True,blank=True)
    status  = models.BooleanField(default=1)
    assigned_at = models.DateTimeField(auto_now_add=True)


    def __int__(self):
        return self.ticketId
    class Meta:
        db_table = 'ticket_assign'
       # unique_together = ('ticketId','caretakerId')

class ticketConversation(models.Model):
    ticketId = models.ForeignKey(Ticket, on_delete=models.PROTECT,null=True,blank=True)
    message = models.TextField(max_length=30)
    caretakerId = models.ForeignKey(User, on_delete=models.PROTECT, related_name='caretaker_ids', null=True, blank=True)
    customerId = models.ForeignKey(User, on_delete=models.PROTECT ,related_name='customer_ids', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self):
        return self.ticketId


