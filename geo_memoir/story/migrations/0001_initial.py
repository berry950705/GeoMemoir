# Generated by Django 2.2.12 on 2022-08-16 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('area', models.CharField(max_length=32)),
                ('category', models.CharField(max_length=32)),
                ('country', models.CharField(max_length=64)),
                ('photo', models.ImageField(upload_to='photo')),
                ('photo_desc', models.CharField(max_length=512)),
                ('content', models.TextField(default='')),
                ('view', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_author', to='user.UserProfile')),
                ('like', models.ManyToManyField(default=None, related_name='story_like', to='user.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='LikeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_clicked', models.BooleanField(default=False)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story.Story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
        ),
    ]
