# Generated by Django 2.2.4 on 2019-11-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hx_lti_assignment', '0003_assignment_common_inst_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='highlights_options',
            field=models.TextField(blank=True, max_length=1024),
        ),
    ]
