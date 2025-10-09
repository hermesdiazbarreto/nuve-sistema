-- Script SQL para corregir ventas mal registradas
-- Problema: Ventas con descuento marcadas como ABONO cuando están completamente pagadas

-- Ver las ventas con problemas (ABONO pero monto_abonado >= total)
SELECT
    id,
    numero_venta,
    estado,
    total,
    descuento,
    monto_abonado,
    saldo_pendiente,
    fecha_venta
FROM alm_venta
WHERE estado = 'ABONO'
  AND monto_abonado >= total;

-- Corregir las ventas problemáticas
UPDATE alm_venta
SET
    estado = 'PAGADO',
    saldo_pendiente = 0.00,
    monto_abonado = total
WHERE estado = 'ABONO'
  AND monto_abonado >= total;

-- Verificar que se corrigieron
SELECT
    id,
    numero_venta,
    estado,
    total,
    descuento,
    monto_abonado,
    saldo_pendiente,
    fecha_venta
FROM alm_venta
WHERE numero_venta IN (
    SELECT numero_venta
    FROM alm_venta
    WHERE estado = 'PAGADO'
      AND descuento > 0
)
ORDER BY fecha_venta DESC
LIMIT 10;
