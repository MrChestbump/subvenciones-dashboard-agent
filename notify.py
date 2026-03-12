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
        print("Notificacion de Slack enviada.")
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
    fecha = data.get('fecha_actualizacion', '')[:10]
    total = len(subvenciones)
    msg = f"[SUBVENCIONES] Nuevas subvenciones encontradas ({fecha})\n"
    msg += f"Total convocatorias: {total}\n"
    for s in subvenciones[:5]:
        titulo = s.get('titulo', s.get('title', 'Sin titulo'))
        msg += f"- {titulo}\n"
    if total > 5:
        msg += f"... y {total - 5} mas."

    send_slack_notification(msg)

if __name__ == '__main__':
    main()
