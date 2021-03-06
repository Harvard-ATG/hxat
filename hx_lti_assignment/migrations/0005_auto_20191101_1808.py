# Generated by Django 2.2.4 on 2019-11-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hx_lti_assignment", "0004_auto_20191101_1754"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="include_public_tab",
            field=models.BooleanField(
                default=True,
                help_text="Include a tab for peer annotations. Used for private annotations. If you want users to view each other's annotations.",
            ),
        ),
    ]
