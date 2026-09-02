"""
Notification Service

Handles SMS and WhatsApp notifications.
"""

from typing import Tuple
from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class NotificationService:
    """
    Notification service for SMS and WhatsApp.

    Supports:
        - Native Android SMS/WhatsApp
        - Twilio integration
    """

    @staticmethod
    def send_sms(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send SMS notification.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            if not phone:
                return False, "Phone number required"

            if Config.SMS_PROVIDER == "twilio":
                return NotificationService._send_sms_twilio(phone, message)
            else:
                return NotificationService._send_sms_native(phone, message)
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return False, "Failed to send SMS"

    @staticmethod
    def send_whatsapp(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send WhatsApp notification.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            if not phone:
                return False, "Phone number required"

            if Config.SMS_PROVIDER == "twilio":
                return NotificationService._send_whatsapp_twilio(phone, message)
            else:
                return NotificationService._send_whatsapp_native(phone, message)
        except Exception as e:
            logger.error(f"Failed to send WhatsApp: {e}")
            return False, "Failed to send WhatsApp"

    @staticmethod
    def _send_sms_native(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send SMS using native Android.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            from kivy.utils import platform

            if platform == "android":
                from jnius import autoclass

                Uri = autoclass("android.net.Uri")
                Intent = autoclass("android.content.Intent")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                uri = Uri.parse(f"smsto:{phone}")
                intent = Intent(Intent.ACTION_SENDTO, uri)
                intent.putExtra("sms_body", message)
                PythonActivity.mActivity.startActivity(intent)
                logger.info(f"SMS sent via native: {phone}")
                return True, "SMS app opened"
            else:
                logger.info(f"Simulated SMS to {phone}: {message[:50]}...")
                return True, "Simulated SMS"
        except Exception as e:
            logger.error(f"Native SMS failed: {e}")
            return False, "Failed to send SMS"

    @staticmethod
    def _send_whatsapp_native(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send WhatsApp using native Android.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            from kivy.utils import platform

            if platform == "android":
                from jnius import autoclass

                Uri = autoclass("android.net.Uri")
                Intent = autoclass("android.content.Intent")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                # Clean phone number
                clean_phone = phone.replace("+", "").replace(" ", "")
                if len(clean_phone) == 10:
                    clean_phone = "91" + clean_phone

                uri = Uri.parse(f"whatsapp://send?phone={clean_phone}&text={message}")
                intent = Intent(Intent.ACTION_VIEW, uri)
                PythonActivity.mActivity.startActivity(intent)
                logger.info(f"WhatsApp sent via native: {phone}")
                return True, "WhatsApp app opened"
            else:
                logger.info(f"Simulated WhatsApp to {phone}: {message[:50]}...")
                return True, "Simulated WhatsApp"
        except Exception as e:
            logger.error(f"Native WhatsApp failed: {e}")
            return False, "Failed to send WhatsApp"

    @staticmethod
    def _send_sms_twilio(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send SMS using Twilio.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            from twilio.rest import Client

            client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            sms = client.messages.create(
                body=message,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=phone,
            )
            logger.info(f"SMS sent via Twilio: {phone} - SID: {sms.sid}")
            return True, "SMS sent successfully"
        except Exception as e:
            logger.error(f"Twilio SMS failed: {e}")
            return False, "Failed to send SMS"

    @staticmethod
    def _send_whatsapp_twilio(phone: str, message: str) -> Tuple[bool, str]:
        """
        Send WhatsApp using Twilio.

        Args:
            phone: Phone number
            message: Message content

        Returns:
            Tuple of (success, message)
        """
        try:
            from twilio.rest import Client

            client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            msg = client.messages.create(
                body=message,
                from_=f"whatsapp:{Config.TWILIO_PHONE_NUMBER}",
                to=f"whatsapp:{phone}",
            )
            logger.info(f"WhatsApp sent via Twilio: {phone} - SID: {msg.sid}")
            return True, "WhatsApp sent successfully"
        except Exception as e:
            logger.error(f"Twilio WhatsApp failed: {e}")
            return False, "Failed to send WhatsApp"
