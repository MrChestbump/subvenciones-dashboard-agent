import json
from datetime import datetime

# Cargar datos
with open('clientes.json', 'r', encoding='utf-8') as f:
    clientes = json.load(f)

with open('subvenciones.json', 'r', encoding='utf-8') as f:
    subvenciones = json.load(f)

# Lógica de matching
def calcular_antiguedad_meses(fecha_alta):
    """Calcula la antigüedad en meses desde la fecha de alta"""
    fecha = datetime.strptime(fecha_alta, '%Y-%m-%d')
    hoy = datetime(2026, 3, 13)
    return (hoy.year - fecha.year) * 12 + hoy.month - fecha.month

def match_cliente_subvencion(cliente, subvencion):
    """Determina si un cliente encaja con una subvención y el nivel de aplicabilidad"""
    matches = []
    
    # TR341D - Promoción Autoempleo (Autónomos y sociedades < 3 años)
    if subvencion['codigo'] == 'TR341D':
        antiguedad_meses = calcular_antiguedad_meses(cliente['fecha_alta'])
        if antiguedad_meses < 36:  # Menos de 3 años
            estado = 'aplica'
            if cliente['tipo'] == 'FIS':
                cuantia = '7.500-12.000€'
                motivo = f"Alta {cliente['fecha_alta'][-7:]}. Menos de 3 años. Subvención inicio/cuotas SS."
            else:
                cuantia = 'Cuotas SS 1ª contrat.'
                motivo = f"Sociedad nueva {cliente['fecha_alta'][-7:]}. Primera contratación o inversión inicial."
            matches.append({'id': 'TR341D', 'estado': estado, 'cuantia': cuantia, 'motivo': motivo})
    
    # TR341Q - Inversión Modernización
    if subvencion['codigo'] == 'TR341Q':
        # Aplica a autónomos, especialmente CNAEs relacionados con comercio, hostelería, TIC
        cnaes_prioritarios = ['6201', '6202', '4719', '1071', '5610', '4520', '5320']
        if cliente['cnae'] in cnaes_prioritarios or cliente['tipo'] == 'FIS':
            estado = 'aplica'
            if cliente['cnae'].startswith('62'):  # TIC
                motivo = 'Si invierte en TIC o software.'
            elif cliente['cnae'].startswith('47') or cliente['cnae'].startswith('56'):
                motivo = 'Inversión digitalización comercio, e-commerce, TPV.'
            elif cliente['cnae'].startswith('107') or cliente['cnae'].startswith('56'):
                motivo = 'Inversión maquinaria panadería o equipamiento hostelería.'
            elif cliente['cnae'] in ['4520', '5320']:
                motivo = 'Inversión vehículos mensajería o TIC comercio.'
            else:
                motivo = 'Inversión en activos productivos, maquinaria o digitalización.'
            matches.append({'id': 'TR341Q', 'estado': estado, 'cuantia': 'Hasta 7.000 60%', 'motivo': motivo})
    
    # TR341R - Conciliación (si tiene empleados o puede contratar)
    if subvencion['codigo'] == 'TR341R':
        if cliente['empleados'] > 0 or cliente['ingresos'] > 100000:
            estado = 'aplica' if cliente['empleados'] >= 2 else 'posible'
            matches.append({'id': 'TR341R', 'estado': estado, 'cuantia': 'Salario sustituto', 
                          'motivo': 'Si contrata sustituto para conciliación.'})
    
    # TR880A - Emprendimiento Reciente (< 2 años)
    if subvencion['codigo'] == 'TR880A':
        antiguedad_meses = calcular_antiguedad_meses(cliente['fecha_alta'])
        if antiguedad_meses < 24 and cliente['tipo'] == 'FIS':
            matches.append({'id': 'TR880A', 'estado': 'aplica', 'cuantia': 'Hasta 12.000€',
                          'motivo': 'Emprendimiento reciente. Programa específico nuevos autónomos.'})
    
    # TR340E - IEBT Base Tecnológica
    if subvencion['codigo'] == 'TR340E':
        cnaes_tecnologicos = ['6201', '6202', '6209', '6311', '6312', '7311', '7220', '3511']
        if cliente['cnae'] in cnaes_tecnologicos:
            estado = 'aplica' if cliente['tipo'] == 'SOC' else 'posible'
            matches.append({'id': 'TR340E', 'estado': estado, 'cuantia': 'Variable',
                          'motivo': 'Si acredita base tecnológica.' if estado == 'posible' else 'Base tecnológica acreditada. I+D+i'})
    
    # PEL - Empleo Diputación A Coruña (municipios < 20k habitantes prioritarios)
    if subvencion['codigo'] == 'PEL':
        municipios_prioritarios = ['Narón', 'Sada', 'Arteixo', 'Oleiros', 'Culleredo', 'Cambre']
        if cliente['domicilio'] in municipios_prioritarios:
            estado = 'aplica'
            cuantia = 'Hasta 12.000€' if cliente['domicilio'] in ['Narón', 'Sada'] else 'Hasta 10.000€'
            motivo = f"{cliente['domicilio']}. Contratación indefinida 2026."
        elif cliente['empleados'] > 0 or cliente['ingresos'] > 80000:
            estado = 'posible'
            cuantia = 'Hasta 10.000€'
            motivo = 'Si contrata indefinido con incremento empleo neto.'
        else:
            estado = None
        
        if estado:
            matches.append({'id': 'PEL', 'estado': estado, 'cuantia': cuantia, 'motivo': motivo})
    
    # KIT DIGITAL - Seg III
    if subvencion['codigo'] == 'KITDIGITAL':
        cnaes_digitales = ['6201', '6202', '4719', '8559', '5610', '7311', '6920']
        if cliente['cnae'] in cnaes_digitales or (cliente['empleados'] < 10 and cliente['tipo'] == 'SOC'):
            estado = 'aplica'
            if cliente['cnae'].startswith('62'):
                motivo = f"CNAE {cliente['cnae']} IT. CRM, ciberseguridad, web."
            elif cliente['cnae'] == '8559':
                motivo = 'Aula virtual, gestión alumnos, LMS.'
            elif cliente['cnae'].startswith('47') or cliente['cnae'].startswith('56'):
                motivo = 'E-commerce, SEO, gestión comercial.'
            else:
                motivo = 'Digitalización PYME. Web, CRM, factura electrónica.'
            matches.append({'id': 'KITDIGITAL', 'estado': 'aplica' if cliente['empleados'] < 10 else 'posible', 
                          'cuantia': 'Hasta 12.000€', 'motivo': motivo})
    
    return matches

