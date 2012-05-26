from django import forms

class AssignmentCreateForm(forms.Form):
	assg_title = forms.CharField(max_length=60, label='Assignment Title', required=True, widget=forms.TextInput(attrs={'size':'53'}))
	assg_details = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':'6','cols':'40'}), label='Assignment Instructions', required=True)
	
class QuestionUploadForm(forms.Form):
	question = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows':'6','cols':'40'}), required=True, label='Question')
	ques_hint = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows':'2','cols':'40'}), required=False, label='Hint')
	ques_file = forms.FileField(label='File <span style="font-size:14px;">(If Any) (Max: 5MB)</style>', required=False)