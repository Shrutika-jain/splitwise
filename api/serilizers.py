from rest_framework import serializers
from users.models import User

class SplitAmountAmoungUserSerializer(serializers.Serializer):
    userid = serializers.UUIDField()
    amount = serializers.DecimalField(required=False, max_digits=8, decimal_places=2)
    percent = serializers.DecimalField(required=False, max_digits=5, decimal_places=2)

    def validate_userid(self, value):
        if not User.objects.filter(userid=value).exists():
            raise serializers.ValidationError(f"Invalid split_to userid {value}.")

        return value


class SplitBillSerializer(serializers.Serializer):
    amount_paid_by = serializers.UUIDField()
    split_type = serializers.ChoiceField(choices=[("EQUAL", "EQUAL"), ("EXACT", "EXACT"), ("PERCENT", "PERCENT")])
    total_amount = serializers.DecimalField(min_value=1, decimal_places=2, max_digits=8)
    split_to = SplitAmountAmoungUserSerializer(many=True)

    def validate(self, attrs):
        if attrs.get("split_type") == "PERCENT":
            # Share percentage must be 100
            total_share = sum([i["percent"] for i in attrs.get("split_to")])
            if not total_share == 100:
                raise serializers.ValidationError("Total share percentage must be equal to 100.")

        elif attrs.get("split_type") == "EXACT":
            # Share total must be equal to paid amount
            total_share = sum([i["amount"] for i in attrs.get("split_to")])

            if not total_share == attrs.get("total_amount"):
                raise serializers.ValidationError(f"Total share amount must be equal to {attrs.get("total_amount")}")

        return attrs

