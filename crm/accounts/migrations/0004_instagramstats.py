# Generated by Django 4.2.3 on 2023-07-16 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_instagramprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_link', models.URLField()),
                ('comments', models.JSONField()),
            ],
        ),
    ]
