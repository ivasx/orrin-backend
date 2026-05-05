from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orrin', '0002_alter_artist_genres'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='liked_tracks',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('track', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='liked_by',
                    to='orrin.track',
                )),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('user', 'track')},
            },
        ),
        migrations.AddIndex(
            model_name='likedtrack',
            index=models.Index(fields=['user', 'track'], name='library_lik_user_id_idx'),
        ),
        migrations.CreateModel(
            name='FollowedArtist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='followed_artists',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('artist', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='followers',
                    to='orrin.artist',
                )),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('user', 'artist')},
            },
        ),
        migrations.AddIndex(
            model_name='followedartist',
            index=models.Index(fields=['user', 'artist'], name='library_fol_user_id_idx'),
        ),
        migrations.CreateModel(
            name='ListeningHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='listening_history',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('track', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='history_entries',
                    to='orrin.track',
                )),
            ],
            options={
                'ordering': ('-played_at',),
            },
        ),
        migrations.AddIndex(
            model_name='listeninghistory',
            index=models.Index(fields=['user', 'played_at'], name='library_his_user_id_idx'),
        ),
    ]
