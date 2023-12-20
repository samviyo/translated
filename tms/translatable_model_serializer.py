from rest_framework import serializers
from .translated import use_translated, lazy_translate as _


class TranslatableModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.Meta, "translated_fields"):
            for field_name in self.Meta.translated_fields:
                method = self.create_translated_field_method(field_name)
                setattr(self, f"get_translated_{field_name}", method)
                self.fields[f"{field_name}"] = serializers.SerializerMethodField(
                    method_name=f"get_translated_{field_name}"
                )

    def create_translated_field_method(self, field_name):
        def method(instance):
            return self.get_field_translated(instance, field_name)

        return method

    def get_field_translated(self, obj, field_name):
        if hasattr(self, f"get_{field_name}"):
            original_text = getattr(self, f"get_{field_name}")(obj)
        else:
            original_text = getattr(obj, field_name, "")
        return _(original_text)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if use_translated() and hasattr(self.Meta, "translated_fields"):
            for field_name in self.Meta.translated_fields:
                translated_value = self.get_field_translated(instance, field_name)
                data[field_name] = translated_value
        return data
