"""
Management command para agregar la columna tipo_movimiento si no existe
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Agrega la columna tipo_movimiento a la tabla alm_venta si no existe'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='alm_venta' AND column_name='tipo_movimiento';
            """)

            if cursor.fetchone():
                self.stdout.write(
                    self.style.WARNING('La columna tipo_movimiento ya existe')
                )
                return

            # Si no existe, agregarla
            try:
                cursor.execute("""
                    ALTER TABLE alm_venta
                    ADD COLUMN tipo_movimiento VARCHAR(10) DEFAULT 'INGRESO' NOT NULL;
                """)

                self.stdout.write(
                    self.style.SUCCESS('✓ Columna tipo_movimiento agregada exitosamente')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error al agregar columna: {str(e)}')
                )
                raise