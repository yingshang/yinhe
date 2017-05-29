from django import forms

class userinfo(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
class nm(forms.Form):
    host = forms.CharField(max_length=50)
    port = forms.CharField(max_length=50)

class cap(forms.Form):
    mode = forms.CharField(max_length=20,initial='regular')
    port = forms.CharField(max_length=20,initial='8080')