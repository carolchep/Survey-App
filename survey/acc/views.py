from django.shortcuts import render
from django.db import transaction
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Create your views here.


@login_required

def create(request):

    """User creating a new survey"""

    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey.creator = request.user
            survey.save()
            return redirect("survey-edit", pk=survey.id)
    else:
        form = SurveyForm()


    return render(request, "survey/create.html", {"form": form})

@login_required

def survey_list(request):

    """User can view all their surveys"""
    surveys = Survey.objects.filter(creator=request.user).order_by("-created_at").all()
    return render(request, "survey/list.html", {"surveys": surveys}

@login_required
def delete(request, pk):

    """User can delete an existing survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        survey.delete()


    return redirect("survey-list")

@login_required

def question_create(request, pk):
    """User can add a question to a draft survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect("survey-option-create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()


    return render(request, "survey/question.html", {"survey": survey, "form": form})

@login_required

def option_create(request, survey_pk, question_pk):
    """User can add options to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            option.save()
    else:
        form = OptionForm()


    options = question.option_set.all()
    return render(
        request,
        "survey/options.html",
        {"survey": survey, "question": question, "options": options, "form": form},
    )


def text_create(request, survey_pk, question_pk):
    """User can add textfield to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            textfi = form.save(commit=False)
            textfi.question_id = question_pk
            textfi.save()
    else:
        form = TextForm()


    textfis = question.Textfield_set.all()
    return render(
        request,
        "survey/text.html",
        {"survey": survey, "question": question, "textfis": textfis, "form": form},
    )
def float_create(request, survey_pk, question_pk):
    """User can add floatypes to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = FloatForm(request.POST)
        if form.is_valid():
            floatt = form.save(commit=False)
            floatt.question_id = question_pk
            floatt.save()
    else:
        form =FloatForm()


    floatts = question.Float_set.all()
    return render(
        request,
        "survey/float.html",
        {"survey": survey, "question": question, "Floatts": floatts, "form": form},
    )

@login_required

def detail(request, pk):
    """User can view an  survey"""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user
        )
    except Survey.DoesNotExist:
        raise Http404()


    questions = survey.question_set.all()

    
    for question in questions:
        option_pks = question.option_set.values_list("pk", flat=True)
        total_answers = Answer.objects.filter(option_id__in=option_pks).count()
        for option in question.option_set.all():
            num_answers = Answer.objects.filter(option=option).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0


    host = request.get_host()
    public_path = reverse("survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = survey.submission_set.filter(is_complete=True).count()
    return render(
        request,
        "survey/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,

        },

@login_required

def edit(request, pk):
    """User can edit questions """
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except Survey.DoesNotExist:
        raise Http404()


    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-detail", pk=pk)
    else:
        questions = survey.question_set.all()
        return render(request, "survey/edit.html", {"survey": survey, "questions": questions})



def submit(request, survey_pk, sub_pk):

    """Survey-taker submit their completed survey."""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=survey_pk, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()


    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()


    questions = survey.question_set.all()
    options = [q.option_set.all() for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == "POST":

        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)

        if formset.is_valid():

        

                for form in formset:

                    Answer.objects.create(

                        option_id=form.cleaned_data["option"], submission_id=sub_pk,

                    )

