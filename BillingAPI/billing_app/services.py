from rest_framework.response import Response


def response_exception():
    return Response({'success': False})
