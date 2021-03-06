# Generated by Django 3.1.2 on 2020-12-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Refbanco',
            fields=[
                ('id_banco', models.AutoField(primary_key=True, serialize=False)),
                ('id_pessoa_cod_fk', models.IntegerField()),
                ('id_bancos_fk', models.IntegerField()),
                ('situacao', models.IntegerField()),
                ('agencia', models.CharField(blank=True, max_length=6, null=True)),
                ('conta', models.CharField(blank=True, max_length=10, null=True)),
                ('abertura', models.DateTimeField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=50, null=True)),
                ('data_criacao', models.DateTimeField(blank=True, null=True)),
                ('data_atualizacao', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'refbanco',
                'managed': False,
            },
        ),
    ]
