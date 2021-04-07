from django.shortcuts import render
from django.http import HttpResponse
# import PyPDF2
# import pdftotext
import io
from . import resume_parse
from .models import Candidate
from django.contrib import messages


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


def job_post(request):
    if request.method == 'GET':
        return render(request, 'poc/job_post_portal.html')
    elif request.method == 'POST':

        params = request.POST
        job_description_text = params['job-description']

        # do something with job description...
        print(job_description_text)

        candidate_set = Candidate.objects.all()
        match_percentage = []
        for candidate in candidate_set.iterator():
            cv = CountVectorizer()
            job_comparision_list = [candidate.skills, job_description_text]
            count_matrix = cv.fit_transform(job_comparision_list)
            matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
            matchPercentage = round(matchPercentage, 2)  # round to two decimal
            match_percentage.append(matchPercentage)

        result = zip(candidate_set, match_percentage)
        context = {'result': result}
        return render(request, 'poc/job_post_portal.html', context)


def candidate_portal(request):

    if request.method == 'GET':
        return render(request, 'poc/candidate_portal.html')

    elif request.method == 'POST':

        # candidate submitted a resume document
        if not len(request.FILES) == 0:
            params = resume_parse.parse_resume(request)

        # else candidate verified and submitted their information
        else:
            params = request.POST
            # ... do stuff with the params

            saverecord = Candidate()
            saverecord.first_name = params.get('first-name')
            saverecord.middle_name = params.get('middle-name')
            saverecord.last_name = params.get('last-name')
            saverecord.skills = params.get('skills')
            saverecord.email = params.get('email')

            # saverecord.degree = params.getlist(
            #    'degree.degree_type')
            # saverecord.field = params.getlist(
            #   'degree.field_of_study')

            saverecord.save()
            messages.success(request, "Record Saved Successfully...!")
            return render(request, 'poc/candidate_portal.html')

        return render(request, 'poc/candidate_portal.html', context=params)


def results(request):
    return HttpResponse("Results Page")
