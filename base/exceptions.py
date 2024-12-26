from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def global_exception_handler(exc, context):
    """
    Custom global exception handler for DRF.
    """
    # Call the default DRF exception handler to get the standard error response
    response = exception_handler(exc, context)

    if response is None:
        response = Response(
            {
                "detail": str(exc),
                "error_type": type(exc).__name__,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response