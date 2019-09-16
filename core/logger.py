import logging
import datetime
from .utils import makeDir, indent

# remote_addr
class logger():
  
  @staticmethod
  def insertLog(tilte='', message=''):    
    makeDir(subpath='log')
    filename = 'log_%s' %(datetime.datetime.now().strftime("%Y%m%d"))
    template = './log/%s.log' %(filename)

    if not tilte:
      tilte = ''

    # amount = 4
    # ch=' '
    # padding = amount * ch
    # message = ''.join(padding+line for line in message.splitlines(True))
    message = indent(message, 4)

    time = datetime.datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
    strTitle = 'Log Time: %s\n%s\n%s\n' %(time, tilte, message)

    logger = logging.getLogger()
    if not (logger.hasHandlers()):
      handle = logging.FileHandler(template, 'a', 'utf8')
      
      if not (handle):
        file_handler = logging.FileHandler(template, 'w', 'utf8')
        logger.addHandler(file_handler)
      else:
        logger.addHandler(handle)

    logger.setLevel(logging.INFO)
    logger.info(strTitle)

  