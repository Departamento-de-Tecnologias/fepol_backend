# Generated by Django 4.0.2 on 2022-06-04 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id_member',
        ),
        migrations.AddField(
            model_name='member',
            name='id_student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.student'),
        ),
    ]
