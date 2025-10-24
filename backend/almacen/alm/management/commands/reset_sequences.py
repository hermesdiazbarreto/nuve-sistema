"""
Comando Django para resetear las secuencias de PostgreSQL.

Esto corrige el error: duplicate key value violates unique constraint "alm_productovariante_pkey"
que ocurre cuando la secuencia de autoincremento está desincronizada.

Uso:
    python manage.py reset_sequences
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Resetea las secuencias de PostgreSQL para que coincidan con el MAX(id) actual'

    def handle(self, *args, **options):
        """
        Resetea todas las secuencias de las tablas que usan autoincremento.
        Esto es necesario cuando se importan datos con IDs específicos.
        """
        self.stdout.write(self.style.WARNING('Reseteando secuencias de PostgreSQL...'))

        # Lista de tablas que tienen secuencias de autoincremento
        tablas = [
            'alm_categoria',
            'alm_marca',
            'alm_talla',
            'alm_color',
            'alm_producto',
            'alm_productovariante',
            'alm_cliente',
            'alm_proveedor',
            'alm_venta',
            'alm_detalleventa',
            'alm_pagoventa',
            'alm_compra',
            'alm_detallecompra',
            'alm_movimientoinventario',
            'alm_categoriagasto',
            'alm_gasto',
            'alm_promocionwhatsapp',
            'alm_enviowhatsapp',
        ]

        with connection.cursor() as cursor:
            for tabla in tablas:
                try:
                    # Resetear la secuencia al valor máximo actual + 1
                    cursor.execute(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{tabla}', 'id'),
                            COALESCE((SELECT MAX(id) FROM {tabla}), 1),
                            true
                        );
                    """)

                    nuevo_valor = cursor.fetchone()[0]

                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {tabla}: secuencia reseteada a {nuevo_valor}')
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error en {tabla}: {str(e)}')
                    )

        self.stdout.write(self.style.SUCCESS('\n¡Secuencias reseteadas correctamente!'))
        self.stdout.write(self.style.WARNING(
            'Ahora puedes crear nuevas variantes sin errores de duplicate key.'
        ))