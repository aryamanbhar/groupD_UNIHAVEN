from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RatingForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    class Meta:
        model = Rating
        fields = ['accommodation', 'score', 'comment', 'is_anonymous', 'images']
        widgets = {
            'score': forms.Select(choices=[(i, '★'*i) for i in range(1, 6)]),
            'images': forms.ClearableFileInput(attrs={'multiple': True})
        }

    def __init__(self, user, *args, ​**kwargs):
        super().__init__(*args, ​**kwargs)
        self.fields['accommodation'].queryset = Accommodation.objects.filter(
            contract__user=user, 
            contract__status='signed'
        )
