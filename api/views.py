from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api.serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice
from rest_framework import viewsets


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    choice_id = request.data['choice']

    return redirect('question-detail', question_id)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer




