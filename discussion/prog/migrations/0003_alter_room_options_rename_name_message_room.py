# Generated by Django 4.0.2 on 2022-02-22 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prog', '0002_topic_alter_room_options_room_host_message_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='name',
            new_name='room',
        ),
    ]
