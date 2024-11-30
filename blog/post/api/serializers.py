from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='post:detail',
        lookup_field='slug'
    )
    username = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "username",
            "title",
            "content",
            "image",
            "slug",
            'url',
            "created_date",
            "user",
            "draft"
        ]

    # def username_new(self, obj):
    #     return str(obj.user.username)

    def get_username(self, obj):
        return str(obj.user.username)


class PostUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
        ]

    # def save(self, **kwargs):
    #     print("deneme 111")
    #     return True

    # def create(self, validated_data):
    #     # email göndermek, sms göndermek, .....
    #     print("create çalıştı 11111")
    #     print("validated_data  22222 ", validated_data)
    #     barcode = validated_data["content"]
    #     validated_data.pop("content")
    #     return Post.objects.create(user=self.context["request"].user,
    #                                content="NOVA-ACADEMY-" + barcode,
    #                                **validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.content = "editlendiiiiiiii. " + validated_data["content"]
    #     instance.image = validated_data.get("image", instance.image)
    #     instance.save()
    #     print("updateeee yapıldı....")
    #     return instance
    #
    # def validate(self, attrs):
    #     if attrs["title"] == "selcuk yalancı":
    #         raise serializers.ValidationError("bu değer sakıncalı. böyle birşey giremezsiniz.")
    #     if "deli" in attrs["content"]:
    #         raise serializers.ValidationError("contentin içerisinde yasaklı sözcük kullandınız."
    #                                           "Kaydı gerçekleştiremesiniz.")
    #     return attrs
    #
    # def validate_title(self, value):
    #     yasakli_kelimeler = ["deli", "aptal", "saçma", "şişman", "şişko"]
    #     control = False
    #     for i in yasakli_kelimeler:
    #         if i in value:
    #             control = True
    #     if control:
    #         raise serializers.ValidationError("Title içerisinde yasaklı kelime kullandınız. "
    #                                           "Bu şekilde veri girmeniz yasaklandı.")
    #     return value
