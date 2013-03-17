from django.test import Client
from django.utils import unittest

class InstagramTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_correct1(self):
        challenge = '11241023410'
        token = 'geography'
        subscribe = 'subscribe'
        response = self.client.get(
                '/instagram/subscription/?hub.challenge=%s&hub.verify_token=%s&hub.mode=%s'
                % (challenge, token, subscribe))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, challenge)

    def test_get_correct2(self):
        challenge = '0'
        token = 'geography'
        subscribe = 'subscribe'
        response = self.client.get(
                '/instagram/subscription/?hub.challenge=%s&hub.verify_token=%s&hub.mode=%s'
                % (challenge, token, subscribe))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, challenge)

    def test_get_wrong_token(self):
        challenge = '11241023410'
        token = 'foo'
        subscribe = 'subscribe'
        response = self.client.get(
                '/instagram/subscription/?hub.challenge=%s&hub.verify_token=%s&hub.mode=%s'
                % (challenge, token, subscribe))
        self.assertEqual(response.status_code, 403)

    def test_get_wrong_subscribe(self):
        challenge = '11241023410'
        token = 'geography'
        subscribe = 'foo'
        response = self.client.get(
                '/instagram/subscription/?hub.challenge=%s&hub.verify_token=%s&hub.mode=%s'
                % (challenge, token, subscribe))
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        import simplejson
        json_string = u'''[{ "subscription_id": "1", "object": "user",
        "object_id": "1234", "changed_aspect": "media", "time": 1297286541 }, {
        "subscription_id": "2", "object": "tag", "object_id": "nofilter",
        "changed_aspect": "media", "time": 1297286541 }]'''
        json_data = simplejson.loads(json_string)
        response = self.client.post(
                '/instagram/subscription/', json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
