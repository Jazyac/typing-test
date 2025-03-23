from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import TypingTest, TextSample
import json
import random
from django.db import models
from django.db.models import Avg, Max, Count
from datetime import datetime, timedelta

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def game(request, game_type):
    game_type = game_type.upper()
    return render(request, 'core/game.html', {'game_type': game_type})

@login_required
def get_text(request, game_type):
    game_type = game_type.upper()
    text_samples = TextSample.objects.filter(game_type=game_type)
    if not text_samples.exists():
        return JsonResponse({'error': 'No text samples found for this game type'}, status=404)
    
    random_sample = random.choice(text_samples)
    return JsonResponse({'text': random_sample.content})

@csrf_exempt
@login_required
def save_result(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        test = TypingTest.objects.create(
            user=request.user,
            wpm=data['wpm'],
            accuracy=data['accuracy'],
            errors=data['errors'],
            test_text=data['test_text'],
            game_type=data['game_type']
        )
        return JsonResponse({'id': test.id})
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required
def profile(request):
    # Get user's tests
    user_tests = TypingTest.objects.filter(user=request.user)
    
    # Calculate overall statistics
    stats = user_tests.aggregate(
        avg_wpm=Avg('wpm'),
        avg_accuracy=Avg('accuracy'),
        total_tests=Count('id'),
        best_wpm=Max('wpm')
    )
    
    # Get best accuracy test
    best_accuracy_test = user_tests.order_by('-accuracy').first()
    
    # Calculate statistics by game type
    type_stats = {}
    for game_type in ['WORDS', 'PARAGRAPH', 'CODE']:
        type_tests = user_tests.filter(game_type=game_type)
        if type_tests.exists():
            type_stats[game_type] = {
                'count': type_tests.count(),
                'avg_wpm': type_tests.aggregate(Avg('wpm'))['wpm__avg'],
                'avg_accuracy': type_tests.aggregate(Avg('accuracy'))['accuracy__avg'],
                'max_wpm': type_tests.aggregate(Max('wpm'))['wpm__max']
            }
    
    # Calculate streak
    dates = user_tests.values_list('timestamp', flat=True).order_by('timestamp')
    longest_streak = 1
    current_streak = 1
    if dates:
        prev_date = dates[0].date()
        for date in dates[1:]:
            current_date = date.date()
            if (current_date - prev_date).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            elif (current_date - prev_date).days > 1:
                current_streak = 1
            prev_date = current_date
    
    context = {
        'avg_wpm': stats['avg_wpm'] or 0,
        'avg_accuracy': stats['avg_accuracy'] or 0,
        'total_tests': stats['total_tests'],
        'recent_tests': user_tests.order_by('-timestamp')[:10],
        'type_stats': type_stats,
        'best_wpm': stats['best_wpm'] or 0,
        'best_wpm_date': user_tests.filter(wpm=stats['best_wpm']).first().timestamp if stats['best_wpm'] else None,
        'best_accuracy': best_accuracy_test.accuracy if best_accuracy_test else 0,
        'best_accuracy_date': best_accuracy_test.timestamp if best_accuracy_test else None,
        'longest_streak': longest_streak
    }
    
    return render(request, 'core/profile.html', context)
