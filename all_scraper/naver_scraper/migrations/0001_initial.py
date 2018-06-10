# Generated by Django 2.0 on 2018-02-24 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds', models.DateField(verbose_name='start date')),
                ('de', models.DateField(verbose_name='end date')),
                ('search_mode', models.IntegerField()),
                ('press_codes', models.CharField(max_length=500)),
                ('essential_word', models.CharField(max_length=200)),
                ('exact_word', models.CharField(max_length=200)),
                ('except_word', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_subject', models.CharField(max_length=1000)),
                ('news_date', models.DateField(verbose_name='news published date')),
                ('news_press', models.CharField(max_length=100)),
                ('news_url', models.CharField(max_length=2000)),
                ('news_body', models.CharField(max_length=100000)),
                ('search_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='naver_scraper.SearchCondition')),
            ],
        ),
    ]