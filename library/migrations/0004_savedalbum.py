import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_initial'),
        ('orrin', '0003_artist_is_verified_track_plays_count_lyrics_album'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='saved_albums',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('album', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='saved_by',
                    to='orrin.album',
                )),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddIndex(
            model_name='savedalbum',
            index=models.Index(fields=['user', 'created_at'], name='library_sav_user_id_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='savedalbum',
            unique_together={('user', 'album')},
        ),
    ]
