# Generated by Django 3.2.7 on 2021-09-28 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_Extract', '0002_alter_customer_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['email']},
        ),
    ]
