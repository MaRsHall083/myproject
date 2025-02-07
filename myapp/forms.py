from django import forms
from .models import Question, Answer

class NameForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'] = forms.ModelChoiceField(
            queryset=Answer.objects.filter(question=question),
            widget=forms.RadioSelect,
            empty_label=None
        )