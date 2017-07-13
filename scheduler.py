import threading, schedule, time, platform
import subprocess, sys
import locale
from schedule_UI_strings import ENG, RUS

"""
This module implements job scheduling. Each job consists of a directory to clean
and the age of files that the files should exceed in order to be deleted.
The sceduler.py module is intended to work permanently. It provides user interface
for managing the list of current jobs. In order to keep the job list consistent it is
backed up to a config.txt file on every operation that adds or deletes a job.

To perform date scheduling "schedule" library was used:
link: https://github.com/dbader/schedule
"""


LOG_FILE = "log.txt"
CONFIGS = "config.txt"
# a link to a dictionary that contains selected localisation strings
LOCALISATION_PKG = None

def job(*args):
    """
    A function that provide the functionality of a job. It accepts two arguments
    the path to the directory to be cleaned and the age of files to be deleted.
    """
    temp = args[1].split('\r')[0]
    print(LOCALISATION_PKG['starting_cleaning']+' ' + args[0]+ ' '+temp + '\n')
    try:
        f = open(LOG_FILE, "a")
        f.write('Starting cleaning ' + args[0]+ ' '+temp + '\n')
        f.close()
    except:
        pass
    try:	            #throws CalledProcessError if return value is not zero
        output = subprocess.check_output([sys.executable, "autodel.py", args[0], temp])
        try:
            f = open(LOG_FILE, "a")
            f.write(output.decode("utf-8"))
            f.close()
        except:
            pass
    except subprocess.CalledProcessError:
        global L
        #if directory hasnt been found - it will be deleted from the list
        L.delete(args[0])
        print(LOCALISATION_PKG['directory']+' '+args[0]+' '+LOCALISATION_PKG['not_found']+'\n')
        try:
            f = open(LOG_FILE, "a")
            f.write(LOCALISATION_PKG['directory']+' '+args[0]+' '+LOCALISATION_PKG['not_found']+'\n')
            f.close()
        except:
            pass

class Node:
    """ job list element """
    def __init__(self, direct, next, prev, ind):
        #number of the elem
        self.ind = ind
        self.next = next
        self.prev = prev
        pars = direct.split(' ')
        # age of files to be deleted
        self.file_age = pars[3]
        # the size of the interval between job calls
        self.time_count = pars[2]
        try:
            # time format (every hours/minutes/days)
            self.time_mode = (LOCALISATION_PKG['TIME_FORMAT'])[pars[1]]
        except:
            self.time_mode = pars[1]
        # directory for searching
        self.direct = pars[0]

def add_to_schedule(node):
    """ adds task to schedule """
    if node.time_mode == 'hours':
        schedule.every(interval=int(node.time_count)).hours.do(job, node.direct, node.file_age)
    if node.time_mode == 'minutes':
        schedule.every(interval=int(node.time_count)).minutes.do(job, node.direct, node.file_age)
    if node.time_mode == 'days':
        schedule.every(interval=int(node.time_count)).days.do(job, node.direct, node.file_age)

