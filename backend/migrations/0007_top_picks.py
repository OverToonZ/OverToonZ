# Generated by Django 4.2.15 on 2024-09-15 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_animeinfo_banner_alter_animeinfo_img_src_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Top_picks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(default=0)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animepicks', to='backend.animeinfo')),
            ],
        ),
    ]
