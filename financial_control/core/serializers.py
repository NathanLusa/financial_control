from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Account, Category, Transaction


class BaseModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        ModelClass = self.Meta.model

        kwargs = {}
        create_fields_verify = getattr(self.Meta, 'create_fields_verify', [])

        for item in create_fields_verify:
            kwargs[item] = validated_data[item]

        # kwargs = {
        #     '{0}__{1}'.format('name', 'startswith'): 'A',
        #     '{0}__{1}'.format('name', 'endswith'): 'Z'
        # }

        instance = None
        if len(kwargs) > 0:
            instance = ModelClass._default_manager.filter(**kwargs).first()

        if not instance:
            instance = ModelClass._default_manager.create(**validated_data)

        return instance


class AccountSerializer(BaseModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        create_fields_verify = ['description', 'type']


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        create_fields_verify = ['description']


class TransactionSerializer(BaseModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        create_fields_verify = ['description', 'date', 'value', 'account']


class AccountDashboardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    # value = serializers.DecimalField(max_digits=15, decimal_places=2)
