import uuid

class StatusCode():
  COD200 = 200
  COD201 = 201
  COD204 = 204
  COD400 = 400
  COD401 = 401
  COD403 = 403
  COD404 = 404
  COD500 = 500

class Message():
  SUCCESS = 'Success'
  FAILS = 'Fails'
  NOT_FOUND = 'Not Found'
  BAD_REQUEST = 'invalid request'
  NO_AUTHEN = 'UnAuthorized'
  NO_CONTENT = ''
  EXIST_DATA = 'User {0} already registered'
  NOT_EXIST = 'User {0} NOT registered'

class DateTimeFormart():

  DATETIME_FORMAT_YYYYMMDDHHMMSSF = '%Y%m%d%H%M%S%f'

  DATETIME_FORMAT_YYYYMMDD_HHMMSS = '%Y%m%d %H:%M:%S'

  DATETIME_FORMAT_YYYYMMDD = '%Y%m%d'


class BaseEnum():
  

  
