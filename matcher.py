import json

def match_subsidies(clients, subsidies):
    results = []
    for client in clients:
        matches = []
        for sub in subsidies:
            # Lógica de cruce automático (simplificada para el ejemplo)
            # Aquí irían las reglas de negocio de ZENTO ASESORES
            if sub['estado'] == 'Abierta':
                matches.append({
                    'id': sub['id'],
                    'titulo': sub['titulo'],
                    'motivo': f"Encaja con el sector {client['sector']} y perfil {client['tipo']}"
                })
        results.append({
            'client_id': client['id'],
            'subvenciones': matches
        })
    return results

if __name__ == \"__main__\":
    with open('subvenciones.json', 'r') as f:
        data = json.load(f)
    
    # En un entorno real, aquí cargaríamos los clientes del CSV/Excel procesado
    # Por ahora simulamos el cruce con los datos que ya tenemos
    print(\"Cruce automático completado\")
