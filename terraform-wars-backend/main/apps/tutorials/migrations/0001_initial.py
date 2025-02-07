# Generated by Django 5.1.3 on 2024-11-16 22:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorialGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Tutorial Group',
                'verbose_name_plural': 'Tutorial Groups',
            },
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('ordering', models.PositiveIntegerField(default=0, verbose_name='Ordering')),
                ('tutorial_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutorials', to='tutorials.tutorialgroup')),
            ],
            options={
                'verbose_name': 'Tutorial',
                'verbose_name_plural': 'Tutorials',
            },
        ),
        migrations.CreateModel(
            name='TutorialUserSubmission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutorial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tutorial Submission',
                'verbose_name_plural': 'Tutorial Submissions',
                'constraints': [models.UniqueConstraint(fields=('tutorial', 'user'), name='unique_user_tutorial_submission')],
            },
        ),
    ]
