# Generated by Django 4.2.21 on 2025-05-11 07:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0002_alter_administrator_admin_id_and_more'),
        ('students', '0002_course_alter_registration_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='course',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='student',
        ),
        migrations.AlterField(
            model_name='registration',
            name='academic_year',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Academic year must be in the format: "2023-2024".', regex='^\\d{4}-\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='registration',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrators.course'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='semester',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Semester must contain only letters, numbers, and spaces.', regex='^[A-Za-z0-9\\s]+$')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Student ID must be 8-10 digits.', regex='^\\d{8,10}$')]),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
