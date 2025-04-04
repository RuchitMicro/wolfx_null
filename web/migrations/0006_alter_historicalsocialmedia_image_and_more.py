# Generated by Django 4.2.7 on 2025-04-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_historicalsocialmedia_default_llm_prompt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsocialmedia',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='social_media/'),
        ),
    ]
