# Generated by Django 4.0.5 on 2022-08-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula_app', '0018_trka_pozadina_slika_trka_staza_slika_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trka',
            name='kraj',
            field=models.DateField(default='2022-08-02'),
        ),
        migrations.AlterField(
            model_name='trka',
            name='pocetok',
            field=models.DateField(default='2022-08-02'),
        ),
    ]
