# Generated by Django 5.0 on 2024-01-07 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_visit_alter_post_snippet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='visit',
        ),
        migrations.AddField(
            model_name='post',
            name='visit',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]