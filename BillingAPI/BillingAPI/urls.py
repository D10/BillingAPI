from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf.urls import handler500, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('billing_app.urls'))
]


def response_404(request, status=404, message=False, data=None):
    message = {'response': message}
    return JsonResponse(message)


def response_500(request, status=500, message=False, data=None):
    message = {'error': message}
    return JsonResponse(message)


handler404 = response_404
handler500 = response_500
