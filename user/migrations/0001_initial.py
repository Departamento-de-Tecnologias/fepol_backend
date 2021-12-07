# Generated by Django 3.1.7 on 2021-04-15 16:45

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('card_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('born_date', models.DateField()),
                ('genre', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1)),
                ('signature', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('enrollment_id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('level', models.CharField(choices=[('100', '100-I'), ('100', '100-II'), ('200', '200-I'), ('200', '200-II'), ('300', '300-I'), ('300', '300-II'), ('400', '400-I'), ('400', '400-II'), ('500', '500-I'), ('500', '500-II')], max_length=6)),
                ('photo', models.CharField(blank=True, max_length=100, null=True)),
                ('id_person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.person')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.person')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('description', models.CharField(max_length=100)),
                ('date_joined', models.DateField(auto_now=True)),
                ('role', models.CharField(choices=[('A', 'Presidente'), ('B', 'Vicepresidente'), ('C', 'Secretario'), ('D', 'Tesorero'), ('E', 'Vocal'), ('F', 'Miembro'), ('N', 'Ninguno'), ('X', 'Asesor'), ('Y', 'Tutor'), ('Z', 'Externo')], default='F', max_length=2)),
                ('permissions', models.CharField(choices=[('A', 'Presidente'), ('B', 'Vicepresidente'), ('C', 'Sub Organización'), ('D', 'Miembro'), ('N', 'Ninguno')], default='N', max_length=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('id_student', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Members',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]