# Generated by Django 4.0.3 on 2022-06-01 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_profile_forgot_password_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forgot_password_token',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]
