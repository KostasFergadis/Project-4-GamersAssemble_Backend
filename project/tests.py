from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from games.models import Game
from groups.models import Group

User = get_user_model()


class ApiTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner', email='owner@test.com', password='pass12345!')
        self.other = User.objects.create_user(
            username='other', email='other@test.com', password='pass12345!')
        self.game = Game.objects.create(
            title='Rust', developer='Facepunch', release_date='2018',
            image='http://x/y.png', description='Survive.', platforms='PC',
            official_site='http://rust.com')
        self.group = Group.objects.create(
            name='Raiders', game=self.game, owner=self.owner, description='We raid')

    def login(self, email):
        res = self.client.post('/api/auth/login/', {'email': email, 'password': 'pass12345!'})
        self.assertEqual(res.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['token']}")


class AuthTests(ApiTestCase):
    def test_login_rejects_bad_password(self):
        res = self.client.post('/api/auth/login/', {'email': 'owner@test.com', 'password': 'nope'})
        self.assertEqual(res.status_code, 403)

    def test_user_list_requires_auth(self):
        res = self.client.get('/api/auth/users/')
        self.assertEqual(res.status_code, 401)
        # Must not be "Basic", or browsers pop up a native login dialog.
        self.assertTrue(res['WWW-Authenticate'].startswith('Bearer'))

    def test_cannot_edit_another_users_profile(self):
        self.login('other@test.com')
        res = self.client.put(f'/api/auth/users/{self.owner.id}/', {'description': 'hacked'})
        self.assertEqual(res.status_code, 403)
        self.owner.refresh_from_db()
        self.assertNotEqual(self.owner.description, 'hacked')

    def test_can_edit_own_profile(self):
        self.login('owner@test.com')
        res = self.client.put('/api/auth/user/', {'description': 'hi'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['description'], 'hi')


class GameTests(ApiTestCase):
    def test_anonymous_cannot_delete_game(self):
        self.assertEqual(self.client.delete(f'/api/games/{self.game.id}/').status_code, 401)

    def test_non_staff_cannot_delete_game(self):
        self.login('other@test.com')
        self.assertEqual(self.client.delete(f'/api/games/{self.game.id}/').status_code, 403)

    def test_paginated_search(self):
        res = self.client.get('/api/games/?page=1&search=rus')
        self.assertEqual(res.data['count'], 1)
        res = self.client.get('/api/games/?page=1&search=zzz')
        self.assertEqual(res.data['count'], 0)


class GroupTests(ApiTestCase):
    def test_create_group_and_duplicate_name(self):
        self.login('other@test.com')
        payload = {'title': 'Rust', 'name': 'Fresh', 'description': 'd'}
        self.assertEqual(self.client.post('/api/groups/', payload).status_code, 201)
        dupe = self.client.post('/api/groups/', payload)
        self.assertEqual(dupe.status_code, 422)
        self.assertIsInstance(dupe.data['error'], str)

    def test_only_owner_can_edit_or_delete(self):
        self.login('other@test.com')
        self.assertEqual(self.client.put(f'/api/groups/{self.group.id}/', {'name': 'x'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/groups/{self.group.id}/').status_code, 403)
        self.login('owner@test.com')
        res = self.client.put(f'/api/groups/{self.group.id}/', {'name': 'Renamed'})
        self.assertEqual(res.status_code, 202)
        self.assertEqual(self.client.delete(f'/api/groups/{self.group.id}/').status_code, 204)

    def test_join_chat_and_leave(self):
        self.login('other@test.com')
        url = f'/api/groups/{self.group.id}'
        self.assertEqual(self.client.post(f'{url}/groupchat/', {'message_text': 'hey'}).status_code, 403)
        self.assertEqual(self.client.post(f'{url}/join/').status_code, 201)
        self.assertEqual(self.client.post(f'{url}/groupchat/', {'message_text': 'hey'}).status_code, 201)
        self.assertEqual(self.client.post(f'{url}/groupchat/', {'message_text': '  '}).status_code, 400)
        self.assertEqual(self.client.delete(f'{url}/leavegroup/').status_code, 204)


class RatingTests(ApiTestCase):
    def counts(self):
        self.group.refresh_from_db()
        return self.group.likes, self.group.dislikes

    def join(self, email):
        self.login(email)
        self.client.post(f'/api/groups/{self.group.id}/join/')

    def test_non_members_cannot_rate(self):
        self.login('other@test.com')
        res = self.client.post(f'/api/groups/{self.group.id}/like/')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(self.counts(), (0, 0))

    def test_same_vote_toggles_and_other_vote_switches(self):
        self.join('other@test.com')
        url = f'/api/groups/{self.group.id}'
        res = self.client.post(f'{url}/like/')
        self.assertEqual(res.data['user_rating'], 'like')
        self.assertEqual(self.counts(), (1, 0))
        res = self.client.post(f'{url}/like/')  # toggles off
        self.assertEqual(res.data['user_rating'], None)
        self.assertEqual(self.counts(), (0, 0))
        self.client.post(f'{url}/like/')
        res = self.client.post(f'{url}/dislike/')  # switches
        self.assertEqual(res.data['user_rating'], 'dislike')
        self.assertEqual(self.counts(), (0, 1))

    def test_group_detail_reports_my_rating(self):
        self.join('other@test.com')
        self.client.post(f'/api/groups/{self.group.id}/like/')
        res = self.client.get(f'/api/groups/{self.group.id}/')
        self.assertEqual(res.data['user_rating'], 'like')
        self.assertEqual(res.data['game_id'], self.game.id)
        self.client.credentials()  # anonymous
        res = self.client.get(f'/api/groups/{self.group.id}/')
        self.assertIsNone(res.data['user_rating'])

    def test_votes_from_different_users_add_up(self):
        for email in ('owner@test.com', 'other@test.com'):
            self.join(email)
            self.client.post(f'/api/groups/{self.group.id}/like/')
        self.assertEqual(self.counts(), (2, 0))
