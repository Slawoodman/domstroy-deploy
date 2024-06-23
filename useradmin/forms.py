from django import forms
from core.models import Product, Category, PreCategory, Vendor, STATUS_CHOICE
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name="default"))

    class Meta:
        model = Product
        fields = [
            "category",
            "precategory",
            "tags",
            "title",
            "image",
            "description",
            "price",
            "old_price",
            "product_status",
            "status",
            "in_stock",
            "featured",
            "product_character",
            "vendor",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["precategory"].queryset = PreCategory.objects.all()
        self.fields["vendor"].queryset = Vendor.objects.all()
        self.fields["product_status"].widget = forms.Select(choices=STATUS_CHOICE)


class ProductEditForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name="default"))

    class Meta:
        model = Product
        fields = [
            "category",
            "precategory",
            "tags",
            "title",
            "image",
            "description",
            "price",
            "old_price",
            "in_stock",
            "featured",
            "vendor",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["precategory"].queryset = PreCategory.objects.all()
        self.fields["vendor"].queryset = Vendor.objects.all()
