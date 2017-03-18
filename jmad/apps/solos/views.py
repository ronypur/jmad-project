from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Solo


def solo_detail(request, album, track, artist):
    context = {
        'solo': Solo.objects.get(slug=artist, track__slug=track, track__album__slug=album)
    }
    return render(request, 'solos/solo_detail.html', context)


def index(request):
    context = {'solos': []}

    if request.GET.keys():
        solos_queryset = Solo.objects.all()

        if request.GET.get('instrument', None):
            solos_queryset = solos_queryset.filter(
                instrument=request.GET.get('instrument', None)
            )

        if request.GET.get('artist', None):
            solos_queryset = solos_queryset.filter(
                artist=request.GET.get('artist', None)
            )

        context['solos'] = solos_queryset

    return render(request, 'solos/index.html', context)
