import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orrin', '0003_artist_is_verified_track_plays_count_lyrics_album'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ── Note ─────────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Note text')),
                ('note_type', models.CharField(
                    choices=[('public', 'Public'), ('private', 'Private')],
                    default='public',
                    max_length=10,
                    verbose_name='Visibility',
                )),
                ('timecode', models.FloatField(
                    blank=True,
                    null=True,
                    help_text='Offset in seconds within the track.',
                    verbose_name='Timecode (seconds)',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Author',
                )),
                ('track', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notes',
                    to='orrin.track',
                    verbose_name='Track',
                )),
                ('artist', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notes',
                    to='orrin.artist',
                    verbose_name='Artist',
                )),
                ('lyric_line', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='notes',
                    to='orrin.lyricline',
                    verbose_name='Lyric line reference',
                )),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),

        # ── NoteLike ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='NoteLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='note_likes',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('note', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='likes',
                    to='notes.note',
                )),
            ],
        ),

        # ── Indexes ───────────────────────────────────────────────────────────
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['track', 'note_type'], name='notes_note_track_type_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['artist', 'note_type'], name='notes_note_artist_type_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['author', 'note_type'], name='notes_note_author_type_idx'),
        ),
        migrations.AddIndex(
            model_name='notelike',
            index=models.Index(fields=['note'], name='notes_notelike_note_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='notelike',
            unique_together={('user', 'note')},
        ),

        # ── Constraint: note must have track or artist ─────────────────────
        migrations.AddConstraint(
            model_name='note',
            constraint=models.CheckConstraint(
                check=(
                    models.Q(track__isnull=False) |
                    models.Q(artist__isnull=False)
                ),
                name='note_must_have_track_or_artist',
            ),
        ),
    ]
