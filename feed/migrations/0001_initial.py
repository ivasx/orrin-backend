from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orrin', '0003_playlistmodel_description_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='orrin.track')),
            ],
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author', 'created_at'], name='feed_post_author_idx'),
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='feed.post')),
            ],
            options={'unique_together': {('user', 'post')}},
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['post'], name='feed_postlike_post_idx'),
        ),
        migrations.CreateModel(
            name='PostRepost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reposts', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reposts', to='feed.post')),
            ],
            options={'unique_together': {('user', 'post')}},
        ),
        migrations.AddIndex(
            model_name='postrepost',
            index=models.Index(fields=['post'], name='feed_postrepost_post_idx'),
        ),
        migrations.CreateModel(
            name='PostSave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_posts', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saves', to='feed.post')),
            ],
            options={'unique_together': {('user', 'post')}},
        ),
        migrations.AddIndex(
            model_name='postsave',
            index=models.Index(fields=['user', 'created_at'], name='feed_postsave_user_idx'),
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feed.post')),
            ],
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['post', 'created_at'], name='feed_postcomment_post_idx'),
        ),
        migrations.CreateModel(
            name='PostReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('spam', 'Spam'), ('inappropriate', 'Inappropriate'), ('harassment', 'Harassment'), ('other', 'Other')], default='other', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_reports', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='feed.post')),
            ],
            options={'unique_together': {('user', 'post')}},
        ),
    ]
