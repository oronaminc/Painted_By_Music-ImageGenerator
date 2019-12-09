from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^run/$', views.run, name='run'),
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
    url(r'^make1/$', views.make1, name="make1"),
    url(r'^make2/$', views.make2, name="make2"),
    url(r'^make3/$', views.make3, name="make3"),
    url(r'^make4/$', views.make4, name="make4"),
    url(r'^make5/$', views.make5, name="make5"),
]
