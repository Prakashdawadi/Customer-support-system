from django.db import models
from myUser.models import User
status = (('active','active'),('inactive','inactive'))

# Create your models here.
class Category(models.Model):
    category = models.CharField(unique=True,max_length=20)
    created_by = models.ForeignKey(User,related_name='created_by_user', on_delete=models.CASCADE,blank=True,null=True)
    updated_by = models.ForeignKey(User, related_name='updated_by_user',on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=8,choices=status,default=status[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category
    #
    class Meta:
        ordering = ['updated_at']

