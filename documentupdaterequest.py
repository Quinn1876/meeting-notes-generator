class Agenda:
  __agenda = []

  def __init__(self) -> None:
      pass

  def add_agenda_item(self, agenda_item):
    """
    agenda_item: Agenda() | string
    """
    if self is agenda_item:
      raise Exception("Cannot add self, to self")

    self.__agenda.append(agenda_item)

  def __str__(self) -> str:
      return '\t'.join([
        str(agenda_item) for agenda_item in self.__agenda
      ])

def insertText(start_index, text):
  return {
    "insertText": {
      "location": {
        "index": start_index
      },
      "text": text,
    }
  }

class DocumentUpdateRequest:
  __documentUpdateRequest = []
  __currentIndex = 0;

  def __init__(self, start_index) -> None:
      self.__currentIndex = start_index
      pass

  def add_document_header(self, header="Waterloop", subheader="Web team Spring 2021", document_type="Meeting Notes"):
    """
    # add_document_header
    Adds a three line header to the top of the document taking the form:

    header
    subheader
    document_type

    """

    start_index = self.__currentIndex
    ## Add header
    self.__documentUpdateRequest = [*self.__documentUpdateRequest,
      insertText(start_index, header),
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
                  "endIndex": start_index+len(header)
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
                        "endIndex": start_index+len(header)
                }
            }
        },
    ]

    start_index += len(header)

    ## Add sub header
    self.__documentUpdateRequest = [*self.__documentUpdateRequest,
        insertText(start_index, subheader),
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
                    "startIndex": start_index,
                    "endIndex": start_index+len(subheader)
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
                    "startIndex": start_index,
                    "endIndex": start_index+len(subheader)
                }
            }
        },
    ]

    start_index += len(subheader)

    ## Add document type
    self.__documentUpdateRequest = [*self.__documentUpdateRequest,
        insertText(start_index, document_type),
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
                    "startIndex": start_index,
                    "endIndex": start_index+len(document_type)
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
                    "startIndex": start_index,
                    "endIndex": start_index+len(document_type)
                }
            }
        },
    ]

    self.__currentIndex = start_index + len(document_type)

    pass

  def add_document_title(self, title="Jan 01, 00"):
    """
    The title of the document. For meeting notes, this is usually the date that the meeting takes place.
    Otherwise, this could be anything.
    """
    pass

  def add_meeting_details(self, time="00:00h EDT", location="E5/online", purpose="Enter Purpose Here", relevent_docs=[]):
    pass

  def add_meeting_attendees(self, facilitator="", noteTaker="", attendees=[]):
    pass

  def add_agenda(self, agenda=Agenda()):
    pass
