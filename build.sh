#!/usr/bin/env bash
# Build step for Render (see render.yaml). Exits on the first error.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Optional: set LOAD_SEEDS=true to fill an empty database with the demo data.
# Groups and members reference each other, so everything is loaded in one
# loaddata call (a single transaction) rather than one call per app.
if [ "$LOAD_SEEDS" = "true" ] && [ "$(python manage.py shell -c 'from games.models import Game; print(Game.objects.exists())')" = "False" ]; then
  python manage.py loaddata jwt_auth/seeds.json genres/seeds.json games/seeds.json \
    groups/seeds.json members/seeds.json ratings/seeds.json groupchat/seeds.json
fi
