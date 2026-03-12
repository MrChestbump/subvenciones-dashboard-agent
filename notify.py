import os
import json
import requests

def send_slack_notification(message):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("SLACK_WEBHOOK_URL no configurada.")
        return
    
    payload = {"text": message}
    try:
        requests.post(webhook_url, json=payload)
        print("Notificación de Slack enviada.")
    except Exception as e:
        print(f"Error enviando a Slack: {e}")

def main():
    if not os.path.exists('subvenciones.json'):
        return
        
    with open('subvenciones.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    subvenciones = data.get('subvenciones', [])
    if not subvenciones:
        return
        
    # Crear mensaje resumen
    msg = f"🔔 *Nuevas Subvenciones Encontradas ({data['fecha_actualizacion'][:10]})*

"
    for s in subvenciones[:5]:  # Mostrar las 5 primeras
        msg += f"• *{s['titulo']}*
  Organismo: {s['organismo']} | <{s['url']}|Ver más>

"
        
    if len(subvenciones) > 5:
        msg += f"_...y {len(subvenciones)-5} más en el dashboard._"
        
    send_slack_notification(msg)

if __name__ == "__main__":
    main()
