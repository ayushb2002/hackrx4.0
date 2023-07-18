# Generated by Django 4.2.3 on 2023-07-18 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_employee_user'),
        ('leads', '0005_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='email',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='name',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='score',
        ),
        migrations.AddField(
            model_name='lead',
            name='handled_by',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.employee'),
        ),
        migrations.AddField(
            model_name='lead',
            name='location',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='lead',
            name='username',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='lead',
            name='status',
            field=models.CharField(choices=[('new', 'New Lead'), ('engaged', 'Engaged Lead'), ('qualified', 'Qualified Lead'), ('converted', 'Converted Lead'), ('lost', 'Lost Lead')], default='new', max_length=100),
        ),
    ]