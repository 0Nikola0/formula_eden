# Generated by Django 4.0.5 on 2022-07-26 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formula_app', '0015_alter_sesija_datum'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrkaSesija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sesija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formula_app.sesija')),
            ],
        ),
        migrations.AlterField(
            model_name='trka',
            name='sesii',
            field=models.ManyToManyField(blank=True, through='formula_app.TrkaSesija', to='formula_app.sesija'),
        ),
        migrations.AddField(
            model_name='trkasesija',
            name='trka',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formula_app.trka'),
        ),
    ]