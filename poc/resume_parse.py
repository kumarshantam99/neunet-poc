import json
import requests
from pathlib import Path
import io
import time


# gets the uploaded file and saves it in the uploads folder,
# then parses the document and returns the relevant information in a dictionary
def parse_resume(request):

    uploaded_file = request.FILES['resume-upload']

    print()

    # store the uploaded file in the uploads folder
    with open('poc/uploads/' + uploaded_file.name, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    filepath = Path("poc/uploads/" + uploaded_file.name)
    token = "55fdaf76b6be73d7db458617b021673252217e4d"
    headers = {"Authorization": f"Bearer {token}"}

    # use these two lines to send the uploaded file to affinda and use up a parsing token
    identifier = send_file_for_parsing(filepath, uploaded_file.name, headers)
    parsed_dict = retrieve_parsing_results(identifier, headers)

    # use these three lines instead of the previous two to use previous results instead of sending the new doc for parsing
    # identifiers = list_parsed_docs(headers)
    # print(identifiers)
    # parsed_dict = retrieve_parsing_results(identifiers[-1], headers)

    return get_relevant_info(parsed_dict)


# send resume to Affinda for parsing, and return the identifier for the job
def send_file_for_parsing(filepath, filename, headers):

    url = "https://resume-parser.affinda.com/public/api/v1/documents/"

    with open(filepath, "rb") as doc_file:
        response = requests.post(
            url,
            json={"fileName": filename},
            files={"file": doc_file},
            headers=headers,
        )

    print(response.json())

    return response.json()['identifier']


# retrieve the json data from Affinda for the resume with the supplied identifier
# save the json file in the resume_json folder and then return the data
def retrieve_parsing_results(identifier, headers):

    url = f"https://resume-parser.affinda.com/public/api/v1/documents/{identifier}"
    # initial request for the parsed data
    response = requests.get(url, headers=headers)

    # if the resume isn't finished being parsed
    while not response.json()['meta']['ready']:
        print('not ready, looping again')
        time.sleep(1)  # wait one second to check if the parsing is finished
        response = requests.get(url, headers=headers)

    response_json = response.json()

    with open("poc/resume_json/" + response_json['meta']['fileName'][:-4] + '.json', 'w') as outfile:
        json.dump(response_json, outfile)

    return response_json


# this function lists the identifiers for all the documents we have parsed before
def list_parsed_docs(headers):

    url = "https://resume-parser.affinda.com/public/api/v1/documents/"
    response = requests.get(url, headers=headers)

    # print(json.dumps(response.json()))

    identifiers = []
    for item in response.json()['results']:
        identifiers.append(item['identifier'])

    return identifiers


# this function takers the info returned from Affinda and returns the relevant stuff
def get_relevant_info(parsed_dict):

    data = parsed_dict['data']
    result = dict()

    if data['name']:
        result['first_name'] = data['name']['first']
        result['middle_name'] = data['name']['middle']
        result['last_name'] = data['name']['last']

    if data['dateOfBirth']:
        result['date_of_birth'] = data['dateOfBirth']

    if data['emails']:
        result['email'] = data['emails'][0]

    if data['phoneNumbers']:
        result['mobile_number'] = data['phoneNumbers'][0]

    if data['education']:
        result['degrees'] = []
        for item in data['education']:
            degree = dict(
                organization=item['organization'],
                degree_type=item['accreditation']['education'],
                field_of_study='',
                # grade=item['grade']['value'],
                # dates=item['dates']['completionDate']
            )
            result['degrees'].append(degree)

    if data['workExperience']:
        result['experience'] = []
        for item in data['workExperience']:
            exp = dict()

            if item['organization']:
                exp['organization'] = item['organization']

            if item['jobTitle']:
                exp['designation'] = item['jobTitle']

            if item['dates'] and item['dates']['monthsInPosition']:
                exp['duration'] = item['dates']['monthsInPosition']

            result['experience'].append(exp)

    if data['skills']:
        result['skills'] = ', '.join(data['skills'])

    if data['summary']:
        result['summary'] = data['summary']

    return result

    # return dict(

    #     # info that wont be used to rank candidates
    #     first_name='first_name',
    #     middle_name='',
    #     last_name='last_name',
    #     date_of_birth='11/03/1990',
    #     email='john@gmail.com',
    #     mobile_number='204-685-3458',

    #     # info that will be used to rank candidates
    #     degrees = [
    #         dict(
    #             degree_type='B.S.',
    #             field_of_study='Computer Science'
    #         ),
    #         dict(
    #             degree_type='M.S.',
    #             field_of_study='Computer Science'
    #         )
    #     ],
    #     experience=[
    #         dict(
    #             organization='Microsoft',
    #             designation='Software Engineer',
    #             duration='2'
    #         )
    #     ],
    #     skills='c++, Java, React, Tensorflow',
    #     awards='honor student 2020',
    #     summary='looking for software job'
    # )
