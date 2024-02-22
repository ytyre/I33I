"""
URL configuration for I33I project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from berserk.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy


urlpatterns = [
    path('', ber, name='ber'),
    path('I33I/', i33iX),
    path('I33I/login/', MyLoginView.as_view(), name='login'),
    path('I33I/sing_in/', registreted, name='sing_in'),
    path('accounts/logout', brLogOut.as_view(), name='logout'),
    path('I33I/create_record/', Create_view, name='create_record'),
    path('I33I/accounts/profile/', account, name='account'),
    path('I33I/admin/', admin.site.urls),
    path('I33I/create_comment/<int:post_id>/', CreateComment, name='comment'),
    path('I33I/record/<int:post_id>/', specific_entry, name='specific_entry'),
    path('I33I/record/<int:post_id>/like', CreateLike, name='CreateLike'),
    path('I33I/record/<int:post_id>/dislike', CreateDislike, name='CreateDislike'),
    path('I33I/accounts/profile/extrainformation', CreateExtraInformation, name='CreateExtraInformation'),
    path('I33I/accounts/profile/Mynotes', MyNotes, name='MyNotes'),
    path('I33I/accounts/profile/Mynotes/<int:pk>', BrDeleteRecord.as_view(), name='BrDeleteRecord'),
    path('I33I/login/reset_password', PasswordResetRecord.as_view(), name='PasswordResetRecord'),
    path('I33I/login/reset_password/<uidb64>/<token>/', PasswordReset.as_view(), name='PasswordReset'),
    path('I33I/record/searchrecord', SearchForRecords, name='SearchForRecords'),
    path('I33I/accounts/profile/change_password/', PasswordChangeView.as_view(), name='PasswordChangeView'),
    path('I33I/accounts/profile/change_password/done', PasswordChangeDoneView.as_view(), name='PasswordChangeDoneView'),
    path('I33I/image/', DefaultImage, name='DefaultImage' ),
    path('I33I/accounts/profile/<int:user_id>/', UserInformations, name='UserInformations'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)