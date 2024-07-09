from ajax_datatable.views import AjaxDatatableView
from .models import Asset, AssetType


class AssetAjaxDatatableView(AjaxDatatableView):
    model = Asset
    title = 'Asset'
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, 'title': 'id',},
        {'name': 'name', 'visible': True, 'title': "Name", },
        {'name': 'code', 'visible': True, 'title': 'Code'},
        {'name': 'asset_type', 'visible': True, 'title': 'Asset Type', "foreign_field": "asset_type__name"},
        {'name': 'status', 'visible': True, 'title': 'Status'},
        {'name': 'created_at', 'visible': True, 'title': 'Created At'},
        {'name': 'updated_at', 'visible': True, 'title': 'Updated At'},
        {'name': 'edit', 'title': 'Edit', 'placeholder': True, 'searchable': False, 'orderable': False, },
    ]


    def customize_row(self, row, obj):
        row['edit'] = f"""
            <a href="/assets/{obj.id}/" class="btn btn-success btn-sm">
               Show
            </a>
            <a href="/assets/{obj.id}/update" class="btn btn-primary btn-sm">
               Edit
            </a>
        """    
    

class AssetTypeAjaxDatatableView(AjaxDatatableView):
    model = AssetType
    title = 'AssetType'
    search_values_separator = '+'
    

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, 'title': 'id',},
        {'name': 'name', 'visible': True, 'title': "Name",},
        {'name': 'created_at', 'visible': True, 'title': 'Created At'},
        {'name': 'updated_at', 'visible': True, 'title': 'Updated At'},
        {'name': 'edit', 'title': 'Edit', 'placeholder': True, 'searchable': False, 'orderable': False, },
    ]

    def customize_row(self, row, obj):
        row['edit'] = f"""
            <a href="/asset_types/{obj.id}/" class="btn btn-success btn-sm">
               Show
            </a>
            <a href="/asset_types/{obj.id}/update" class="btn btn-primary btn-sm">
               Edit
            </a>
        """


