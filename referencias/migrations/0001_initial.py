# Generated by Django 3.1.2 on 2020-12-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Referencias',
            fields=[
                ('id_referencia', models.AutoField(primary_key=True, serialize=False)),
                ('id_pessoa_cod_fk', models.IntegerField()),
                ('situacao', models.IntegerField()),
                ('tipo', models.CharField(blank=True, max_length=15, null=True)),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('endereco', models.CharField(blank=True, max_length=100, null=True)),
                ('data_criacao', models.DateTimeField(blank=True, null=True)),
                ('data_atualizacao', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'referencias',
                'managed': False,
            },
        ),
    ]
