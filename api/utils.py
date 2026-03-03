def success_response(data, message="Success"):
    """Standard success response format"""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message, errors=None):
    """Standard error response format"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return response

