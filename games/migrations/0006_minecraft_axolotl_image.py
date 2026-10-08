from django.db import migrations

OLD = 'https://upload.wikimedia.org/wikipedia/commons/c/cc/Minecraft_Classic_screenshot.jpg'
NEW = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Minecraft_Axolotl.jpg'


def update_image(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    Game.objects.filter(title='Minecraft').update(image=NEW)


def revert_image(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    Game.objects.filter(title='Minecraft').update(image=OLD)


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_fix_broken_game_images'),
    ]

    operations = [
        migrations.RunPython(update_image, revert_image),
    ]
