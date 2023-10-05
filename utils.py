import os

def disable_windows_notifications():
    try:
        # Run the Windows notification settings command
        os.system("powershell -Command 'Set-ItemProperty -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\PushNotifications -Name ToastEnabled -Value 0'")
    except Exception as e:
        print("An error occurred:", str(e))


def enable_windows_notifications():
    try:
        os.system("powershell -Command 'Set-ItemProperty -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\PushNotifications -Name ToastEnabled -Value 1'")
    except Exception as e:
        print("An error occurred:", str(e))