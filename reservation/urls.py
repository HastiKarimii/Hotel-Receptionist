from django.urls import path
from .views import ReservationDeleteView, ReservationListView, ReservationUpdateView, ReservationCreateView


urlpatterns = [

    path('reserve/create/', ReservationCreateView.as_view(), name="createreserve"),
    path('reserve/edit/<int:pk>/', ReservationUpdateView.as_view(), name='editreserve'),
    path('reserve/list/', ReservationListView.as_view(), name='listreserve'),
    path('delete/<int:pk>', ReservationDeleteView.as_view(), name = 'deletereserve'),

    ]
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



