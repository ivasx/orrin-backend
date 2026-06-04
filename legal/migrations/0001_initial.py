from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LegalDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(
                    choices=[('terms', 'Terms of Service'), ('privacy', 'Privacy Policy')],
                    max_length=10,
                    verbose_name='Document type',
                )),
                ('language', models.CharField(
                    choices=[('en', 'English'), ('uk', 'Ukrainian')],
                    default='en',
                    max_length=5,
                    verbose_name='Language',
                )),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('last_updated', models.DateField(verbose_name='Last updated')),
                ('sections', models.JSONField(
                    default=list,
                    help_text='JSON array of { "id", "title", "content" } objects.',
                    verbose_name='Sections',
                )),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text='Only the active version is served via the API.',
                    verbose_name='Active',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Legal document',
                'verbose_name_plural': 'Legal documents',
                'ordering': ('doc_type', 'language'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='legaldocument',
            unique_together={('doc_type', 'language')},
        ),
    ]
