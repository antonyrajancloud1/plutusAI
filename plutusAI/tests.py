from django.views.decorators.http import require_http_methods

from .server.manualOrder import *
import subprocess

# Create your tests here.
@require_http_methods([GET])
def tester(request):
    return restart_celery()



def is_celery_running():
    app_name = "plutus.celery"
    try:
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()

        for line in lines:
            if 'celery' in line and app_name in line:
                return True
        return False
    except Exception as e:
        print(f"Error checking Celery status: {e}")
        return False
def check_celery_status(request):
    try:

        if is_celery_running():
            return JsonResponse({"celery_running": True, "details": "Celery is running."})
        else:
            return JsonResponse({"celery_running": False, "details": "Celery is NOT running."})
    except Exception as e:
        return JsonResponse({"celery_running": False, "error": str(e)}, status=500)

def stop_celery():
    try:
        print(is_celery_running())
        if is_celery_running():
            subprocess.run(["pkill", "-f", "celery -A plutus.celery"], check=True)
            return {"success": True, "message": "Celery stopped successfully."}
        else:
            return {"success": False, "message": "Celery is not running."}
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": f"Failed to stop Celery: {e}"}

def restart_celery():
    if is_celery_running():
        stop_result = stop_celery()
        if not stop_result["success"]:
            return JsonResponse({"success": False, "message": "Failed to stop Celery. Restart aborted."})

        time.sleep(2)

    try:
        command = "celery -A plutus.celery worker --loglevel=info --autoscale=100,3"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return JsonResponse({"success": True, "message": "Celery restarted successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Failed to restart Celery: {e}"})
