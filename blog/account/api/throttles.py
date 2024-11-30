from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle, UserRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerThrottle'

    def get_cache_key(self, request, view):
        # if request.user.is_authenticated or request.method == 'GET':
        #     # burada giriş yaptıysa ya da get isteği atmışsa sıkıntı yok.
        #     # ancak post isteği varsa throttle counter sayıyor
        #     return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class RegisterAnonThrottle(AnonRateThrottle):
    scope = 'registerAnonThrottle'


class RegisterUserRateThrottle(UserRateThrottle):
    # gelen kişi user'sa id'sine göre işlem yapar, değilse ip'sine göre işlem yapar.
    scope = 'registerUserRateThrottle'
