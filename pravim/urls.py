from django.contrib import admin
from django.urls import path, include
from usuarios.views import LoginInstitucionalView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginInstitucionalView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('fichas/', include(('fichas.urls', 'fichas'), namespace='fichas')),
]
