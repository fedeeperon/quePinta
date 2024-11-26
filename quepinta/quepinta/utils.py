from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import os

def enviar_correo(subject, message, recipient_list):
    """
    Función para enviar un correo electrónico usando la configuración de Django.
    """
    try:
        send_mail(
            subject,          # Asunto del correo
            message,          # Cuerpo del correo
            settings.EMAIL_HOST_USER,  # Remitente (configurado en settings.py)
            recipient_list    # Lista de destinatarios
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
    
def test_email(request):
    try:
        subject = "Prueba de correo"
        message = "Este es un correo de prueba."
        recipient_list = ["tuemail@gmail.com"]  # Cambia por tu correo
        send_mail(subject, message, "tuemail@gmail.com", recipient_list)
        return HttpResponse("Correo enviado exitosamente.")
    except Exception as e:
        return HttpResponse(f"Error al enviar correo: {e}")

    print("EMAIL_HOST_USER:", os.getenv("EMAIL_HOST_USER"))
    print("EMAIL_HOST_PASSWORD:", os.getenv("EMAIL_HOST_PASSWORD"))
    print("DEFAULT_FROM_EMAIL:", os.getenv("DEFAULT_FROM_EMAIL"))
