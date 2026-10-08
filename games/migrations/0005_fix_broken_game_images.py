from django.db import migrations

# Image hosts that stopped serving these files. Applied as a data migration so
# existing databases (e.g. on Render) are fixed on the next deploy.
STEAM = 'https://cdn.cloudflare.steamstatic.com/steam/apps'
NEW_IMAGES = {
    'Overwatch 2': f'{STEAM}/2357570/capsule_616x353.jpg',
    'Warframe': f'{STEAM}/230410/capsule_616x353.jpg',
    'Minecraft': 'https://upload.wikimedia.org/wikipedia/commons/c/cc/Minecraft_Classic_screenshot.jpg',
}


def fix_images(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    for title, image in NEW_IMAGES.items():
        Game.objects.filter(title=title).update(image=image)


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_game_release_date'),
    ]

    operations = [
        migrations.RunPython(fix_images, migrations.RunPython.noop),
    ]
