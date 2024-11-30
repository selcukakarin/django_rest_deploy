import django

django.setup()
from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from favorite.models import Favorite
from post.models import Post


class FavoriteCreateList(APITestCase):
    url = reverse("favorite:list-create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_with_token()

    def login_with_token(self):
        data = {
            "username": "yıldız111",
            "password": "Microman1903"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_add_favorite(self):
        """
            Kullanıcının bir gönderiyi favorilere ekleyip ekleyemediğini test eder.
        """
        data = {
            "content": "bu post çok harika.",
            "user": self.user.id,
            "post": self.post.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_favs(self):
        """
            Kullanıcının favori gönderilerini listeleyip listeleyemediğini test eder.
        """
        # bir post bir kullanıcının favorilerine eklenir.
        self.test_add_favorite()
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"]) == Favorite.objects.filter(
            user=self.user).count())


class FavoriteUpdateDeleteTest(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="Nova_user", password="NovaSifre")
        self.favorite = Favorite.objects.create(post=self.post,
                                                user=self.user,
                                                content="user'ın bu post için olan yorumu")
        self.update_url = reverse("favorite:update-retrieve", kwargs={"pk": self.favorite.pk})
        self.delete_url = reverse("favorite:delete-retrieve", kwargs={"pk": self.favorite.pk})
        self.login_with_token()

    def login_with_token(self, username="yıldız111", password="Microman1903"):
        data = {
            "username": username,
            "password": password
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_fav_delete(self):
        """
            Kullanıcının kendi favori gönderisini silip silemediğini test eder.
        """
        response = self.client.delete(self.delete_url)
        self.assertEqual(204, response.status_code)

    def test_fav_delete_different_user(self):
        """
            Farklı bir kullanıcının başka bir kullanıcıya ait favori postu silmeye çalışması durumunda
            yetkisizlik 403 hastası alıp almadığını test eder.
        """
        self.login_with_token("Nova_user", "NovaSifre")
        response = self.client.delete(self.delete_url)
        self.assertEqual(403, response.status_code)

    def test_fav_update(self):
        """
            Kullanıcının kendi favori postunu güncelleyip güncelleyemediğini test eder.
        """
        data = {
            "content": "içerik 123",
            "post": self.post.id,
            "user": self.user.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(200, response.status_code)

    def test_fav_update_different_user(self):
        """
            Farklı bir kullanıcının başka bir kullanıcıya ait favori postu güncellemeye çalışması durumunda
            yetkisizlik 403 hatası alıp almadığını test eder.
        """
        self.login_with_token("Nova_user", "NovaSifre")
        data = {
            "content": "içerik 123",
            "post": self.post.id,
            "user": self.user2.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(403, response.status_code)

    def test_unauthorization(self):
        """
            Kullacının oturum açmadan bir favori kaydını görüntülemeye çalışması durumunda yetkisizlik 401
            hatası alıp almadığını test eder.
        """
        self.client.credentials()           # bu şekilde oturum sonlandırılmış olur
        response = self.client.get(self.delete_url)
        self.assertEqual(401, response.status_code)
