from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Asset, AssetType, AssetImage
from .forms import AssetCreateForm, AssetForm, AssetImageForm
from django.contrib import messages
from django.views.generic.edit import FormMixin
import csv
from django.http import HttpResponse


class AssetList(LoginRequiredMixin, ListView):
    '''
    List all assets
    '''
    template_name = 'assets/list.html'
    model = Asset


class AssetCreate(LoginRequiredMixin, FormMixin, View):
    '''
    Create new asset
    '''
    template_name = 'assets/add.html'
    model = Asset
    fields = ['name', 'asset_type', 'status', 'images']
    success_url = reverse_lazy('asset_list')
    form_class = AssetCreateForm

    def get(self, request):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                if image.size > 1024 * 1024 * 2:
                    form.add_error('images', 'Image size should not exceed 2MB')
                    return self.form_invalid(form)
                asset_image = AssetImage(asset=self.object, image=image)
                asset_image.save()
            messages.success(request, 'Asset created successfully')
            return redirect(self.get_success_url())
        return self.form_invalid(form)
    
    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request, form.errors)
        return render(self.request, self.template_name, {'form': form})


class AssetDetail(LoginRequiredMixin, View):
    template_name = 'assets/show.html'
    model = Asset 
    success_url = reverse_lazy('asset_list')

    def get(self, request, pk):
        asset = Asset.objects.get(pk=pk)
        return render(request, self.template_name, {'object': asset})
    
    def post(self, request, pk):
        asset = Asset.objects.get(pk=pk)
        asset.delete()
        return JsonResponse({'message': 'Asset deleted successfully'}, status=200)


class AssetUpdate(LoginRequiredMixin, View, FormMixin):
    template_name = 'assets/edit.html'
    model = Asset
    fields = ['name', 'asset_type', 'status']
    success_url = reverse_lazy('asset_list')
    form_class = AssetForm

    def get(self, request, pk):
        asset = Asset.objects.get(pk=pk)
        form = AssetForm(instance=asset)
        asset_image_form = AssetImageForm()
        return render(request, self.template_name, {'form': form, 'object': asset, "asset_image_form": asset_image_form})
    
    def post(self, request, pk):
        asset = Asset.objects.get(pk=pk)
        form = AssetForm(instance=asset, data=request.POST)
        if form.is_valid():
            self.object = form.save()            
            messages.success(request, 'Asset updated successfully')
            return redirect(self.success_url)
        return self.form_invalid(form)
    
    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request, form.errors)
        return render(self.request, self.template_name, {'form': form, 'object': self.object})


class AssetTypeList(LoginRequiredMixin, ListView):
    template_name = 'asset_type/list.html'
    model = AssetType


class AssetTypeCreate(LoginRequiredMixin, CreateView):
    template_name = 'asset_type/add.html'
    model = AssetType
    fields = ['name', 'description']
    success_url = reverse_lazy('asset_type_list')


class AssetTypeDetail(LoginRequiredMixin, View):
    template_name = 'asset_type/show.html'
    model = AssetType
    success_url = reverse_lazy('asset_type_list')

    def get(self, request, pk):
        asset_type = AssetType.objects.get(pk=pk)
        return render(request, self.template_name, {'object': asset_type})
    
    def post(self, request, pk):
        asset_type = AssetType.objects.get(pk=pk)
        asset_type.delete()
        return JsonResponse({'message': 'Asset Type deleted successfully'}, status=200)


class AssetTypeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'asset_type/edit.html'
    model = AssetType
    fields = ['name', 'description']


class AssetImageRemove(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('imageId')
        if pk:
            asset_image = AssetImage.objects.get(pk=pk) 
            if asset_image.asset.images.count() > 1:
                asset_image.delete()                     
                return JsonResponse({'message': 'Asset Image deleted successfully'}, status=200)
            return JsonResponse({'message': 'At least one image is required'}, status=400)
        return JsonResponse({'message': 'Invalid request'}, status=400)


class AssetImageUploadView(LoginRequiredMixin, View):
    def post(self, request): 
        pk = request.POST.get('assetId')
        asset = Asset.objects.get(pk=pk)
        images = request.FILES.getlist('image')
        for image in images:
            if image.size > 1024 * 1024 * 2:
                return JsonResponse({'message': 'Image size should not exceed 2MB'}, status=400)
            asset_image = AssetImage(asset=asset, image=image)
            asset_image.save()
        return JsonResponse({'message': 'Asset Image uploaded successfully'}, status=200)


class AssetCSVView(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="assets.csv"'

        writer = csv.writer(response)
        writer.writerow(['Code', 'Name', 'Status', 'Asset Type'])

        assets = Asset.objects.all()
        for asset in assets:
            writer.writerow([asset.code, asset.name, asset.status, asset.asset_type.name])

        return response
