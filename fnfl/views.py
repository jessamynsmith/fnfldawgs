from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Lineup
from .forms import LineupForm
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'fnfl/welcome.html', {})

@login_required
def lineup_list(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'fnfl/lineup_list.html', {'lineups': lineups})

@login_required
def lineup_detail(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    return render(request, 'fnfl/lineup_detail.html', {'lineup': lineup})

@login_required
def lineup_new(request):
    if request.method == "POST":
        form = LineupForm(request.POST)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm()
    return render(request, 'fnfl/lineup_edit.html', {'form': form})

@login_required
def lineup_edit(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    if request.method == "POST":
        form = LineupForm(request.POST, instance=lineup)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm(instance=lineup)
    return render(request, 'fnfl/lineup_edit.html', {'form': form})

@login_required
def lineup_draft_list(request):
    lineups = Lineup.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'fnfl/lineup_draft_list.html', {'lineups': lineups})

@login_required
def lineup_publish(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.publish()
    return redirect('fnfl.views.lineup_detail', pk=pk)

@login_required
def lineup_remove(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.delete()
    return redirect('fnfl.views.lineup_list')
