#!/afs/csl.tjhsst.edu/students/2018/2018akotnana/Linear_Project/lin_proj/bin/python2.7

from __future__ import print_function
import linecache
from apiclient import errors
import httplib2
import os
import base64
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

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

def ListMessagesMatchingQuery(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id,q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except:
        print("bad")

def GetAttachments(service, user_id, msg_id, prefix=""):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    att_id=part['body']['attachmentId']
                    att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data=att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = prefix+part['filename']

                with open(path, 'w') as f:
                    f.write(file_data)
    except errors.HttpError, error:
        print(sys.exc_info())

def DeleteMessage(service, user_id, msg_id):
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print('Message with id: %s deleted successfully.' % msg_id)
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir, filenames):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)
    for filename in filenames:
        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)
        main_type=""
        sub_type=""
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    id = ""
    try:
        id = str(ListMessagesMatchingQuery(service, "me", query="from:aneesh.kotnana@gmail.com")[0]["id"])
    except:
        id = "none"
    
    if(id != "none"):
        GetAttachments(service, "me", id, "//afs//csl.tjhsst.edu//students//2018//2018akotnana//Linear_Project//ve//")
        print("saved image")

        os.system("./do.sh")

        files = os.listdir(".")
        filenames = []
        for each in files:
            if "output_" in each:
                filenames.append(each)
        SendMessage(service, "me", CreateMessageWithAttachment("kakbkys@gmail.com", "aneesh.kotnana@gmail.com", "data","data", "//afs//csl.tjhsst.edu//students//2018//2018akotnana//Linear_Project//ve//", filenames))
        print("sent")
        os.system("rm -rf output*.png")
        DeleteMessage(service, "me", id)

if __name__ == '__main__':
   while True:
       print("checking")
       try:
           main()
           time.sleep(10)
       except:
           PrintException()
