from django.urls import path
from .views import (
    AssetList, AssetCreate, AssetDetail, AssetUpdate,
    AssetTypeList, AssetTypeCreate, AssetTypeDetail, AssetTypeUpdate,
    AssetImageRemove, AssetImageUploadView, AssetCSVView
)
from .ajax_datatable_views import AssetAjaxDatatableView, AssetTypeAjaxDatatableView

app_name = 'assets'

urlpatterns = [
    path('assets/', AssetList.as_view(), name='asset_list'),
    path('assets/create/', AssetCreate.as_view(), name='asset_create'),
    path('assets/<int:pk>/', AssetDetail.as_view(), name='asset_detail'),
    path('assets/<int:pk>/update/', AssetUpdate.as_view(), name='asset_update'),

    path('asset_types/', AssetTypeList.as_view(), name='asset_type_list'),
    path('asset_types/create/', AssetTypeCreate.as_view(),
         name='asset_type_create'),
    path('asset_types/<int:pk>/', AssetTypeDetail.as_view(),
         name='asset_type_detail'),
    path('asset_types/<int:pk>/update/',
         AssetTypeUpdate.as_view(), name='asset_type_update'),
         
    path('assetimage/', AssetImageRemove.as_view(), name='asset_image_remove'),
    path('asset_image_update/', AssetImageUploadView.as_view(),
         name='asset_image_update'),

    path('ajax_datatable/assets/', AssetAjaxDatatableView.as_view(),
         name="ajax_datatable_assets"),
    path('ajax_datatable/asset_types/', AssetTypeAjaxDatatableView.as_view(),
         name="ajax_datatable_asset_types"),

    path('download_assets', AssetCSVView.as_view(),
         name="generate_csv"),

]
