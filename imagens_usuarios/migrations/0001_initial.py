# Generated by Django 3.1.2 on 2020-10-20 14:47

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instituicao', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagensUsuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', cloudinary.models.CloudinaryField(max_length=255, verbose_name='imagem')),
                ('instit_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='instituicao.instit', verbose_name='id instituicao')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='id usuario')),
            ],
        ),
    ]
