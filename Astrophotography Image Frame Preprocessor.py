"""
This code is intented to sort and rate an series of astronomy image files
using measurable metrics in the filename, mainly the number of stars detected
and the half-flux-radius which is a measure of star eccentricity. The script
takes in three user inputs to define the index position of
the metrics used for the sorting process.

The inputs to this program are pre-specified in an .ini type configuration file which
must be present in the same directory as the program itself.

2024 Fabian Butkovich
"""

import os
import statistics
import logging
import configparser
import datetime

original_file_names = []
new_file_names = []
delimited_file_names = []
temperature_list = []
starcount_list = []
hfr_list = []
quality_rating = []

file_extensions = [
    "tif",
    "tiff",
    "dng",
    "jpg",
    "jpeg",
    "crw",
    "nef",
    "cr2",
    "raw",
    "cr3",
    "rw2",
    "png",
    "fits",
]

lists = [original_file_names, new_file_names, delimited_file_names,
         temperature_list, starcount_list, hfr_list, quality_rating]

rooterror = False
subfolder = ""

Config = configparser.ConfigParser()


class Logging:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def ConfigLogger(self, topfolder):
        # If the specified folder containing the image files doesn't exist in the working directory, create a log file at the root level
        if self.logger.level == 40 and rooterror:
            logging.basicConfig(filename=os.getcwd() + ".log",
                                format="%(message)s", filemode="w")
        else:
            logging.basicConfig(filename=os.path.join(
                os.getcwd(), topfolder + ".log"), format="%(message)s", filemode="w",)
        self.logger.info("Log file sucessfully created at: %s".ljust(
            10) % datetime.datetime.now())

    def ShowLogfileLocation(self, topfolder):
        if self.logger.level == 40 and rooterror:
            print(
                "Analysis failed with [1] error(s), results stored at '%s.log'" % os.getcwd())
        elif self.logger.level == 40:
            print("Analysis failed with [1] error(s), results stored at '%s\\%s.log'" % (
                os.getcwd(), topfolder))
        else:
            print("Analysis complete with [0] error(s), results stored at '%s\\%s.log'" % (
                os.getcwd(), topfolder))


# Instance of Logging class object
Report = Logging()


def find_mode(array):
    first_occ_value = 0
    index = 0
    freq = 0
    most_freq_vals = []
    for n in range(1, len(array)):
        if array[n] == array[n - 1]:
            first_occ_value = array[n]
            most_freq_vals.append(array[n - 1])
        else:
            index = n
        if n > 1:
            break
    for n in range(index - 1, len(array)):
        if array[n] == first_occ_value:
            most_freq_vals.append(array[n])
    freq = len(most_freq_vals)
    return [first_occ_value, freq]


def index_defined(i):
    try:
        Config.getint(Config.sections()[i], 'index')
    except ValueError:
        return False
    else:
        return True


def duplicate_indexes():
    config_file_indexes = []
    for i in range(len(Config.sections())):
        if index_defined(i):
            config_file_indexes.append(Config.getint(Config.sections()[i], 'index'))
    config_file_set = set(config_file_indexes)
    if len(config_file_indexes) != len(config_file_set):
        return True
    else:
        return False


def generate_new_filename(i):
    temp_string = ""
    # First build filename up until the end of the original name
    for x in range(len(new_file_names[i])):
        if x < len(delimited_file_names[i]) - 1:
            temp_string = temp_string + delimited_file_names[i][x] + "_"
        # See if HFR metric (or any floating point number) is at the end of the filename before the file extension, if it is then remove it
        elif len(delimited_file_names[i][len(delimited_file_names[i]) - 1].split(".")) > 2:
            temp_string = temp_string + delimited_file_names[i][x].split(
                "." + delimited_file_names[i][len(delimited_file_names[i]) - 1].split(".")[2])[0] + "_"
        else:
            temp_string = temp_string + delimited_file_names[i][x].split(
                "." + delimited_file_names[i][len(delimited_file_names[i]) - 1].split(".")[1])[0] + "_"
    # Add quality rating and 4-digit serial number to the end of the new filename
    # See if HFR metric (or any floating point number) is at the end of the filename before the file extension, if it is then remove it
    if len(delimited_file_names[i][len(delimited_file_names[i]) - 1].split(".")) > 2:
        temp_string = temp_string + f"{quality_rating[i]}_" + f"{i:04}." + \
            delimited_file_names[i][len(
                delimited_file_names[i]) - 1].split(".")[2]
    else:
        temp_string = temp_string + f"{quality_rating[i]}_" + f"{i:04}." + \
            delimited_file_names[i][len(
                delimited_file_names[i]) - 1].split(".")[1]
    return temp_string


