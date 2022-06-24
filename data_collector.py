#! /usr/bin/env python3

# adapted from https://stackoverflow.com/questions/52899174/real-time-ocr-in-python

import time
import logging
import sys
import pytesseract
import PIL
from PIL import Image
from difflib import SequenceMatcher

# Import ImageGrab if possible, might fail on Linux
try:
    from PIL import ImageGrab
    use_grab = True
except Exception as ex:
    # Some older versions of pillow don't support ImageGrab on Linux
    # In which case we will use XLib 
    if ( sys.platform == 'linux' ):
        from Xlib import display, X   
        use_grab = False
    else:
        raise ex


def screenGrab( rect ):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Handles a Linux installation with and older Pillow by falling-back
        to using XLib """
    global use_grab
    x, y, width, height = rect

    if ( use_grab ):
        image = PIL.ImageGrab.grab( bbox=[ x, y, x+width, y+height ] )
    else:
        # ImageGrab can be missing under Linux
        dsp  = display.Display()
        root = dsp.screen().root
        raw_image = root.get_image( x, y, width, height, X.ZPixmap, 0xffffffff )
        image = Image.frombuffer( "RGB", ( width, height ), raw_image.data, "raw", "BGRX", 0, 1 )
        # DEBUG image.save( '/tmp/screen_grab.png', 'PNG' )
    return image


### Do some rudimentary command line argument handling
### So the user can speicify the area of the screen to watch
if ( __name__ == "__main__" ):
    EXE = sys.argv[0]
    del( sys.argv[0] )

    # EDIT: catch zero-args
    if ( len( sys.argv ) != 4 or sys.argv[0] in ( '--help', '-h', '-?', '/?' ) ):  # some minor help
        sys.stderr.write( EXE + ": monitors section of screen for text\n" )
        sys.stderr.write( EXE + ": Give x, y, width, height as arguments\n" )
        sys.exit( 1 )

    # TODO - add error checking
    x      = int( sys.argv[0] )
    y      = int( sys.argv[1] )
    width  = int( sys.argv[2] )
    height = int( sys.argv[3] )

    # Area of screen to monitor
    screen_rect = [ x, y, width, height ]  
    print( EXE + ": watching " + str( screen_rect ) )

    # show region to be recorded
    image = screenGrab( screen_rect )
    image.show()

    ### Loop forever, monitoring the user-specified rectangle of the screen
    logging.basicConfig(format='%(message)s',filename='data_collector_logfile.log',level=logging.DEBUG)
    elapsed_time=0
    counter=0 #counts up to 3 or 4, so it only saves the 4th consecutive detected image
    time_lim_secs=10000000
    last_text,simm_texts='',[]
    def similarity(a,b):
        return SequenceMatcher(None,a,b).ratio()
    def most_common(lst):
        return max(set(lst), key=lst.count)
    while (elapsed_time<time_lim_secs):
        image = screenGrab( screen_rect )              # Grab the area of the screen
        text  = pytesseract.image_to_string(image)   # OCR the image  #config='--psm 7'

        # IF the OCR found anything, write it to stdout.
        text = text.strip()
        if len(text)>0:
            if similarity(last_text,text)>=0.5:
                simm_texts.append(text)
                if counter==8:
                    out_text=most_common(simm_texts)
                    tm=int(time.time())
                    logging.info(str(tm)+', '+out_text.replace('\n',' '))
                    print(str(tm)+', '+out_text.replace('\n',' '))
                #if counter==4:
                #    image.save('images/6-9/'+str(int(tm))+'.png',"PNG")
                counter+=1
            else:
                simm_texts=[]
                last_text=text
                counter=0
        else:
            simm_texts=[]
            last_text=text
            counter=0
        
#        print(text)
        time.sleep(0.5)
        elapsed_time+=1 #this is not exact
