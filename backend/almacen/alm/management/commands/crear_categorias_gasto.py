from django.core.management.base import BaseCommand
from alm.models import CategoriaGasto


class Command(BaseCommand):
    help = 'Crea las categorías de gasto predefinidas'

    def handle(self, *args, **options):
        categorias = [
            'GASTOS DE PERSONAL',
            'HONORARIO',
            'IMPUESTOS',
            'ARRENDAMIENTOS',
            'CONTRIBUCIONES Y AFILIACIONES',
            'SEGUROS',
            'SERVICIOS',
            'GASTOS LEGALES',
            'MANTENIMIENTO Y REPARACIONES',
            'ADECUACION E INSTALACION',
            'GASTOS DE VIAJE',
            'OTRO'
        ]

        self.stdout.write('Creando categorías de gasto...')
        creadas = 0
        existentes = 0

        for nombre in categorias:
            categoria, created = CategoriaGasto.objects.get_or_create(
                nombre=nombre,
                defaults={'activo': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'+ Creada: {nombre}'))
                creadas += 1
            else:
                self.stdout.write(f'  Ya existe: {nombre}')
                existentes += 1

        self.stdout.write(self.style.SUCCESS(f'\n=== Resumen ==='))
        self.stdout.write(self.style.SUCCESS(f'Categorías creadas: {creadas}'))
        self.stdout.write(f'Categorías existentes: {existentes}')
        self.stdout.write(f'Total: {len(categorias)}')
