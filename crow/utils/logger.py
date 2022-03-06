import datetime
import traceback


def mylog(e):
    """
    General purpose function for writing errors to an external .txt file

    e: exception raised by Crow
    """
    debugfile = open("debug.txt", "a")
    debugfile.write("\n")
    debugfile.write(datetime.datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S") + " - " + str(e))
    debugfile.write("\n")
    debugfile.write(traceback.format_exc())
    debugfile.write("\n")
    debugfile.close()
