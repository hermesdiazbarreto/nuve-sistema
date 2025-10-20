"""
Comando Django para limpiar variantes duplicadas o huérfanas
"""
from django.core.management.base import BaseCommand
from alm.models import ProductoVariante

class Command(BaseCommand):
    help = 'Elimina variantes duplicadas basándose en producto+talla+color'

    def add_arguments(self, parser):
        parser.add_argument(
            '--codigo',
            type=str,
            help='Eliminar variante específica por codigo_variante',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se eliminaría sin realmente eliminarlo',
        )

    def handle(self, *args, **options):
        codigo = options.get('codigo')
        dry_run = options.get('dry_run', False)

        if codigo:
            # Eliminar variante específica por código
            try:
                variantes = ProductoVariante.objects.filter(codigo_variante=codigo)
                count = variantes.count()

                if count == 0:
                    self.stdout.write(self.style.WARNING(
                        f'No se encontró ninguna variante con código: {codigo}'
                    ))
                    return

                if dry_run:
                    self.stdout.write(self.style.WARNING(
                        f'[DRY RUN] Se eliminarían {count} variante(s) con código: {codigo}'
                    ))
                    for v in variantes:
                        self.stdout.write(f'  - ID: {v.id}, Producto: {v.producto}, Talla: {v.talla}, Color: {v.color}')
                else:
                    for v in variantes:
                        self.stdout.write(f'Eliminando: {v.codigo_variante} (ID: {v.id})')
                    variantes.delete()
                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Se eliminaron {count} variante(s) con código: {codigo}'
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error: {e}'))
                raise
        else:
            # Limpiar duplicados basados en unique_together (producto, talla, color)
            duplicados_eliminados = 0

            # Obtener todas las combinaciones únicas
            combinaciones = ProductoVariante.objects.values('producto', 'talla', 'color').distinct()

            for combo in combinaciones:
                variantes = ProductoVariante.objects.filter(
                    producto=combo['producto'],
                    talla=combo['talla'],
                    color=combo['color']
                ).order_by('id')

                if variantes.count() > 1:
                    # Mantener la primera, eliminar las demás
                    primera = variantes.first()
                    duplicadas = variantes.exclude(id=primera.id)

                    if dry_run:
                        self.stdout.write(self.style.WARNING(
                            f'[DRY RUN] Se eliminarían {duplicadas.count()} duplicado(s) de: {primera}'
                        ))
                        for d in duplicadas:
                            self.stdout.write(f'  - ID: {d.id}, Código: {d.codigo_variante}')
                    else:
                        count = duplicadas.count()
                        self.stdout.write(f'Eliminando {count} duplicado(s) de: {primera}')
                        for d in duplicadas:
                            self.stdout.write(f'  - Eliminado: {d.codigo_variante} (ID: {d.id})')
                        duplicadas.delete()
                        duplicados_eliminados += count

            if duplicados_eliminados > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Se eliminaron {duplicados_eliminados} variante(s) duplicada(s)'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    '✓ No se encontraron variantes duplicadas'
                ))
