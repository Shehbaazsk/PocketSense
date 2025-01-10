# Generated by Django 5.1.4 on 2025-01-10 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expenses', '0004_expensesplit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending', max_length=20)),
                ('settlement_method', models.CharField(max_length=100)),
                ('due_date', models.DateField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('expense_split', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settlements', to='expenses.expensesplit')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('payee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to=settings.AUTH_USER_MODEL)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
