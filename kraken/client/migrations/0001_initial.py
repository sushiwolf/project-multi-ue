# Generated by Django 2.0.5 on 2018-05-27 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_temp', models.DecimalField(decimal_places=10, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_name', models.CharField(max_length=200)),
                ('problem_algo_used', models.CharField(max_length=200)),
                ('problem_date_essai', models.DateTimeField(verbose_name='date published')),
                ('problem_length_cycle', models.DecimalField(decimal_places=2, max_digits=10)),
                ('problem_time_to_resolve', models.DecimalField(decimal_places=2, max_digits=5)),
                ('problem_author', models.CharField(max_length=200)),
                ('problem_param_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Param')),
            ],
        ),
        migrations.CreateModel(
            name='Problem_City_Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.City')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Problem')),
            ],
        ),
    ]
