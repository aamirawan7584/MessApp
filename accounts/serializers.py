from rest_framework import serializers
from accounts.models import User, Vendor, Customer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'deliverylt',
            'foodserved',
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('birth_date', 'preference')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    vendor = VendorSerializer(required=True)

    customer = CustomerSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email',
                  'image', 'password', 'is_seller', 'vendor', 'customer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('is_seller') == True:
            print(validated_data)
            profile_data = validated_data.pop('vendor')
            password = validated_data.pop('password')
            image = validated_data.pop('image')
            email = validated_data.pop('email')
            username = validated_data.pop('username')
            first_name = validated_data.pop('first_name')
            last_name = validated_data.pop('last_name')
            is_seller = validated_data.pop('is_seller')
            user = User(
                email=email,
                username=username,
                image=image,
                first_name=first_name,
                last_name=last_name,
                is_seller=is_seller,
            )
            user.set_password(password)
            user.save()
            Vendor.objects.create(user=user, **profile_data)
            return user

        else:

            profile_data = validated_data.pop('customer')
            password = validated_data.pop('password')
            email = validated_data.pop('email')
            username = validated_data.pop('username')
            is_seller = validated_data.pop('is_seller')
            user = User(email=email, username=username, is_seller=is_seller)
            user.set_password(password)
            user.save()
            Customer.objects.create(user=user, **profile_data)
            return user

    def update(self, instance, validated_data):

        if validated_data.get('is_seller') == True:

            profile_data = validated_data.pop('vendor')
            # profile = instance.profile
            vendor = instance.vendor

            instance.email = validated_data.get('email', instance.email)
            instance.save()
            vendor.deliverylt = profile_data.get('deliverylt',
                                                 vendor.deliverylt)
            vendor.foodserved = profile_data.get('foodserved',
                                                 vendor.foodserved)
            vendor.save()

            return instance

        else:

            profile_data = validated_data.pop('customer')

            customer = instance.customer

            instance.email = validated_data.get('email', instance.email)

            instance.save()

            customer.birth_date = profile_data.get('birth_date',
                                                   customer.birth_date)

            customer.preference = profile_data.get('preference',
                                                   customer.preference)

            customer.save()

            return instance