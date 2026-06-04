from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(
                choices=[
                    ('new_track', 'New Track'),
                    ('like_track', 'Like Track'),
                    ('new_post', 'New Post'),
                    ('like_post', 'Like Post'),
                    ('like_comment', 'Like Comment'),
                    ('reply', 'Comment Reply'),
                    ('follow', 'New Follower'),
                    ('playlist_add', 'Added to Playlist'),
                    ('new_release', 'New Release'),
                ],
                max_length=20,
            ),
        ),
    ]
