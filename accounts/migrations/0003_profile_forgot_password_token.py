# Generated by Django 4.0.3 on 2022-05-31 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forgot_password_token',
            field=models.CharField(default=1234, max_length=100),
            preserve_default=False,
        ),
    ]