def sort_and_rename_files(subdirectory, subfolder):
    global original_file_names, delimited_file_names, new_file_names
    n = len(original_file_names)
    currdir = currdir = os.path.join(os.getcwd(), subdirectory)
    if subfolder:
        currdir = os.path.join(os.getcwd(), subdirectory, subfolder)

    for i in range(n):
        # First append the new file names array with empty placeholder arrays to store the applicable sections in the config.ini
        new_file_names.append([])
        # Append a section to array only if it's index position has been defined in config.ini, this leaves the actual index
        # position of a given section incorrect
        for x in range(len(Config.sections())):
            if index_defined(x):
                new_file_names[i].append(Config.sections()[x])
    
    # Unused
    '''   
    # See if there is an additional user specified value in the config file that does not currently have a place in the original file name, 
    # if so, append it to the delimited_file_names list
    if len(Config.sections()) > len(delimited_file_names[0]):
        config_file_indexes = []
        original_filename_indexes = []
        for j in range(len(Config.sections())):
            if index_defined(j):
                config_file_indexes.append(
                    Config.getint(Config.sections()[j], 'index'))
        for p in range(len(delimited_file_names[0])):
            original_filename_indexes.append(p)
        # Find out which index from the config file is missing
        for m in delimited_file_names:
            for x in config_file_indexes:
                if x not in original_filename_indexes:
                    for u in range(len(Config.sections())):
                        if index_defined(u):
                            if Config.getint(Config.sections()[u], 'index') == x:
                                m.append(Config.get(
                                    Config.sections()[u], 'value'))
    '''

    p = len(new_file_names[0])

    # Sort index positions of stored sections in array to actual user defined index in config.ini
    for i in range(n):
        already_sorted = True
        for j in range(p - i - 1):
            if Config.getint(new_file_names[i][j], 'index') > Config.getint(new_file_names[i][j + 1], 'index'):
                for x in new_file_names:
                    x[j], x[j + 1] = x[j + 1], x[j]
                already_sorted = False
        if already_sorted:
            break

    # Bubble sort array method which compares the value of the next
    # element in the array with the current index
    for i in range(n - 1):
        already_sorted = True
        for j in range(n - i - 1):
            # Can also sort by other arrays such as starcount or hfr value
            if quality_rating[j] > quality_rating[j + 1]:
                for x in lists:
                    x[j], x[j + 1] = x[j + 1], x[j]
                already_sorted = False
        if already_sorted:
            break

    for i in range(n):
        ReconstructedString = generate_new_filename(i)
        # Check if the filepath exists first before renaming file
        if os.path.exists(os.path.join(currdir, original_file_names[i])):
            os.rename(os.path.join(currdir, original_file_names[i]), os.path.join(
                currdir, ReconstructedString))
            Report.logger.info(ReconstructedString)


def parse_image_files(subdirectory, subfolder, starcountindex, hfrindex, usertempindex):
    global delimited_file_names, starcount_list, temperature_list, hfr_list, quality_rating, rooterror
    Report.logger.info("IMAGE FILENAME PARAMETERS".ljust(10))
    errorindex = 0
    try:
        for x in delimited_file_names:
            tempindex = 0
            temperature = 0
            starcount = 0
            hfr = 0
            for n in x:
                if "c" in n:
                    tempindex = x.index(n)
                    break
                else:
                    tempindex = usertempindex
            temperature = float(x[tempindex].split("c")[0])
            if "." in x[starcountindex]:
                starcount = int(x[starcountindex].split(".")[0])
            else:
                starcount = int(x[starcountindex])
            # If the hfr_list metric was appended to the end of the filename, then remove the file extension and retrieve just the number
            if x[hfrindex].count(".") > 1:
                hfr = float(x[hfrindex].split(
                    "." + x[len(x) - 1].split(".")[2])[0])
            else:
                hfr = float(x[hfrindex])
            temperature_list.append(temperature)
            starcount_list.append(starcount)
            hfr_list.append(hfr)
            Report.logger.info("#Stars:%s,Temperature:%s,HFR:%s" %
                               (starcount, temperature, hfr))
        for n in range(len(delimited_file_names)):
            if hfr_list[n] > 0:
                # Quality rating is a simple dividen which is strongly influced by the hfr_list value, other formulas could be used
                # to factor both a high star count and low hfr_list into account
                quality_rating.append(
                    round(starcount_list[n] / hfr_list[n], 2))
            else:
                quality_rating.append(0.00)
    except ValueError:
        Report.logger.setLevel(logging.ERROR)
        errorindex = delimited_file_names.index(x)
    except IndexError:
        Report.logger.setLevel(logging.ERROR)
        errorindex = delimited_file_names.index(x)
    finally:
        output_logging(subdirectory, errorindex, subfolder)


def parse_folders():
    global rooterror
    files = 0
    for _, dirnames, filenames in os.walk(os.path.join(os.getcwd(), topfolder)):
        files += len(filenames)
    if files != 0:
        for filename in os.listdir(topfolder):
            if filename.split(".")[len(filename.split(".")) - 1].lower() in file_extensions:
                original_file_names.append(filename)
                delimited_file_names.append(filename.split("_"))
            else:
                rooterror = True
                Report.logger.setLevel(logging.ERROR)
                Report.ConfigLogger(topfolder)
        parse_image_files(topfolder, subfolder, Config.getint('STARCOUNT', 'index'), Config.getint(
            'HFR', 'index'), Config.getint('SENSORTEMP', 'index'))
    else:
        Report.logger.setLevel(logging.ERROR)
        Report.ConfigLogger(topfolder)
        Report.logger.error("ERROR: Specified folder path '%s\\%s' contains no image files" % (
            os.getcwd(), topfolder))


