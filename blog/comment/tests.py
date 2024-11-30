import django

django.setup()
from comment.models import Comment

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from post.models import Post


# Create your tests here.

class CommentCreate(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.create_url = reverse("comment:create")
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.parent_comment = Comment.objects.create(content="commentin içeriği", user=self.user, post=self.post)
        self.url_list = reverse("comment:list")
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

    def test_create_comment(self):
        """
            Kullanıcının bir posta yeni bir comment ekleyip ekleyemediğini test eder.
            başarılı olursa 201 gelir.
        """
        data = {
            "content": "yeni yorum yapıyorum.",
            "user": self.user.id,
            "post": self.post.id,
            "parent": ""
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(201, response.status_code)

    def test_create_child_comment(self):
        """
            Kullanıcının mevcut bir yoruma yanıt olarak alt bir yorum (child comment) ekleyip
            ekleyemediğini test eder.
        """
        data = {
            "content": "child comment oluşturuyorum..",
            "user": self.user.id,
            "post": self.post.id,
            "parent": self.parent_comment.id  # Bu parent_comment, yeni oluşturacağımız yorumun atasıdır.
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(201, response.status_code)

    def test_comment_list(self):
        """
            Belirli bir gönderiye ait tüm yorumların listelenip listelenmediğini test eder.
        """
        self.test_create_comment()  # ilk olarak bir yorum oluşturulur.
        response = self.client.get(self.url_list, {'q': self.post.id})
        self.assertTrue(response.data['count'] == Comment.objects.filter(post=self.post).count())


class CommentUpdateDeleteTest(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="nova1", password="nova1")
        self.parent_comment = Comment.objects.create(content="commentin içeriği", user=self.user, post=self.post)
        self.update_delete_url = reverse("comment:update", kwargs={'pk': self.parent_comment.pk})
        self.login_with_token()

    def login_with_token(self, username="yıldız111", password="Microman1903"):
        data = {
            "username": username,
            "password": password
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_delete_comment(self):
        """
            Kullanıcının kendi yorumunu başarılı bir şekilde silip silemediğini test eder.
            Silme işlemi başarılı olduğunda, yorum veritabanından tamamen kaldırılır.
            204 geri döner.
        """
        response = self.client.delete(self.update_delete_url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Comment.objects.filter(pk=self.parent_comment.pk).exists())

    def test_delete_other_user(self):
        """
            Başka bir kullanıcının bir başka kullanıcının yorumunu silip silemediğini test eder.
            Başarısız olursa 403 forbidden hatası döner ve yorumu silmez.
        """
        self.login_with_token("nova1", "nova1")
        response = self.client.delete(self.update_delete_url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk=self.parent_comment.pk))

    def test_update_comment(self):
        """
            Kullanıcının kendi yorumunu başarılı bir şekilde güncelleyip güncelleyemediğini test eder.
            Güncelle başarılı olduğunda, yorumun içeriği değişir.
        """
        response = self.client.put(self.update_delete_url, data={"content": "içerik 1111"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk=self.parent_comment.id).content, "içerik 1111")

    def test_update_comment_other_user(self):
        """
            Başka bir kullanıcının bir başka kullanıcının yorumunu güncelleyip güncelleyemediğini
            test eder.
            Başarısız olursa 403 Forbidden hatası döner ve yorumun içeriği değişmez.
        """
        self.login_with_token(username="nova1", password="nova1")
        response = self.client.put(self.update_delete_url, data={"content": "içerik 1111"})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk=self.parent_comment.id).content, "içerik 1111")

    def test_unauthorization(self):
        """
            Oturum açmamış bir kullanıcının yorum update sayfasına erişip erişşemeyeceğini test eder.
            Yetkisiz erişim denemesi olduğu zaman 401 hatası döndürülmelidir.
        """
        self.client.credentials()       # oturumu kapatır. logout
        response = self.client.get(self.update_delete_url)
        self.assertEqual(401, response.status_code)