class List:
    """ Linked list of current job """
    def __init__(self):
        self.first = None
        self.last = None

    def str(self):
        """ string for a few purposes (print out or write to configuration file) """
        if self.first != None:
            current = self.first
            out = str(current.direct) + ' ' + str(current.time_mode) + ' ' + \
            str(current.time_count) + ' ' + str(current.file_age)
            while current.next != None:
                current = current.next
                # [directory] [time_mode] [time count] [how old file]
                out += '\n' + str(current.direct) + ' ' + str(current.time_mode) \
                + ' ' + str(current.time_count) + ' ' + str(current.file_age)
            return out
        return ''

    def clear(self):
        """ clears the list """
        self.init()

    def add(self, x):
        h = x.split(' ')[0]
        if self.search(h) == None:
            if self.first == None:
                temp = Node(x, None, None, 0)
                self.last = self.first = temp
                # add task to schedule
                add_to_schedule(temp)
            else:
                temp = Node(x, None, self.last, self.last.ind + 1)
                self.last.next = self.last = temp
                add_to_schedule(temp)
            # rewrite the configuration file
            self.writeTXT()
        else:
            print(LOCALISATION_PKG['double_directory_assertion'])

    def readTXT(self):
        """ read cleaning list from configuration file """
        f = open(CONFIGS, "r")
        for line in f:
            self.add(line.split('\n')[0])
        f.close()

    def writeTXT(self):
        """ write cleaning list to configuration file """
        f = open(CONFIGS, "w")
        f.write(self.str())
        f.close()

    def delete(self, x):
        """ deletes a job """
        elem = self.search(x)
        if elem:
            if elem.prev != None:
                elem.prev.next = elem.next
            else:
                self.first = elem.next
            if elem.next != None:
                elem.next.prev = elem.prev
            else:
                self.last = elem.prev
            # delete job from schedulers jobs list
            schedule.jobs.pop(elem.ind)
            # renumbering elements id
            self.indit(elem.next)
            self.writeTXT()

    def indit(self, V):
        """
        shifts the indexes after a node was deleted in order
        to keep job list consistent with schedule.jobs list.
        """
        if V != None:
            t = V.ind
            V.ind = V.ind - 1
            temp = V.next
            while temp != None:
                temp.ind = t
                t = t + 1
                temp = temp.next

    def search(self,x):
        """ search a job in list """
        temp = self.first
        while temp != None:
            if temp.direct == x:
                return temp
            temp = temp.next
        return temp


def UI_thread(L):
    """
    function which is executed in separate threading
    it implements user interface.
    """
    while True:
        print('\n')
        operation = raw_input(LOCALISATION_PKG['menu_option_list'])
        try:
            operation = int(operation)
        except ValueError:
            continue
        if operation == 1:
            del_str = raw_input(LOCALISATION_PKG['menu_operation1_input'])
            print('\n')
            L.add(del_str)
        if operation == 2:
            del_str = raw_input(LOCALISATION_PKG['menu_operation2_input'])
            print('\n')
            L.delete(del_str)
        if operation == 3:
            print(L.str())
        if operation == 4:
            break

# dictionary of supported languages
LANGUAGES = {
    'ru': RUS,
    'en': ENG
}

def set_lockalisation_pkg(system_lng):
    """ sets the localisation package """
    global LOCALISATION_PKG
    for key in LANGUAGES:
        if key in system_lng:
            LOCALISATION_PKG = LANGUAGES[key]
            break
    if LOCALISATION_PKG is None:
        LOCALISATION_PKG = LANGUAGES['en']

def init_os_win():
    """ retrives sustem language on Windows """
    import ctypes
    windll = ctypes.windll.kernel32
    system_lng = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    set_lockalisation_pkg(system_lng)

def init_os_linux():
    """ retrives sustem language on Linux """
    system_lng = locale.getdefaultlocale()[0]
    set_lockalisation_pkg(system_lng)

def init_os_default():
    """ sets the language packet to eng """
    global LOCALISATION_PKG
    LOCALISATION_PKG = LANGUAGES['en']

# dictionary that is used to select the initialisation function
# for current OS.
INIT_SYSTEM = {
    'Windows': init_os_win,
    'Linux': init_os_linux
}

def init_python_version_based():
    """
    perform initialisation based on python version
    in order to preserv compability with python version 2.7
    """
    # For portability between 2.7 and 3.6
    if int((sys.version).split('.')[0]) >= 3:
        global raw_input
        raw_input = input

def schedule_loop():
    """ Waiting and executing jobs time to time """
    while True:
        schedule.run_pending()
        time.sleep(1)

def init():
    """ performs initialisation based on the information about the system """
    try:
        init_os_based = INIT_SYSTEM[platform.system()]
    except KeyError:
        init_os_based = init_os_default
    init_os_based()
    init_python_version_based()
    print(LOCALISATION_PKG['greeting'])
    global L
    L = List()
    L.readTXT()
    # a separate thread is created for user interface
    t = threading.Thread(target=UI_thread, args=(L,))
    t.start()
    # initialisation comleted, start scheduling jobs
    schedule_loop()

# start initialisation
init()