def output_logging(subdirectory, errorindex, subfolder):
    if Report.logger.level == 20:
        sort_and_rename_files(subdirectory, subfolder)
        seconds = 0
        for i in range(len(original_file_names)):
            seconds += float(delimited_file_names[0][Config.getint(
            'EXPOSURETIME', 'index')].split('s')[0])
        hours = seconds / 60 / 60
        Report.logger.info("IMAGE ANALYSIS STATISTICS".ljust(10))
        Report.logger.info("Total number of frames: %d" %
                           len(original_file_names))
        Report.logger.info("Min temperature among frames: %3.1fc" %
                           min(temperature_list))
        Report.logger.info("Max temperature among frames: %3.1fc" %
                           max(temperature_list))
        Report.logger.info("Mean temperature among frames: %3.1fc" %
                           statistics.mean(temperature_list))
        Report.logger.info("Median temperature among frames: %3.1fc" %
                           statistics.median(temperature_list))
        Report.logger.info("Mode temperature among frames by first occurence: %3.1fc, frequency: %d" % (
            find_mode(temperature_list)[0], find_mode(temperature_list)[1]))
        Report.logger.info(
            "Min # of stars detected among frames: %d" % min(starcount_list))
        Report.logger.info(
            "Max # of stars detected among frames: %d" % max(starcount_list))
        Report.logger.info("Mean # of stars detected among frames: %d" %
                           statistics.mean(starcount_list))
        Report.logger.info("Median # of stars detected among frames: %d" %
                           statistics.median(starcount_list))
        Report.logger.info("Mode # of stars detected among frames by first occurence: %d, frequency: %d" % (
            find_mode(starcount_list)[0], find_mode(starcount_list)[1]))
        Report.logger.info(
            "Min half-flux radius detected among frames: %3.1f" % min(hfr_list))
        Report.logger.info(
            "Max half-flux radius detected among frames: %3.1f" % max(hfr_list))
        Report.logger.info(
            "Mean half-flux radius detected among frames: %3.1f" % statistics.mean(hfr_list))
        Report.logger.info(
            "Median half-flux radius detected among frames: %3.1f" % statistics.median(hfr_list))
        Report.logger.info("Mode half-flux radius detected among frames by first occurence: % 3.1f, frequency: %d" %
                           (find_mode(hfr_list)[0], find_mode(hfr_list)[1]))
        Report.logger.info(
            "Cumulative exposure time among frames: %3.1fh" % hours)
    else:
        try:
            Report.logger.setLevel(logging.ERROR)
            Report.logger.error(">>>%s" % original_file_names[errorindex])
            Report.logger.error(
                "ERROR: Issue while parsing filenames for valid parameters. Please verify image files are supported or \nthe specified index locations are correct")
        except IndexError:
            Report.logger.error("ERROR: No files with supported extension types found within the current working directory '%s\\%s'" % (
                os.getcwd(), topfolder))


try:
    topfolder = input(
        "ENTER FOLDER NAME WITHIN THIS WORKING DIRECTORY TO PERFORM ASTROPHOTOGRAPHY FRAME ANALYSIS ON>>")
    Report.ConfigLogger(topfolder)
    os.listdir(topfolder)
except FileNotFoundError:
    rooterror = True
    Report.logger.setLevel(logging.ERROR)
    Report.ConfigLogger(topfolder)
    Report.logger.error("ERROR: Could not locate the specified path '%s\\%s' within the current working directory" % (
        os.getcwd(), topfolder))
else:
    if os.path.isfile("F:\\Astrophotography Shared\\config.ini"):
        try:
            Config.read("F:\\Astrophotography Shared\\config.ini")
        except configparser.DuplicateSectionError:
            Report.logger.setLevel(logging.ERROR)
            Report.logger.error(
                "ERROR: Configuration file contains duplicate sections, please correct")
        except configparser.NoSectionError:
            Report.logger.setLevel(logging.ERROR)
            Report.logger.error(
                "ERROR: Configuration file contains no sections, please correct")
        else:
            if duplicate_indexes() == True:
                Report.logger.setLevel(logging.ERROR)
                Report.logger.error(
                    "ERROR: Configuration file contains duplicate index values, please correct")
            elif duplicate_indexes() == False:
                parse_folders()
    else:
        Report.logger.setLevel(logging.ERROR)
        Report.ConfigLogger(topfolder)
        Report.logger.error("ERROR: Missing 'config.ini at root directory path '%s\\%s'" % (
            os.getcwd(), topfolder))


Report.ShowLogfileLocation(topfolder)
userinput = input("Press [ENTER] to exit")
