from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from alm.models import Producto, Categoria, ProductoVariante, Marca

def lista_productos(request):
    """Vista para mostrar la página de productos"""
    return render(request, 'productos/lista.html')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_productos(request):
    """API para manejar productos"""
    if request.method == 'GET':
        productos = Producto.objects.select_related('categoria', 'marca').all()
        data = []
        for producto in productos:
            # Calcular stock total de todas las variantes
            stock_total = sum(variante.stock_actual for variante in producto.variantes.all())
            
            data.append({
                'id': producto.id,
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'categoria': producto.categoria.nombre,
                'marca': producto.marca.nombre,
                'precio_compra': str(producto.precio_compra),
                'precio_venta': str(producto.precio_venta),
                'stock': stock_total,
                'activo': producto.activo,
                'fecha_creacion': producto.fecha_creacion.isoformat(),
            })
        return JsonResponse({'productos': data})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            categoria = get_object_or_404(Categoria, id=data.get('categoria_id'))
            marca = get_object_or_404(Marca, id=data.get('marca_id'))
            
            # Crear producto con los campos correctos
            producto = Producto.objects.create(
                codigo=data['codigo'],
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                categoria=categoria,
                marca=marca,
                precio_compra=data['precio_compra'],
                precio_venta=data['precio_venta']
            )
            
            return JsonResponse({
                'success': True,
                'mensaje': 'Producto creado exitosamente',
                'producto': {
                    'id': producto.id,
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'precio_venta': str(producto.precio_venta),
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_producto_detalle(request, producto_id):
    """API para manejar producto individual"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'GET':
        stock_total = sum(variante.stock_actual for variante in producto.variantes.all())
        
        return JsonResponse({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'categoria': producto.categoria.nombre,
            'marca': producto.marca.nombre,
            'precio_compra': str(producto.precio_compra),
            'precio_venta': str(producto.precio_venta),
            'stock': stock_total,
            'activo': producto.activo,
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            producto.codigo = data.get('codigo', producto.codigo)
            producto.nombre = data.get('nombre', producto.nombre)
            producto.descripcion = data.get('descripcion', producto.descripcion)
            producto.precio_compra = data.get('precio_compra', producto.precio_compra)
            producto.precio_venta = data.get('precio_venta', producto.precio_venta)
            
            producto.save()
            
            return JsonResponse({
                'success': True,
                'mensaje': 'Producto actualizado exitosamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        producto.delete()
        return JsonResponse({
            'success': True,
            'mensaje': 'Producto eliminado exitosamente'
        })

def api_categorias(request):
    """API para obtener categorías"""
    categorias = Categoria.objects.all()
    data = [{'id': cat.id, 'nombre': cat.nombre} for cat in categorias]
    return JsonResponse({'categorias': data})