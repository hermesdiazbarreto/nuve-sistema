"""
Comando Django para arreglar la columna codigo_variante permitiendo NULL
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Altera la columna codigo_variante para permitir valores en blanco'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # PostgreSQL: Eliminar NOT NULL de codigo_variante
                cursor.execute("""
                    ALTER TABLE alm_productovariante
                    ALTER COLUMN codigo_variante DROP NOT NULL;
                """)
                self.stdout.write(self.style.SUCCESS(
                    '✓ Columna codigo_variante actualizada correctamente: ahora permite valores vacíos'
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'✗ Error al actualizar la columna: {e}'
                ))
                raise
