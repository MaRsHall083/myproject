from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Question, Answer, Result
from .forms import NameForm, AnswerForm


def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['name'] = form.cleaned_data['name']
            request.session['question_index'] = 0
            request.session['result_id'] = Result.objects.create(name=form.cleaned_data['name']).id
            return redirect('question')
    else:
        form = NameForm()
    return render(request, 'myapp/index.html', {'form': form})


def question(request):
    question_index = request.session.get('question_index', 0)
    questions = Question.objects.all()
    if question_index >= len(questions):
        return redirect('results')

    question = questions[question_index]
    if request.method == 'POST':
        form = AnswerForm(request.POST, question=question)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            result = Result.objects.get(id=request.session['result_id'])
            setattr(result, f'scale_{answer.scale}', getattr(result, f'scale_{answer.scale}') + 1)
            result.save()
            request.session['question_index'] = question_index + 1

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'next_url': reverse('question')  # URL для следующего вопроса
                })

            return redirect('question')
    else:
        form = AnswerForm(question=question)
    return render(request, 'myapp/question.html', {'form': form, 'question': question})


def results(request):
    result = Result.objects.get(id=request.session['result_id'])
    return render(request, 'myapp/results.html', {'result': result})