# Realizar matching para todos los clientes
resultados = []
for cliente in clientes:
    subvenciones_cliente = []
    for subvencion in subvenciones:
        matches = match_cliente_subvencion(cliente, subvencion)
        subvenciones_cliente.extend(matches)
    
    # Solo incluir clientes con al menos una subvención aplicable
    if subvenciones_cliente:
        # Determinar tags
        tags = []
        if cliente['tipo'] == 'FIS':
            tags.append('autonomo')
        else:
            tags.append('sociedad')
        
        # Agregar tags por tipo de subvención
        codigos = [s['id'] for s in subvenciones_cliente]
        if any(c.startswith('TR3') or c == 'TR880A' for c in codigos):
            tags.append('xunta')
        if 'PEL' in codigos:
            tags.append('pel')
        if 'KITDIGITAL' in codigos:
            tags.append('kit')
        
        # Preparar nota descriptiva
        if cliente['tipo'] == 'FIS':
            nota = f"Alta {cliente['fecha_alta'][-7:]}"
            if cliente['ingresos'] > 100000:
                nota += f". Ingresos {cliente['ingresos']//1000}k"
        else:
            nota = f"Alta {cliente['fecha_alta'][-7:]}"
        
        # Crear entrada del cliente con formato del dashboard
        resultado = {
            'nif': cliente['nif'],
            'nombre': cliente['nombre'],
            'tipo': 'autonomo' if cliente['tipo'] == 'FIS' else 'sociedad',
            'cnae': cliente['cnae'],
            'domicilio': cliente['domicilio'],
            'tags': tags,
            'nota': nota,
            'subvenciones': subvenciones_cliente
        }
        resultados.append(resultado)

# Guardar resultados
with open('clientes_matched.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"Matching completado: {len(resultados)} clientes con subvenciones aplicables de {len(clientes)} totales")
print(f"Archivo 'clientes_matched.json' generado correctamente")
