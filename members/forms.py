from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	firstname=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
	lastname=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

	#there is no fileld of addresss to save in database
	#address=forms.CharField(max_length=200)


	class Meta:
		model=User
		fields=('username','firstname','lastname','email','password1','password2')




	def __init__(self,*args,**kwargs):
		super(RegisterUserForm, self).__init__(*args,**kwargs)


		self.fields['username'].widget.attrs['class'] = 'form-control'

		self.fields['password1'].widget.attrs['class'] = 'form-control'

		self.fields['password2'].widget.attrs['class'] = 'form-control'