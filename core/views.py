from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import TypingTest, TextSample
import json
import random
from django.db import models

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def game(request, game_type):
    if game_type not in dict(TypingTest.GAME_TYPES):
        return redirect('home')
    
    context = {
        'game_type': game_type,
    }
    return render(request, 'core/game.html', context)

@login_required
def get_text(request, game_type):
    samples = TextSample.objects.filter(game_type=game_type)
    if not samples:
        # Fallback text if no samples are available
        if game_type == 'WORDS':
            words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
                    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at']
            text = ' '.join(random.sample(words, 15))
        else:
            text = "The quick brown fox jumps over the lazy dog."
    else:
        sample = random.choice(samples)
        text = sample.content
    
    return JsonResponse({'text': text})

@csrf_exempt
@login_required
def save_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        TypingTest.objects.create(
            user=request.user,
            game_type=data['game_type'],
            wpm=data['wpm'],
            accuracy=data['accuracy'],
            errors=data['errors'],
            test_text=data['test_text']
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def profile(request):
    user_tests = TypingTest.objects.filter(user=request.user)
    stats = {
        'total_tests': user_tests.count(),
        'avg_wpm': user_tests.aggregate(models.Avg('wpm'))['wpm__avg'] or 0,
        'max_wpm': user_tests.aggregate(models.Max('wpm'))['wpm__max'] or 0,
        'avg_accuracy': user_tests.aggregate(models.Avg('accuracy'))['accuracy__avg'] or 0,
    }
    recent_tests = user_tests[:10]
    
    context = {
        'stats': stats,
        'recent_tests': recent_tests,
    }
    return render(request, 'core/profile.html', context) 