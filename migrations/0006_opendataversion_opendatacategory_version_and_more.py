# Generated by Django 4.1.9 on 2023-05-23 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_default_version(apps, schema_editor):
    OpenDataVersion = apps.get_model('open_data_plugin', 'OpenDataVersion')
    OpenDataVersion.objects.create(name='base', code='base')


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('open_data_plugin', '0005_alter_opendatastorecategory_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenDataVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('code', models.CharField(max_length=16, unique=True)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_default_version),
        migrations.AddField(
            model_name='opendatacategory',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opendataconversion',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opendatafood',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opendataproperty',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opendatastore',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opendataunit',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='open_data_plugin.opendataversion'),
            preserve_default=False,
        ),
    ]
