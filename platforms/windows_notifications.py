from __future__ import annotations

def notify(title: str, message: str) -> bool:
    try:
        from winotify import Notification

        toast = Notification(
            app_id="Wi-Fi Security Tray",
            title=title,
            msg=message,
            duration="short",
        )
        toast.show()
        return True
    except Exception:
        # Notification failure should never stop monitoring.
        return False
