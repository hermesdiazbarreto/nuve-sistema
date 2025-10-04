# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alm', '0003_alter_venta_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='tipo_movimiento',
            field=models.CharField(
                choices=[('INGRESO', 'Ingreso'), ('EGRESO', 'Egreso')],
                default='INGRESO',
                max_length=10
            ),
        ),
    ]
