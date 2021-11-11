# Generated by Django 2.2.16 on 2021-11-11 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20211111_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genres',
        ),
        migrations.CreateModel(
            name='Genre_Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.Genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='reviews.Title')),
            ],
        ),
    ]
