import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Return safe, consistent API errors without exposing internals."""

    response = exception_handler(exc, context)
    view = context.get('view')

    if response is not None:
        response.data = {
            'success': False,
            'message': 'Request failed.',
            'errors': response.data,
        }
        return response

    logger.exception('Unhandled API error in %s', view.__class__.__name__ if view else 'unknown view')
    return Response(
        {
            'success': False,
            'message': 'Internal server error.',
            'errors': 'Please contact support if the problem continues.',
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

