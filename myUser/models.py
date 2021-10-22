from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
status = (('available','available'),('busy','busy'))

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,name,email,address,phone_no,password=None):
        user = self.model(
            email = self.normalize_email(email),
            name =name,
            address= address,
            phone_no = phone_no
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,name,email,address,phone_no,password=None):
        user =self.create_user(
            name,
            email,
            address,
            phone_no,
            password
        )
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True,verbose_name='Email')
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
    image = models.ImageField(upload_to='user/',null=True,blank=False)
    caretaker_status = models.CharField(max_length=9,choices=status,null=True,blank=True)
    is_customer = models.BooleanField(default=False)
    is_Caretaker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin= models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = ['name','address','phone_no']
    def __str__(self):
        return self.name

    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



