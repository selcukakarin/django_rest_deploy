import json

import django

django.setup()

from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


# Create your tests here.

# 1 - Doğru verilerle kayıt işlemi - 201 Created
# 2 - Şifre invalid olabilir - 400 Bad Request
# 3 - Kullanıcı adı kullanılmış olabilir - 400 Bad Request
# 4 - Üye girişi yaptıysak register sayfası görünmemeli - 403 Forbidden
# 5 -

class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")

    def test_user_registeration(self):
        """
            Doğru verilerle kullanıcı kaydı işlemi.
            Bu testte, geçerli kullanıcı bilgileri ile bir POST isteği gönderiliyor.
            ve kullanıcının başarılı bir şekilde kaydedildiği kontrol ediliyor.
            201 Created HTTP status gelecek
        """
        data = {
            "username": "selcuktest1",
            "password": "deneme1SSS"
        }

        response = self.client.post(self.url, data)
        # 201 Created
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        """
            Geçersiz bir parola ile kullanıcı kaydı.
            Bu testte, geçersiz bir parola ile kullanıcı kaydı denemesi yapılıyor ve
            kaydın reddedildiği kontrol ediliyor.
            400 Bad Request HTTP Status
        """
        data = {
            "username": "selcukdeneme1",
            "password": "1"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        """
            Benzersiz kullanıcı adı testi.
            Bu testte, aynı kullanıcı adıyla ikinci bir kayıt denemesi yapılıyor.
            ve bu kaydın reddedildiği kontrol ediliyor.
            400 Bad Request Http Status
        """

        self.test_user_registeration()  # ilk kullanıcı kaydını oluşturuyor
        data = {
            "username": "selcuktest1",
            "password": "deneme1SSS"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """
            Oturum açmış bir kullanıcı, kayıt sayfasını görememeli.
            Bu testte, oturum açmış bir kullanıcının kayıt sayfasına erişimi deneniyor.
            ve bu erişimin engellendiği kontrol ediliyor.
            403 forbidden durum kodu bekleniyor.
        """
        self.test_user_registeration()
        data = {
            "username": "selcuktest1",
            "password": "deneme1SSS"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response2 = self.client.get(self.url)
        self.assertEqual(403, response2.status_code)


class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "nova111"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        """
            Geçerli kullanıcı bilgileri ile giriş yapma testi.
            Bu testte, doğru kullanıcı adı ve parola ile token alma denemesi yapılır.
            Başarılı olduğunda 200 OK durum kodu beklenir ve token'ın içeriğinde "access" anahtarının
            bulunduğu kontrol edilir.
        """

        response = self.client.post(self.url_login, {"username": "nova111", "password": "Microman1903"})
        self.assertEqual(200, response.status_code)
        print(json.loads(response.content))
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        """
            Geçersiz kullanıcı bilgileriyle giriş yapma testi.
            Bu testte, yanlış kullanıcı adı veya parola ile giriş denemesi yapılır.
            401 Unauthorized durum kodu beklenir.
        """
        response = self.client.post(self.url_login, {"username": "nova999", "password": "Microman1903"})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        """
            Boş kullanıcı bilgileriyle giriş yapma testi.
            Bu testte, boş kullanıcı adı ve parola ile giriş deneme yapılır.
            400 Bad Request durum kodu beklenir.
        """
        response = self.client.post(self.url_login, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)


class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "yıldız111",
            "password": "Microman1903"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated(self):
        """
            Oturum açmadan parola değiştirme sayfasına erişim testi.
            Bu testte, oturum açmamış bir kullanıcının parola değiştirme sayfasına erişmeye çalışması
            durumunda 401 Unathorized durum kodu beklenir.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_information(self):
        """
            Geçerli bilgilerle parola değiştirme testi.
            Bu testte, doğru eski parola ve yeni parola bilgileri girildiğinde,
            parolanın başarılı bir şekilde değiştirildiği ve 204 No Content durum kodu döndürüldüğü
            kontrol edilir.
        """
        self.login_with_token()
        data = {
            "old_password": "Microman1903",
            "new_password": "asfaswqr1223S"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_information(self):
        """
            Yanlış bilgilerle parola değiştirme testi.
            Bu testte, yanlış eski parola ile parola değiştirme denemesi yapıldığında,
            400 Bad Request durum kodu döndürüldüğü kontrol edilir.
        """
        self.login_with_token()
        data = {
            "old_password": "Microman19032321312xvxzsaras",
            "new_password": "asfaswqr1223S"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_with_empty_information(self):
        """
            Boş bilgilerle parola değiştirme testi.
            Bu testte, eski ve yeni parola bilgileri boş olarak gönderildiğinde,
            400 Bad request durum kodu döndürüldüğü kontrol edilir.
        """
        self.login_with_token()
        data = {
            "old_password": "",
            "new_password": ""
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)


class UserProfileUpdate(APITestCase):
    url = reverse("account:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yıldız111"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "yıldız111",
            "password": "Microman1903"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated(self):
        """
            Oturum açmadan profile sayfasına sayfasına erişim testi.
            Bu testte, oturum açmamış bir kullanıcının parola değiştirme sayfasına erişmeye çalışması
            durumunda 401 Unathorized durum kodu beklenir.
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_information(self):
        """
            Geçerli bilgilerle profil güncelleme test.
            Bu testte, geçerli ve doğru bilgilerle profil güncellemesi yapıldığında,
            200 OK durum kodu döndürüldüğü ve güncellenen verilerin doğru bir şekilde
            döndürüldüğü kontrol edilir.
        """
        self.login_with_token()
        data = {
            "id": 25,
            "first_name": "selcuk 99999",
            "last_name": "akarın 99999",
            "profile": {
                "id": 23,
                "note": "asgagdcxzvbxc 99999",
                "twitter": "selcuk@twitter 99999"
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), data)

    def test_user_empty_data(self):
        """
            Boş bilgilerle profil güncelleme test.
            Bu testte, boş bilgilerle profil güncellemesi yapıldığında,
            400 OK durum kodu döndürüldüğü ve güncellenen verilerin doğru bir şekilde
            döndürüldüğü kontrol edilir.
        """
        self.login_with_token()
        data = {
            "id": 25,
            "first_name": "",
            "last_name": "",
            "profile": {
                "id": 23,
                "note": "",
                "twitter": ""
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(400, response.status_code)
