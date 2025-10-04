"""
Management command para agregar la columna tipo_movimiento si no existe
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Agrega la columna tipo_movimiento a la tabla alm_venta si no existe'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            try:
                # Intentar agregar la columna
                cursor.execute("""
                    ALTER TABLE alm_venta
                    ADD COLUMN IF NOT EXISTS tipo_movimiento VARCHAR(10)
                    DEFAULT 'INGRESO' NOT NULL;
                """)

                self.stdout.write(
                    self.style.SUCCESS('✓ Columna tipo_movimiento verificada/agregada exitosamente')
                )
            except Exception as e:
                # Si ya existe o hay otro error, solo reportar
                self.stdout.write(
                    self.style.WARNING(f'Columna tipo_movimiento: {str(e)}')
                )