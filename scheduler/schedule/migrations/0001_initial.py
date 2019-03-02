# Generated by Django 2.1.7 on 2019-03-02 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('state', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
                ('participants', models.ManyToManyField(related_name='schedule_participants', to=settings.AUTH_USER_MODEL)),
                ('registrant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule_registrant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
