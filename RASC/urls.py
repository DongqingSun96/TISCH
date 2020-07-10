"""RASC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import *
from django.urls import path
from RASC import view, settings
from django.views.static import serve

urlpatterns = [
    path('', view.home),
    path('home/', view.home),
    path('data/<str:dataset>', view.data, name = "data"),
    # path('search-cancer/', view.search_cancer),
    path('search-gene/', view.search_gene),
    path('gallery/', view.select_dataset),
    path('documentation/', view.doc),
    path('statistics/', view.statistics),
    # path('run-lisa/', view.run_lisa),
    # path('run-success/', view.run_success),
    # path('run-result/', view.run_result),
    # path('link-dataset/<str:dataset>', view.link_dataset, name = "link_dataset"),
    # path('images/tSNE/<str:path>', serve, {'document_root': '/data/home/chenfei/public_html/RASC/images/tSNE/'}),
    path('download/<str:path>', serve, {'document_root': settings.MEDIA_ROOT + "download/"}),
    path('media/tmp/<str:path>', serve, {'document_root': settings.MEDIA_ROOT + "tmp/"}),
    # path('scRNA/Data/<str:path>', serve, {'document_root': '/Users/dongqing/Documents/Project/SingleCell/scRNA/Data/'})
]
