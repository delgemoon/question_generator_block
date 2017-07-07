
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint
# from googleapiclient import discovery

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None




# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'google_sheets_client_secret.json'
APPLICATION_NAME = 'Google Sheets API'

# CLIENT_SECRET_FILE = '/edx/app/edxapp/google-credentials/service_account.json'
# APPLICATION_NAME = 'Drive API Python Quickstart'
# SCOPES = ['https://www.googleapis.com/auth/drive']



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    # credential_path = os.path.join(credential_dir,
    #                                'google_sheets_client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_credentials_web_service():

    # SCOPES = ['https://www.googleapis.com/auth/drive']

    # CLIENT_SECRET_FILE = '/edx/app/edxapp/google/MOOC-fb91d4f340e0.json'
    # CLIENT_SECRET_FILE = 'service_account.json'
    # APPLICATION_NAME = 'Drive API Python Quickstart'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes=SCOPES)
    #http_auth = credentials.authorize(httplib2.Http())

    return credentials


class gsheets():
    def check_answer(self, teacher_answer, student_answer):

        print('Raw teacher answer:' + teacher_answer)
        print('Raw student answer:' + student_answer)

        # format answer input strings:
        teacher_answer = teacher_answer.replace(' ','')     # get rig of space character
        teacher_answer_list = teacher_answer.split('=')
        teacher_answer = '=' + teacher_answer_list[-1]

        student_answer = student_answer.replace(' ', '')    # get rig of space character
        student_answer_list = student_answer.split('=')
        student_answer = '=' + student_answer_list[-1]

        print('Expected teacher answer:' + teacher_answer)
        print('Expected student answer:' + student_answer)

        # create a new spreadsheet to store data
        # spreadsheet_body = {
        #     # TODO: Add desired entries to the request body.
        # }

        # credentials = get_credentials()
        credentials = get_credentials_web_service()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        spreadsheet_body = {
            "properties": {
                "title": "Problem Grading Template",
                "locale": "en_US",
                "autoRecalc": "ON_CHANGE",
                "timeZone": "Asia/Jakarta"
            }
        }

        request = service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()
        print('Answer template file:')
        pprint(response)

        sheets = response['sheets']
        for s in sheets:
            properties = s['properties']
            break

        # Update answer data to the newly created spreadsheets, Sheet1
        title = properties['title']
        spreadsheet_id = response["spreadsheetId"]
        rangeName = title + "!A2:B2"
        body = {
            "range": rangeName,
            "majorDimension": 'ROWS',
            "values": [
                [teacher_answer, student_answer]
            ],
        }
        # call REST API to update spreadsheets
        request = service.spreadsheets().values().update(
            spreadsheetId = spreadsheet_id,
            range=rangeName,
            valueInputOption = 'USER_ENTERED',
            body = body
        )
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        # print('Updated answer inputs:')
        # pprint(response)

        # Get answer's value to compare

        # The A1 notation of the values to retrieve.
        range_ = rangeName  # TODO: Update placeholder value.

        # How values should be represented in the output.
        # The default render option is ValueRenderOption.FORMATTED_VALUE.
        value_render_option = 'UNFORMATTED_VALUE'  # TODO: Update placeholder value.

        # How dates, times, and durations should be represented in the output.
        # This is ignored if value_render_option is
        # FORMATTED_VALUE.
        # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
        date_time_render_option = 'FORMATTED_STRING'  # TODO: Update placeholder value.

        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_,
                                                      valueRenderOption=value_render_option,
                                                      dateTimeRenderOption=date_time_render_option)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        print('Get answer output values to compare:')
        pprint(response)

        # extract values to compare
        teacher_answer_value = response['values'][0][0]
        student_answer_value = response['values'][0][1]
        pprint(teacher_answer_value)
        pprint(student_answer_value)

        if student_answer_value == teacher_answer_value:
            print('Correct')
            return True
        else:
            print('Inccorrect')

        return False



def main():

    # import json
    #
    # from httplib2 import Http
    #
    # from oauth2client.service_account import ServiceAccountCredentials
    # from apiclient.discovery import build
    #
    # scopes = ['https://www.googleapis.com/auth/sqlservice.admin']
    #
    # CLIENT_SECRET_FILE = 'edx-project-24663c21e3f6.json'
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(
    #     CLIENT_SECRET_FILE, scopes)
    #
    # sqladmin = build('sqladmin', 'v1beta3', credentials=credentials)
    # response = sqladmin.instances().list(project='examinable-example-123').execute()
    #
    # print
    # response

    # import oauth2client.service_account
    #
    # jsonfile = 'edx-project-24663c21e3f6.json'
    # # use static method .from_json_keyfile_name(filename)
    # credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(jsonfile)


    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    # credentials = get_credentials()
    #
    # print('Credentials 2:')
    # pprint(credentials)
    #
    # http = credentials.authorize(httplib2.Http())
    # discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
    #                 'version=v4')
    # service = discovery.build('sheets', 'v4', http=http,
    #                           discoveryServiceUrl=discoveryUrl)

    # spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    # rangeName = 'Class Data!A2:E'
    # # spreadsheetId = '1uQfNkOefkDBHFIPsa_I-Bo8VgLzUPOu4faaEhLk0hT8'
    # # rangeName = 'Answer!A2:E'
    # result = service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId, range=rangeName).execute()
    # values = result.get('values', [])
    #
    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))
    #
    # print('Creating new spreadsheet.')
    # spreadsheet_body = {
    #     # TODO: Add desired entries to the request body.
    # }
    #
    # request = service.spreadsheets().create(body=spreadsheet_body)
    # response = request.execute()
    # # TODO: Change code below to process the `response` dict:
    # pprint(response)

    print('Calling Google Spreadsheets to evaluate student answer...')
    sheets = gsheets()
    teacher_answer = 'x=sum(3,9)'
    student_answer = 'x = 12'
    sheets.check_answer(teacher_answer,student_answer)




if __name__ == '__main__':
    main()
