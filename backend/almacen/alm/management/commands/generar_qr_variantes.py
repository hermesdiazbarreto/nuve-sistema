from django.core.management.base import BaseCommand
from alm.models import ProductoVariante


class Command(BaseCommand):
    help = 'Genera códigos QR para todas las variantes de productos que no tienen uno'

    def add_arguments(self, parser):
        parser.add_argument(
            '--regenerar',
            action='store_true',
            help='Regenera QR codes incluso para variantes que ya tienen uno',
        )

    def handle(self, *args, **options):
        regenerar = options['regenerar']

        if regenerar:
            variantes = ProductoVariante.objects.all()
            mensaje = 'Regenerando QR codes para todas las variantes...'
        else:
            variantes = ProductoVariante.objects.filter(qr_code='')
            mensaje = 'Generando QR codes para variantes sin QR...'

        self.stdout.write(self.style.SUCCESS(mensaje))
        self.stdout.write(f'Variantes encontradas: {variantes.count()}')

        contador = 0
        errores = 0

        for variante in variantes:
            try:
                variante.generar_qr()
                variante.save()
                contador += 1
                self.stdout.write(f'[OK] QR generado para: {variante.codigo_variante}')
            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] Error en {variante.codigo_variante}: {str(e)}')
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Proceso completado:'))
        self.stdout.write(f'  - QR codes generados: {contador}')
        self.stdout.write(f'  - Errores: {errores}')
