from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether this user profile has been verified.',
                verbose_name='Verified',
            ),
        ),
    ]
