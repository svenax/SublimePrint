import sublime
import sublime_plugin
import subprocess
from os.path import split
from os.path import isabs
from os.path import isfile

class PrintSelectionCommand(sublime_plugin.WindowCommand):
    def run(self):

        # load settings
        settings = sublime.load_settings('SublimePrint.sublime-settings')

        # check whether plain text or file name and line numbers must be printed
        isFileNameAndLineNumberRequested = settings.get("print_file_name_and_line_numbers_for_selection",0)

        # START: get selected text to be printed
        # taken from plug-in copy_with_line_numbers
        textToPrint = ""

        view = sublime.Window.active_view(sublime.active_window())

        # set file name
        if isFileNameAndLineNumberRequested == 1:
            if view.file_name():
                textToPrint = "File: " + view.file_name() + "\n"
            else:
                textToPrint = "File: <unsaved>\n"

        # handle text
        isFollowupSelection = None
        for selection in view.sel():
            if isFollowupSelection:
                # split multi selections with ---
                textToPrint += "---\n"
            else:
                # but not the first one
                isFollowupSelection = True
            # for each selection
            for line in view.lines(selection):
                if isFileNameAndLineNumberRequested == 1:
                    textToPrint += str(view.rowcol(line.begin())[0] + 1) + ": " + view.substr(line) + "\n"
                else:
                    textToPrint += view.substr(line) + "\n"
        # END: get selected text to be printed

        # check where the print command has an absolute path
        printcommand = settings.get("command")
        # if not absolute, search it
        if not isabs(printcommand):
            if isfile("/usr/bin/"+printcommand):
                printcommand = "/usr/bin/"+printcommand
            elif isfile("/usr/local/bin/"+printcommand):
                printcommand = "/usr/local/bin/"+printcommand
            # and save in user settings for the next time
            settings.set("command",printcommand)
            sublime.save_settings('SublimePrint.sublime-settings')

        # additional options but ignore "line-numbers" because this is from clipboard
        options = ["--%s=%s" % (k, v) for k, v in settings.get("options").iteritems() if v != "" and k != "line-numbers"]
        options += ["--%s" % k for k, v in settings.get("options").iteritems() if v == ""]

        # create printer list in user settings if not defined
        printer = settings.get("used_printer","DEFAULT")
        if printer is None or printer == "DEFAULT":
            # where is lpstat to list all printers?
            if isfile("/usr/bin/lpstat"):
                lpstatcommand = "/usr/bin/lpstat"
            elif isfile("/usr/local/bin/lpstat"):
                lpstatcommand = "/usr/local/bin/lpstat"
            # get default printer
            p = subprocess.Popen([lpstatcommand] + ["-d"], stdout=subprocess.PIPE)
            ret = p.wait()
            # Example:
            # $ lpstat -d
            # System-Standardzielort: Samsung_CLP_310_Series__SAMSUNG_CLP310N_
            # $ lpstat -d
            # system default destination: Cups-PDF
            if not ret:
                defaultPrinter = p.stdout.read().split(":")[1].strip()
                settings.set("used_printer",defaultPrinter)
                sublime.save_settings('SublimePrint.sublime-settings')
            # get all printers
            p = subprocess.Popen([lpstatcommand] + ["-a"], stdout=subprocess.PIPE)
            ret = p.wait()
            # Example:
            # $ lpstat -a
            # Samsung_CLP_310_Series__SAMSUNG_CLP310N_ akzeptiert Anfragen seit Sa 29 Sep 23:41:57 2012
            # $ lpstat -a
            # Cups-PDF accepting requests since Sun 30 Sep 2012 01:14:33 AM CEST
            # DEMUC001 accepting requests since Wed 05 Sep 2012 06:28:30 PM CEST
            # HP_Color_LaserJet_4700 accepting requests since Fri 28 Sep 2012 01:24:25 PM CEST
            # SamsungCLP310 accepting requests since Sun 30 Sep 2012 01:16:19 AM CEST
            if not ret:
                printerCount = 0
                for line in p.stdout:
                    printerCount += 1
                    availablePrinterName = "printer_%d" % (printerCount)
                    settings.set(availablePrinterName,line.split()[0])
                sublime.save_settings('SublimePrint.sublime-settings')
        # use the printer
        if printer is not None and printer != "DEFAULT":
            options += ["-P", printer]

        # print
        cmd = [printcommand] + options

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.communicate(textToPrint)
        ret = p.wait()

        if ret:
            raise EnvironmentError((cmd, ret, p.stdout.read()))

    def is_enabled(self):
        return self.window.active_view() != None
