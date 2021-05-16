# Generated by Django 3.1.10 on 2021-05-16 06:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_auto_20210515_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('transaction_id', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SentMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('line_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('currency', models.CharField(max_length=128)),
                ('rate', models.DecimalField(decimal_places=9, max_digits=20)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sent_amount', models.IntegerField()),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfer.transaction')),
                ('transfer_to', models.ForeignKey(editable=False, max_length=255, on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('line_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('recipient', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=128)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=20)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('received_amount', models.IntegerField()),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfer.transaction')),
                ('transfer_from', models.ForeignKey(editable=False, max_length=255, on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
    ]
