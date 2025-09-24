from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog.views import UserRegistrationView
from pages.views import page_not_found, server_error, csrf_failure

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/registration/', UserRegistrationView.as_view(),
         name='auth/registration'),
    path('auth/', include('django.contrib.auth.urls')),
]

# Добавляем обработку медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler403 = csrf_failure
handler404 = page_not_found
handler500 = server_error
