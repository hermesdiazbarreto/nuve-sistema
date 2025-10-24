from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Talla(models.Model):
    nombre = models.CharField(max_length=10, unique=True)  # XS, S, M, L, XL, XXL
    orden = models.IntegerField(default=0)  # Para ordenar las tallas
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['orden']

class Color(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    codigo_hex = models.CharField(max_length=7, blank=True, null=True)  # #FF0000
    
    def __str__(self):
        return self.nombre

class ProductoManager(models.Manager):
    """Manager personalizado para excluir productos eliminados por defecto"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class ProductoAllManager(models.Manager):
    """Manager que incluye todos los productos, incluso eliminados"""
    def get_queryset(self):
        return super().get_queryset()

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Eliminado")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_eliminados', verbose_name="Eliminado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Managers
    objects = ProductoManager()  # Manager por defecto (excluye eliminados)
    all_objects = ProductoAllManager()  # Manager que incluye eliminados

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código automáticamente basado en categoría
            # Obtener las primeras 3 letras de la categoría en mayúsculas
            prefijo = self.categoria.nombre[:3].upper()

            # Buscar el último producto con ese prefijo
            last_producto = Producto.all_objects.filter(
                codigo__startswith=prefijo
            ).order_by('-id').first()

            if last_producto and '-' in last_producto.codigo:
                # Extraer el número del último código
                try:
                    last_number = int(last_producto.codigo.split('-')[1])
                    nuevo_numero = last_number + 1
                except (ValueError, IndexError):
                    nuevo_numero = 1
            else:
                nuevo_numero = 1

            # Generar el nuevo código: PREFIJO-001, PREFIJO-002, etc.
            self.codigo = f"{prefijo}-{nuevo_numero:03d}"

        super().save(*args, **kwargs)

    def soft_delete(self, user=None):
        """Método para realizar soft delete"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.activo = False  # También marcamos como inactivo
        self.save()
        # Desactivar variantes
        self.variantes.update(activo=False)

    def restore(self):
        """Método para restaurar un producto eliminado"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.activo = True
        self.save()
        # Reactivar variantes
        self.variantes.update(activo=True)

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    codigo_variante = models.CharField(max_length=100, unique=True, blank=True)
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.talla} - {self.color}"

    def generar_qr(self):
        """Genera el código QR para esta variante"""
        if not self.codigo_variante:
            return

        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.codigo_variante)
        qr.make(fit=True)

        # Generar imagen
        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar en un BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Guardar como archivo Django
        filename = f'qr_{self.codigo_variante}.png'
        self.qr_code.save(filename, ContentFile(buffer.read()), save=False)

    def save(self, *args, **kwargs):
        if not self.codigo_variante:
            # Generar código automáticamente: CODIGO_PRODUCTO-TALLA-PRIMERAS_3_LETRAS_COLOR
            # Ejemplo: SHO-010-6-AZU, SHO-010-10-BLA

            # Cargar instancias desde IDs si es necesario
            if self.producto_id:
                producto = Producto.all_objects.get(id=self.producto_id)
                producto_codigo = producto.codigo
            else:
                producto_codigo = "UNK"

            if self.talla_id:
                talla = Talla.objects.get(id=self.talla_id)
                talla_nombre = talla.nombre
            else:
                talla_nombre = "0"

            if self.color_id:
                color = Color.objects.get(id=self.color_id)
                codigo_color = color.nombre[:3].upper()
            else:
                codigo_color = "UNK"

            self.codigo_variante = f"{producto_codigo}-{talla_nombre}-{codigo_color}"

        # Generar QR si no existe (solo para registros nuevos)
        generar_qr_nuevo = False
        if not self.qr_code and self.codigo_variante and not self.pk:
            generar_qr_nuevo = True

        super().save(*args, **kwargs)

        # Generar el QR después de guardar para tener el ID
        if generar_qr_nuevo:
            self.generar_qr()
            # Usar update() en lugar de save() para evitar trigger del segundo INSERT
            ProductoVariante.objects.filter(pk=self.pk).update(qr_code=self.qr_code)

    class Meta:
        unique_together = ['producto', 'talla', 'color']
        verbose_name_plural = "Variantes de Producto"

class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI'),
        ('CE', 'Carné de Extranjería'),
        ('PASAPORTE', 'Pasaporte'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, default='DNI')
    numero_documento = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class Venta(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ABONO', 'Abono'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]

    TIPO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('MIXTO', 'Mixto'),
    ]

    TIPO_MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    numero_venta = models.CharField(max_length=20, unique=True)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES, default='INGRESO')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_pago = models.CharField(max_length=15, choices=TIPO_PAGO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        cliente_nombre = self.cliente.nombre_completo if self.cliente else "Cliente General"
        return f"Venta {self.numero_venta} - {cliente_nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_venta:
            # Generar número de venta automáticamente
            last_venta = Venta.objects.order_by('-id').first()
            if last_venta:
                last_number = int(last_venta.numero_venta.split('-')[1])
                self.numero_venta = f"V-{last_number + 1:06d}"
            else:
                self.numero_venta = "V-000001"

        # Calcular saldo pendiente
        self.saldo_pendiente = self.total - self.monto_abonado

        # Asegurar que el saldo pendiente no sea negativo
        if self.saldo_pendiente < 0:
            self.saldo_pendiente = 0

        # Actualizar estado automáticamente basado en saldo_pendiente
        # (excepto si está CANCELADO, ese estado no se modifica)
        if self.estado != 'CANCELADO':
            if self.saldo_pendiente <= 0:
                # Si no hay saldo pendiente, marcar como PAGADO
                self.estado = 'PAGADO'
                self.saldo_pendiente = 0
            elif self.monto_abonado > 0 and self.estado != 'PAGADO':
                # Si hay un abono parcial, marcar como ABONO
                self.estado = 'ABONO'
            elif self.monto_abonado == 0:
                # Sin abono = PENDIENTE
                self.estado = 'PENDIENTE'

        super().save(*args, **kwargs)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.venta.numero_venta} - {self.producto_variante}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
    ]
    
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.IntegerField()
    stock_anterior = models.IntegerField()
    stock_nuevo = models.IntegerField()
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto_variante} - {self.cantidad}"
    
    class Meta:
        ordering = ['-fecha_movimiento']

class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Proveedores"

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]

    TIPO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CREDITO', 'Crédito'),
    ]

    numero_compra = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_pago = models.CharField(max_length=15, choices=TIPO_PAGO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Compra {self.numero_compra} - {self.proveedor.nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_compra:
            # Generar número de compra automáticamente
            last_compra = Compra.objects.order_by('-id').first()
            if last_compra:
                last_number = int(last_compra.numero_compra.split('-')[1])
                self.numero_compra = f"C-{last_number + 1:06d}"
            else:
                self.numero_compra = "C-000001"
        super().save(*args, **kwargs)

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto_variante = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.compra.numero_compra} - {self.producto_variante}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

        # Actualizar stock del producto
        self.producto_variante.stock_actual += self.cantidad
        self.producto_variante.save()

        # Registrar movimiento de inventario
        MovimientoInventario.objects.create(
            producto_variante=self.producto_variante,
            tipo_movimiento='ENTRADA',
            cantidad=self.cantidad,
            stock_anterior=self.producto_variante.stock_actual - self.cantidad,
            stock_nuevo=self.producto_variante.stock_actual,
            motivo=f'Compra {self.compra.numero_compra}',
            usuario=self.compra.responsable
        )

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías de Gasto"

class Gasto(models.Model):
    TIPO_COMPROBANTE_CHOICES = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
        ('RECIBO', 'Recibo'),
        ('NINGUNO', 'Sin Comprobante'),
    ]

    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    tipo_comprobante = models.CharField(max_length=10, choices=TIPO_COMPROBANTE_CHOICES, default='NINGUNO')
    numero_comprobante = models.CharField(max_length=50, blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria.nombre} - {self.descripcion} - ${self.monto}"

    class Meta:
        ordering = ['-fecha']

class PagoVenta(models.Model):
    """Modelo para registrar el historial de pagos/abonos de una venta"""
    TIPO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('MIXTO', 'Mixto'),
    ]

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    tipo_pago = models.CharField(max_length=15, choices=TIPO_PAGO_CHOICES)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago {self.venta.numero_venta} - ${self.monto} - {self.fecha_pago.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = "Pago de Venta"
        verbose_name_plural = "Pagos de Ventas"

class PromocionWhatsApp(models.Model):
    """Modelo para gestionar promociones enviadas por WhatsApp"""
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIANDO', 'Enviando'),
        ('ENVIADO', 'Enviado'),
        ('ERROR', 'Error'),
    ]

    titulo = models.CharField(max_length=200, help_text="Título de la promoción (solo para referencia interna)")
    mensaje = models.TextField(help_text="Mensaje que se enviará. Usa {nombre} para personalizar")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora en que se envió la promoción")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    # Estadísticas de envío
    total_destinatarios = models.IntegerField(default=0)
    mensajes_enviados = models.IntegerField(default=0)
    mensajes_fallidos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.titulo} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Promoción WhatsApp"
        verbose_name_plural = "Promociones WhatsApp"

class EnvioWhatsApp(models.Model):
    """Modelo para registrar cada envío individual de WhatsApp"""
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADO', 'Enviado'),
        ('FALLIDO', 'Fallido'),
    ]

    promocion = models.ForeignKey(PromocionWhatsApp, on_delete=models.CASCADE, related_name='envios')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    mensaje_enviado = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_envio = models.DateTimeField(null=True, blank=True)
    mensaje_error = models.TextField(blank=True, null=True)
    sid_twilio = models.CharField(max_length=100, blank=True, null=True, help_text="ID del mensaje en Twilio")

    def __str__(self):
        return f"{self.promocion.titulo} -> {self.cliente.nombre_completo} ({self.estado})"

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = "Envío WhatsApp"
        verbose_name_plural = "Envíos WhatsApp"