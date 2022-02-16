from config import GOOGLE_DOCS_TEST_FILE_ID, GOOGLE_DOCS_WEB_NOTES
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pprint import pprint

"""
Helpful links for understanding this script:
https://developers.google.com/docs/api/reference/rest

"""

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# The ID of a sample document.
DOCUMENT_ID = GOOGLE_DOCS_WEB_NOTES

class NamedStyleTypes:
    HEADING_1 = "HEADING_1"
    HEADING_2 = "HEADING_2"
    NORMAL_TEXT = "NORMAL_TEXT"


class ParagraphStyles:
    alignment = "alignment"
    namedStyleType = "namedStyleType"

class Paragraph:
    def __init__(self) -> None:
        self.text = ""
        self.paragraphStyles= []
        pass

    def addParagraphStyle(self):
        pass

def generate_meeting_notes(term, year, members, task_list, slideshow_link):
    """
    term: string
    year: number
    members: string[]
    task_list: string[]
    slideshow_link: string
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    # pprint(document.get("body"))
    start_index = document.get("body")["content"][1]["startIndex"]
    waterloop_text = "Waterloop\n"
    meeting_name = f"Web team {term} {year}\n"
    meeting_notes_text = "Meeting Notes\n"
    month = "June" ## TODO: Get this somehow
    day = 16        ## TODO: Get this somehow
    meeting_title = f"{month} {day}, {year}\n"
    heading_length = len(waterloop_text)+len(meeting_name)+len(meeting_notes_text)+len(meeting_title)
    heading_requests = [
            {
                "insertText": {
                    "location": {
                        "index": start_index
                    },
                    "text": waterloop_text
                }
            },
            {
                "updateTextStyle": {
                    "textStyle": {
                        "bold": True,
                        "fontSize": {
                            "magnitude": 16,
                            "unit": 'PT'
                        },
                        "weightedFontFamily": {
                            "fontFamily": "IBM Plex Sans",
                            "weight": 400
                        }
                    },

                    "fields": "bold,fontSize, weightedFontFamily",
                    "range": {
                        "startIndex": start_index,
                        "endIndex": start_index+len(waterloop_text)
                    }
                }
            },
            {
                "updateParagraphStyle": {
                    "paragraphStyle": {
                        "alignment": "CENTER"
                    },
                    "fields": "alignment",
                    "range": {
                        "startIndex": start_index,
                            "endIndex": start_index+len(waterloop_text)
                    }
                }
            },
            {
                "insertText": {
                    "location": {
                        "index": start_index+len(waterloop_text)
                    },
                    "text": meeting_name
                }
            },
            {
                "updateTextStyle": {
                    "textStyle": {
                        "bold": True,
                        "fontSize": {
                            "magnitude": 11,
                            "unit": 'PT'
                        },
                        "weightedFontFamily": {
                            "fontFamily": "IBM Plex Sans",
                            "weight": 400
                        },
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.23,
                                    "green": 0.24,
                                    "blue": 0.38
                                }
                            }
                        }
                    },
                    "fields": "bold,fontSize,foregroundColor, weightedFontFamily",
                    "range": {
                        "startIndex": start_index+len(waterloop_text),
                        "endIndex": start_index+len(waterloop_text)+len(meeting_name)
                    }
                }
            },
            {
                "updateParagraphStyle": {
                    "paragraphStyle": {
                        "alignment": "CENTER"
                    },
                    "fields": "alignment",
                    "range":{
                        "startIndex": start_index+len(waterloop_text),
                        "endIndex": start_index+len(waterloop_text)+len(meeting_name)
                    }
                }
            },
            {
                "insertText": {
                    "location": {
                        "index": start_index+len(waterloop_text)+len(meeting_name)
                    },
                    "text": meeting_notes_text
                }
            },
            {
                "updateTextStyle": {
                    "textStyle": {
                        "bold": False,
                        "fontSize": {
                            "magnitude": 11,
                            "unit": 'PT'
                        },
                        "weightedFontFamily": {
                            "fontFamily": "IBM Plex Sans",
                            "weight": 400
                        },
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    "red": 0,
                                    "green": 0,
                                    "blue": 0
                                }
                            }
                        }
                    },
                    "fields": "bold,fontSize,foregroundColor,weightedFontFamily",
                    "range": {
                        "startIndex": start_index+len(waterloop_text)+len(meeting_name),
                        "endIndex": start_index+len(waterloop_text)+len(meeting_name)+len(meeting_notes_text)
                    }
                }
            },
            {
                "updateParagraphStyle": {
                    "paragraphStyle": {
                        "alignment": "CENTER"
                    },
                    "fields": "alignment",
                    "range":{
                        "startIndex": start_index+len(waterloop_text)+len(meeting_name),
                        "endIndex": start_index+len(waterloop_text)+len(meeting_name)+len(meeting_notes_text)
                    }
                }
            },
            {
                "insertText": {
                    "location": {
                        "index": start_index+len(waterloop_text)+len(meeting_name)+len(meeting_notes_text)
                    },
                    "text": meeting_title
                }
            },
            {
                "updateParagraphStyle": {
                    "paragraphStyle": {
                        "alignment": "CENTER",
                        "namedStyleType": "HEADING_1"
                    },
                    "fields": "alignment,namedStyleType",
                    "range":{
                        "startIndex": start_index+len(waterloop_text)+len(meeting_name)+len(meeting_notes_text),
                        "endIndex": start_index+len(waterloop_text)+len(meeting_name)+len(meeting_notes_text)+len(meeting_title)
                    }
                }
            }
        ]

    time_of_meeting = "7:00pm. EDT"
    details_heading_text = 'Details\n'
    time_text = "Time\t\t"
    time_value = f"{time_of_meeting}\n"
    location_text = "Location\t"
    location_value = "[in-person location if applicable];\n\t\tVideo call link in Calendar Event\n"
    purpose_text = "Purpose\t"
    purpose_value = "Review of work for the week\n"
    relevant_docs_text = "Relevant docs:\n"
    details_length = len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value)+len(purpose_text)+len(purpose_value)+len(relevant_docs_text)

    details_requests = [
        {
            "insertText": {
                "location": {
                    "index": start_index+heading_length
                },
                "text": details_heading_text
            }
        },
        {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "HEADING_2"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length,
                    "endIndex": start_index+heading_length+len(details_heading_text)
                }
            }
        },
        {
            "insertText": {
                "location": {
                    "index": start_index+heading_length+len(details_heading_text)
                },
                "text": time_text+time_value+location_text+location_value+purpose_text+purpose_value+relevant_docs_text
            }
        },
        {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "NORMAL_TEXT"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length+len(details_heading_text),
                    "endIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value)+len(purpose_text)+len(purpose_value)+len(relevant_docs_text)
                }
            }
        },
        {
            "updateTextStyle": {
                "textStyle": {
                    "bold": True,
                } ,
                "fields": "bold",
                "range": {
                    "startIndex": start_index+heading_length+len(details_heading_text),
                    "endIndex": start_index+heading_length+len(details_heading_text)+len(time_text)
                }
            }
        },
        {
            "updateTextStyle": {
                "textStyle": {
                    "bold": True,
                } ,
                "fields": "bold",
                "range": {
                    "startIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value),
                    "endIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)
                }
            }
        },
        {
            "updateTextStyle": {
                "textStyle": {
                    "bold": True,
                } ,
                "fields": "bold",
                "range": {
                    "startIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value),
                    "endIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value)+len(purpose_text)
                }
            }
        },
        {
            "updateTextStyle": {
                "textStyle": {
                    "bold": True,
                } ,
                "fields": "bold",
                "range": {
                    "startIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value)+len(purpose_text)+len(purpose_value),
                    "endIndex": start_index+heading_length+len(details_heading_text)+len(time_text)+len(time_value)+len(location_text)+len(location_value)+len(purpose_text)+len(purpose_value)+len(relevant_docs_text)
                }
            }
        }
    ]

    attendees_header = "Attendees\n"
    attendees_subsections = "Facilitator:\nNotetaker:\nAttendees:\n"
    attendees_length = len(attendees_header)+len(attendees_subsections)
    attendees_requests = [
        {
            "insertText": {
                "location": {
                    "index": start_index+heading_length+details_length
                },
                "text": attendees_header
            }
        },
        {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "HEADING_2"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length+details_length,
                    "endIndex": start_index+heading_length+details_length+len(attendees_header)
                }
            }
        },
        {
            "insertText": {
                "location": {
                    "index": start_index+heading_length+details_length+len(attendees_header)
                },
                "text": attendees_subsections
            }
        },
        {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "NORMAL_TEXT"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length+details_length+len(attendees_header),
                    "endIndex": start_index+heading_length+details_length+len(attendees_header)+len(attendees_subsections)
                }
            }
        },
        {
            "updateTextStyle": {
                "textStyle": {
                    "bold": True,
                } ,
                "fields": "bold",
                "range":{
                    "startIndex": start_index+heading_length+details_length+len(attendees_header),
                    "endIndex": start_index+heading_length+details_length+len(attendees_header)+len(attendees_subsections)
                }
            }
        },
    ]
    agenda_header_text = "Agenda\n"
    agenda_header = [
        {
            "insertText": {
                "location": {
                    "index": start_index+heading_length+details_length+attendees_length
                },
                "text": agenda_header_text
            }
        },
        {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "HEADING_2"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length+details_length+attendees_length,
                    "endIndex": start_index+heading_length+details_length+attendees_length+len(agenda_header_text)
                }
            }
        },
    ]

    agenda_items = [
        "Member Updates\n",
        "\n".join([f"\t{member}" for member in members]),
        "\n",
        "Tasks\n",
        "\n".join([f"\t{task}" for task in task_list]),
        "\n",
        "Adding to slideshow for this weekend\n",
        f"\tLink to the slideshow: {slideshow_link}"
    ]
    # Attempt to update the document
    update_body = {
        "requests": [
            {
                "insertPageBreak": {
                    "location": {
                        "index": start_index
                    }
                }
            },
            *heading_requests,
            *details_requests,
            *attendees_requests,
            *agenda_header,
            {
                "insertText": {
                    "location": {
                        "index": start_index+heading_length+details_length+attendees_length+len(agenda_header_text)
                    },
                    "text": "".join(agenda_items)
                }
            },
            {
                "createParagraphBullets": {
                    "range": {
                        "startIndex": start_index+heading_length+details_length+attendees_length+len(agenda_header_text),
                        "endIndex": start_index+heading_length+details_length+attendees_length+len(agenda_header_text)+(len("".join(agenda_items))),
                    },
                    "bulletPreset": "NUMBERED_UPPERROMAN_UPPERALPHA_DECIMAL",
                }
            },
            {
            "updateParagraphStyle": {
                "paragraphStyle": {
                    "alignment": "START",
                    "namedStyleType": "NORMAL_TEXT"
                },
                "fields": "alignment,namedStyleType",
                "range":{
                    "startIndex": start_index+heading_length+details_length+attendees_length+len(agenda_header_text),
                    "endIndex": start_index+heading_length+details_length+attendees_length+len(agenda_header_text)+(len("".join(agenda_items))),
                }
            }
        },

        ]
    }

    service.documents().batchUpdate(documentId=DOCUMENT_ID, body=update_body).execute()
    print('The title of the document is: {}'.format(document.get('title')))

if __name__ == "__main__":
    member_list=["Quinn", "Evan", "Joshua", "Hassan", "William", "Zeel", "Suvasan", "Steven", "Muhammad", "Kush", "Jeff Z"]
    task_list = ["Hello"]
    slideshow_link = "https://teamwaterloop.ca"
    generate_meeting_notes("spring", 2021, member_list, task_list, slideshow_link)
