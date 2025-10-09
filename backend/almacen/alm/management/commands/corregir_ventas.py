from django.core.management.base import BaseCommand
from alm.models import Venta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Corrige ventas marcadas incorrectamente como ABONO cuando están completamente pagadas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('BUSCANDO VENTAS CON ESTADO INCORRECTO'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        # Buscar ventas con estado ABONO
        ventas_problematicas = Venta.objects.filter(estado='ABONO')
        
        corregidas = 0
        
        for venta in ventas_problematicas:
            # Si el monto abonado es >= al total, debería estar PAGADO
            if venta.monto_abonado >= venta.total:
                self.stdout.write(f"Venta: {venta.numero_venta}")
                self.stdout.write(f"  Estado actual: {venta.estado}")
                self.stdout.write(f"  Total: {venta.total}")
                self.stdout.write(f"  Monto abonado: {venta.monto_abonado}")
                self.stdout.write(f"  Saldo pendiente: {venta.saldo_pendiente}")
                self.stdout.write(f"  Descuento: {venta.descuento}")
                
                # Corregir el estado
                venta.estado = 'PAGADO'
                venta.monto_abonado = venta.total
                venta.saldo_pendiente = Decimal('0.00')
                venta.save()
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ CORREGIDA → Estado: PAGADO, Saldo pendiente: 0.00\n"))
                corregidas += 1
        
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'TOTAL DE VENTAS CORREGIDAS: {corregidas}'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
