from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from polls.models import Choice, Question


def index(request):
    # 데이터를 가장 최근인 자료 5개 가져욤
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    # 위의 과정을 통해서 가져온 데이터를 딕셔너리의 밸류로 전달.
    context = {'latest_question_list': latest_question_list}
    # html문서 렌더링 시 request, context를 html문서의 주소로 가져감.
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # results.html에 득표순으로 정렬하기 - 1 쿼리 만들기  
    reOrdering_list = Choice.objects.all().order_by('-votes')
    
    # results.html에 득표순으로 정렬하기 - 2 만든 쿼리를 딕셔너리로 템플릿에 전달하기 위해서 추가.
    return render(request, 'polls/results.html', {'reOrdering_list': reOrdering_list, 'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # choice_set 하나의 set을 만듬.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # votes 1씩 증가.
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    