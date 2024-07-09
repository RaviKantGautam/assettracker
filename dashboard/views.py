from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from assets.models import Asset
from django.db.models import Count, Q


class Dashboard(LoginRequiredMixin, TemplateView):
    '''
    Display the dashboard page
    '''
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''        
        Get the context data for the dashboard page
        '''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'

        # Get the total number of assets
        context['assets_status'] = Asset.objects.aggregate(
            active_count=Count('id', filter=Q(status=True)),
            inactive_count=Count('id', filter=Q(status=False))
        )

        # Get the total number of assets by type
        _asset = Asset.objects.values(
            'asset_type__name').annotate(count=Count('id'))
        
        # Create a dictionary of asset types and their counts
        context['asset_type_analytic'] = {key: val for key, val in zip(
            [i['asset_type__name'] for i in _asset], [i['count'] for i in _asset])}
        return context
