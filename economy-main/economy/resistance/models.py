from django.db import models
from django_jalali.db import models as jmodels

# Create your models here.

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, phone, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=phone,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class InformationFund(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام نام خانوادگی")
    nCode = models.CharField(max_length=10, verbose_name="کد ملی")
    fName = models.CharField(max_length=100, verbose_name="نام پدر")
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    cGroup = models.CharField(max_length=100, blank=False, null=True, verbose_name="کد گروه")

    def __str__(self):
        return self.name


class Fund(models.Model):
    COURSE_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    BAZZAR_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    fund = models.OneToOneField(InformationFund, on_delete=models.CASCADE)
    member = models.CharField(max_length=100, verbose_name="تعداد اعضا")
    NumberOfLoans = models.CharField(max_length=100, verbose_name="تعداد وام")
    mony = models.CharField(max_length=30, verbose_name="مبلغ پرداختی")
    quantity = models.CharField(max_length=30, verbose_name="موجودی")
    AfterTheSize = models.CharField(max_length=30, verbose_name="پس انداز")
    course = models.CharField(max_length=1, choices=COURSE_CHOICES)
    bazaar = models.CharField(max_length=1, choices=BAZZAR_CHOICES)
    name_course = models.CharField(max_length=100, blank=False, null=True, verbose_name="نام دوره")
    member_course = models.CharField(max_length=100, blank=False, null=True, verbose_name="تعداد شرکت کننده")
    name_teacher = models.CharField(max_length=100, blank=False, null=True, verbose_name="نام استاد")
    phone_teacher = models.CharField(max_length=11, blank=False, null=True, verbose_name="شماره استاد")
    bazzar_desc = models.TextField(blank=False, null=True, verbose_name="توضیحات بازارچه")

    def __str__(self):
        return self.fund.name


class Deprivation(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام نام خانوادگی")
    nCode = models.CharField(max_length=10, verbose_name="کد ملی")
    fName = models.CharField(max_length=100, verbose_name="نام پدر")
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    cGroup = models.CharField(max_length=100, verbose_name="کد گروه")
    fund_name = models.CharField(max_length=100, blank=False, null=True, verbose_name="نام صندوق")

    def __str__(self):
        return self.name


class Report(models.Model):
    deprivation = models.ForeignKey(Deprivation, on_delete=models.CASCADE)
    date = jmodels.jDateField(verbose_name="تاریخ انجام برنامه")
    address = models.CharField(max_length=150, verbose_name="آدرس")
    subject = models.CharField(max_length=150, verbose_name="موضوع")
    desc = models.TextField(verbose_name="توضیحات")
    member = models.CharField(max_length=100, verbose_name="تعداد اعضا")

    def __str__(self):
        return self.deprivation.name
