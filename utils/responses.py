def success_response(data, message="OK"):
    return {"success": True,
            "data": data,
            "message": message,
            "error": None}

def error_response(message, error=None):
    return {"success": False,
            "data": None,
            "message": message,
            "error": error}