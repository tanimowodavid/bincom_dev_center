from django.shortcuts import get_object_or_404, redirect, render

from .forms import MediaForm
from .models import Media


def media_list(request):
    media_list = Media.objects.order_by('-uploaded_at')
    return render(request, 'base/home.html', {'media_list': media_list})


def media_detail(request, pk):
    media = get_object_or_404(Media, pk=pk)
    return render(request, 'base/media_detail.html', {'media': media})


def media_upload(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_item = form.save()
            return redirect('base:detail', pk=media_item.pk)
    else:
        form = MediaForm()

    return render(request, 'base/upload.html', {'form': form})
