import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orrin', '0002_initial'),
    ]

    operations = [
        # ── Artist ───────────────────────────────────────────────────────────
        migrations.AddField(
            model_name='artist',
            name='is_verified',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether this artist profile has been officially verified.',
                verbose_name='Verified',
            ),
        ),

        # ── Track ────────────────────────────────────────────────────────────
        migrations.AddField(
            model_name='track',
            name='plays_count',
            field=models.PositiveBigIntegerField(
                db_index=True,
                default=0,
                help_text='Denormalised counter incremented on each listen.',
                verbose_name='Play count',
            ),
        ),

        # ── Lyrics ───────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Lyrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lyrics_type', models.CharField(
                    choices=[('static', 'Static'), ('synced', 'Synced')],
                    default='static',
                    max_length=10,
                    verbose_name='Lyrics type',
                )),
                ('plain_text', models.TextField(blank=True, default='', verbose_name='Plain text lyrics')),
                ('track', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='lyrics',
                    to='orrin.track',
                    verbose_name='Track',
                )),
            ],
            options={
                'verbose_name': 'Lyrics',
                'verbose_name_plural': 'Lyrics',
            },
        ),

        # ── LyricLine ────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='LyricLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_seconds', models.FloatField(
                    help_text='Timestamp in seconds when this line starts.',
                    verbose_name='Start time (seconds)',
                )),
                ('text', models.CharField(max_length=500, verbose_name='Line text')),
                ('lyrics', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='lines',
                    to='orrin.lyrics',
                    verbose_name='Lyrics',
                )),
            ],
            options={
                'verbose_name': 'Lyric line',
                'verbose_name_plural': 'Lyric lines',
                'ordering': ('time_seconds',),
            },
        ),

        # ── Album ────────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='images/albums/', verbose_name='Cover image')),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Release year')),
                ('album_type', models.CharField(
                    choices=[
                        ('album', 'Album'),
                        ('ep', 'EP'),
                        ('single', 'Single'),
                        ('compilation', 'Compilation'),
                    ],
                    default='album',
                    max_length=15,
                    verbose_name='Release type',
                )),
                ('artist', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='albums',
                    to='orrin.artist',
                    verbose_name='Artist',
                )),
            ],
            options={
                'ordering': ('-year', 'title'),
            },
        ),

        # ── AlbumTrack ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='AlbumTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_number', models.PositiveSmallIntegerField(default=1, verbose_name='Track number')),
                ('album', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='album_tracks',
                    to='orrin.album',
                )),
                ('track', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='album_entries',
                    to='orrin.track',
                )),
            ],
            options={
                'ordering': ('track_number',),
            },
        ),

        # ── AlbumTrack M2M on Album ──────────────────────────────────────────
        migrations.AddField(
            model_name='album',
            name='tracks',
            field=models.ManyToManyField(
                blank=True,
                related_name='albums',
                through='orrin.AlbumTrack',
                to='orrin.track',
            ),
        ),

        # ── Unique constraints ────────────────────────────────────────────────
        migrations.AlterUniqueTogether(
            name='albumtrack',
            unique_together={('album', 'track')},
        ),
    ]
