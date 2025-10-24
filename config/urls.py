"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def root_health_check(request):
    """Root health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'AI Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'chatbot_api': '/api/chatbot/',
            'users_api': '/api/users/',
            'analytics_api': '/api/analytics/',
        }
    })


urlpatterns = [
    # Root endpoint
    path('', root_health_check, name='root'),

    # Django admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/chatbot/', include('apps.chatbot.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
