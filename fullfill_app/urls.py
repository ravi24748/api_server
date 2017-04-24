from django.conf.urls import url
from.import views


urlpatterns = [
    url(r'^request/', views.ThreadTimeout.as_view()),
    url(r'^serverStatus/', views.ThreadStatus.as_view()),
    url(r'^kill/', views.ThreadKill.as_view())


]