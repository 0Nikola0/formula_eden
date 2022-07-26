from formula_app.models import Poraka


# Bez ovoa e napraeno za sea
class PorakaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(PorakaForm, self).__init__(*args, **kwargs)
		self.fields['sender'].queryset = User.objects.filter(pk = user.id)

	class Meta:
		model = Poraka
		# fields = '__all__'
		fields = ("message", "sender")
		# exclude = ('sender',)




# class PorakaForm(forms.ModelForm):
# 	class Meta:
# 		model = Poraka
# 		# fields = '__all__'
# 		fields = ("message",)
# 		# exclude = ('sender',)
