# Generated by Django 4.0.4 on 2022-06-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45, unique=True)),
                ('name', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=45, unique=True)),
                ('point', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]