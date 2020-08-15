from django.conf.urls import url
from .test_functions import test_mail, test_getenviron, test_printdata

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include # url

from members.views import (
    RegistrationView,
    LoginView,
    RequestResetLinkView,
    CompletePasswordChangeView,
    RequestActivationCode,
    MySettingsView,
    edit_myprofile,
    activate,
)

from customers.views import (
    mycustomers,
    create_customer,
    edit_customer,
    delete_customer,
)

from listings.views import (
    upload_brochure,
    upload_certificate,
    upload_eproof,
    upload_manual,
    upload_powerpoint,
    upload_proposal,
    edit_document,
    alldocuments,
    selecteddocument,
    alldocumentsbytype,
    search,
    mydocuments,
    mydocumentsOverview,
    mydocumentstaskList,
    mydocumentstaskDetail,
    mydocumentstaskCreate,
    mydocumentstaskUpdate,
    mydocumentstaskDelete

)


from .views import (
    index,
    gallery,
    blank,
)

urlpatterns = [

    path('gallery/', gallery, name="gallery"),

    path('mydocuments-api/', mydocumentsOverview),
    path('mydocuments/', mydocuments, name ='mydocuments'),
    path('mydocuments/task-list/', mydocumentstaskList),   #json return which is used by javascript
    path('mydocuments/task-detail/<str:pk>/', mydocumentstaskDetail),
    path('mydocuments/task-create/', mydocumentstaskCreate),
    path('mydocuments/task-update/<str:pk>/', mydocumentstaskUpdate),
    path('mydocuments/task-delete/<str:pk>/', mydocumentstaskDelete),

    #function is located is at listings.views
    path('upload-brochure/', upload_brochure, name ='upload_brochure'),
    path('upload-certificate/', upload_certificate, name ='upload_certificate'),
    path('upload_eproof/', upload_eproof, name ='upload_eproof'),
    path('upload-manual/', upload_manual, name ='upload_manual'),
    path('upload-proposal/', upload_proposal, name ='upload_proposal'),
    path('upload-powerpoint/', upload_powerpoint, name ='upload_powerpoint'),

    path('mydocuments/edit/<int:listing_id>', edit_document, name='edit_document'),

    path('alldocuments/', alldocuments, name='alldocuments'),
    path('alldocuments/search', search, name='search'),
    path('selecteddocument/<int:listing_id>', selecteddocument, name='selecteddocument'),
    path('alldocuments/<product_type>', alldocumentsbytype, name='selectedtypedocuments'),

    #function is located is at members.views
    path('myprofile/', edit_myprofile, name='myprofile'),

    path('mysettings/', MySettingsView.as_view(), name='mysettings'),

    path('signup/', RegistrationView.as_view(), name='signup'),
    path('members/login/', LoginView.as_view(), name='login'),
    path('request-reset/', RequestResetLinkView.as_view(), name='reset-password'),
    path('change-password/<uidb64>/<token>', CompletePasswordChangeView.as_view(), name='change-password'),
    path('requestactivatecode/', RequestActivationCode.as_view(), name='requestcode'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

    #function is located is at customers.views
    path('mycustomers/', mycustomers, name ='mycustomers'),
    path('mycustomers/create', create_customer, name='create_customer'),
    path('mycustomers/edit/<int:customer_id>', edit_customer, name='edit_customer'),
    path('mycustomers/delete/<int:customer_id>', delete_customer, name='delete_customer'),

## homepage (prior to successful login) ##
    path('', index, name='home'),
    path('blank/', blank, name ='blank'),
    path('t1/', test_mail),                #test sending email
    path('t2/', test_getenviron),
    path('t3/', test_printdata),


    path('admin/', admin.site.urls),
    path('members/', include('django.contrib.auth.urls')),
]

#if at development phase, all static and media file are stored at local PC drive
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #find STATIC_URL as described in settings and use the path  STATIC_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






