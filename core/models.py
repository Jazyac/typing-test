from django.db import models
from django.contrib.auth.models import User

class TypingTest(models.Model):
    GAME_TYPES = [
        ('WORDS', 'Random Words'),
        ('PARAGRAPH', 'Paragraph'),
        ('CODE', 'Code Snippet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    wpm = models.IntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    errors = models.IntegerField()
    test_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.game_type} - {self.wpm} WPM"

class TextSample(models.Model):
    game_type = models.CharField(max_length=20, choices=TypingTest.GAME_TYPES)
    content = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ])
    
    def __str__(self):
        return f"{self.game_type} - {self.difficulty}" 