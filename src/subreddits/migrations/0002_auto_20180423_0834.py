# Generated by Django 2.0.3 on 2018-04-23 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddits', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subreddit',
            options={'ordering': ('url', 'id'), 'verbose_name': 'Sub', 'verbose_name_plural': 'Subs'},
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='url',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]