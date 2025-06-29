# Generated by Django 5.2 on 2025-06-13 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('headline', models.CharField(blank=True, max_length=150)),
                ('summary', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True, help_text='Comma-separated skills')),
                ('education', models.TextField(blank=True)),
                ('experience', models.TextField(blank=True)),
                ('projects', models.TextField(blank=True)),
                ('certifications', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
