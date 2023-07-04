from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


class ProfileDetails(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    first_name = models.CharField(
        max_length=30,
        validators=(
            MinLengthValidator(2),
        ),
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=30,
        validators=(
            MinLengthValidator(2),
        ),
        blank=True,
        null=True,
    )

    phone_number = PhoneNumberField()

    age = models.PositiveIntegerField()



    # Добавете останалата информация, която искате да съхранявате

    def __str__(self):
        return self.username
