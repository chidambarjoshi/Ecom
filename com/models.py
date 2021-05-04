from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ''' Image file validation '''
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg', '.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone=None, password=None,photo='',*args, **kwargs):
        print(email,photo)
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            photo=photo,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone=None, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone=phone,
            password=password,
            )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    '''
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    '''
    ext = filename.split('.')[-1]
    filename1 = "%s.%s" % (instance.slug, ext)
    return '{0}/{1}'.format(instance.slug, filename1)
class Users(AbstractUser):
    GENDER_CHOICES = (('', 'Gender'),('Male', 'Male'), ('Female', 'Female'), ('Other', 'Prefer Not To Say'))
    username = None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True )
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    slug = models.SlugField(editable=False, max_length=25)
    photo = models.ImageField(upload_to= user_directory_path , height_field=None, width_field=None, max_length=100, null=True,
                              blank=True, validators=[validate_file_extension])


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    objects = UserManager()

    def get_unique_slug(self):
        num = 1
        name = self.first_name + ' ' + self.last_name
        slug_default = slugify(name)
        slug = slug_default
        unique_slug = slug
        while Users.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(slug_default, num)
            unique_slug = slug
            num = num + 1
        return unique_slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(Users, self).save()

    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        return name