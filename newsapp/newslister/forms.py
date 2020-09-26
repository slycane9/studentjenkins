from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import NewsListing, UserXtraAuth
import json

class UpdateUserForm(forms.Form):
    update_user_select = forms.ModelChoiceField(
        label="Username",
        queryset=User.objects.filter(is_superuser=False))
    update_user_token    = forms.CharField(label="Token ID", required=False)
    update_user_secrecy  = forms.IntegerField(label="Secrecy Level")

    def clean(self):
        # STUDENT TODO
        # This is where the "update user" form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["update_user_secrecy"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something
        # is wrong
        cleaned_data = super().clean()
        if self.is_valid():
            user_auth = UserXtraAuth.objects.get(username=cleaned_data["update_user_select"])
            # make sure we do not reduce the secrecy level
            if cleaned_data["update_user_secrecy"] is None or cleaned_data["update_user_secrecy"] < user_auth.secrecy:
                raise ValidationError("You cannot reduce the secrecy level of a user")

            if cleaned_data["update_user_token"] == "" and cleaned_data["update_user_secrecy"] > 0:
                raise ValidationError("You must set a token for anyone above secrecy 0")

        return cleaned_data

class CreateNewsForm(forms.Form):
    new_news_query = forms.CharField(label="New Query", required=False)
    new_news_sources = forms.CharField(label="Sources", required=False)
    new_news_secrecy = forms.IntegerField(label="Secrecy Level", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_secrecy = 0

    def clean(self):
        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something
        # is wrong
        cleaned_data = super().clean()

        if self.is_valid():
            if cleaned_data["new_news_secrecy"] is None or cleaned_data["new_news_secrecy"] < self.user_secrecy:
                raise ValidationError("You cannot create a listing with a lower secrecy level (NWD)")

        return cleaned_data

class UpdateNewsForm(forms.Form):
    update_news_select = forms.ModelChoiceField(
        label="Update News",
        queryset=None,
        required=False)
    update_news_query   = forms.CharField(label="Update Query", required=False)
    update_news_sources = forms.CharField(label="Update Sources", required=False)
    update_news_secrecy = forms.IntegerField(label="Update Secrecy", required=False)

    update_delete = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_secrecy = 0

        # STUDENT TODO
        # you should change the "queryset" in update_news_select to be None.
        # then, here in the constructor, you can change it to be the filtered
        # data passed in. See this page:
        # https://docs.djangoproject.com/en/3.1/ref/forms/fields/
        # Look specifically in the section "Fields which handle relationships¶"
        # where it talks about starting with an empty queryset.
        #
        # This form is constructed in views.py. Modify this constructor to
        # accept the passed-in (filtered) queryset.

    def populate_select(self, queryset):
        self.fields["update_news_select"].queryset = queryset

    def clean(self):
        cleaned_data = super().clean()
        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something
        # is wrong
        try:
            # print(cleaned_data)
            # print(cleaned_data["update_news_select"])
            selected_listing = NewsListing.objects.get(queryId=cleaned_data["update_news_select"])
            if selected_listing.secrecy != self.user_secrecy:
                raise ValidationError("Please select a listing")
        except NewsListing.DoesNotExist:
            raise ValidationError("Please select a listing")

        if self.is_valid():
            if cleaned_data["update_delete"] == "" and (cleaned_data["update_news_secrecy"] is None or cleaned_data["update_news_secrecy"] < self.user_secrecy):
                raise ValidationError("You cannot update a listing to a lower secrecy level (NWD)")

        return cleaned_data