import sublime
import sublime_plugin
import os
import subprocess


def load_settings():
    return sublime.load_settings("SublimePrint.sublime-settings")

def save_settings():
    sublime.save_settings("SublimePrint.sublime-settings")

def open_pipe(cmd, cwd=None, stdin=None):
    return subprocess.Popen(cmd, cwd=cwd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)


class SublimePrint(sublime_plugin.WindowCommand):
    '''
    Base class for the print commands. Handles creating the printer list and
    setting options to the printer command.
    '''

    BIN_PATHS = [
        "/usr/bin",
        "/usr/local/bin"
    ]

    def is_enabled(self):
        '''
        Print commands normally requires an active view.
        '''
        return self.window.active_view() != None

    def find_command(self, cmd):
        '''
        If the given command exists in one of the BIN_PATHS folders, return
        the full path, else exit.
        '''
        if os.path.isabs(cmd) and not os.path.isfile(cmd):
            cmd_path = None
        else:
            try:
                cmd_path = list(filter(os.path.isfile, [os.path.join(p, cmd) for p in self.BIN_PATHS]))[0]
            except:
                cmd_path = None

        if cmd_path is None:
            sublime.error_message("Command '" + cmd + "' not found! Please review the documentation.")

        return cmd_path

    def get_printer(self):
        '''
        Create the list of available printers if necessary and return the
        used printer (the default printer if the list is recreated).
        '''
        # Create printer list in user settings if not defined
        settings = load_settings()
        used_printer = settings.get("used_printer", None)
        cache_printer_names = settings.get("cache_printer_names", True)
        if used_printer is None or not cache_printer_names:
            lpstat_cmd = self.find_command("lpstat")
            if lpstat_cmd is None: return None
            # Get default printer
            p = open_pipe([lpstat_cmd, "-d"])
            if p.wait() == 0:
                try:
                    used_printer = p.stdout.read().split(":")[1].strip()
                    settings.set("used_printer", used_printer)
                except:
                    # No default printer set
                    pass
            # Get all printers
            p = open_pipe([lpstat_cmd, "-a"])
            if p.wait() == 0:
                printer_cnt = 0
                for line in p.stdout:
                    printer_cnt += 1
                    printer_name = "printer_{0}".format(printer_cnt)
                    settings.set(printer_name, line.split()[0])
            # Save the updated printer information
            save_settings()

        return used_printer


    def get_lang(self):
        '''
        Return the syntax (language) of the active window.
        '''
        syntaxPackage = sublime.active_window().active_view().settings().get('syntax')
        #print(syntaxPackage)
        if syntaxPackage.count('/') == 3 and syntaxPackage.count('/Support/') == 1:
            (pkg, lang, support, tmLang) = syntaxPackage.split('/')
        else:
            (pkg, lang, tmLang) = syntaxPackage.split('/')
        
        #print(lang)
        lang = lang.lower()

        return lang


    def printer_command(self, title=None, print_line_numbers=True):
        '''
        Return the array of command line options to pass to the subprocess.
        '''
        settings = load_settings()
        print_cmd = self.find_command(settings.get("command"))
        if print_cmd is None: return None
        options = settings.get("options")
        title_option = settings.get("title_option")
        if title_option and title:
            options[title_option] = title
        if not (print_line_numbers and settings.get("print_line_numbers")):
            options.pop("line-numbers")

        if options["highlight"] == True:
            lang = self.get_lang()
            options["highlight"] = lang
            if lang == 'text':
                options.pop("highlight")
            # print(options)

        options_list = ["--{0}={1}".format(k, v) for k, v in options.items() if v != ""]
        options_list += ["--{0}".format(k) for k, v in options.items() if v == ""]

        # printer = self.get_printer()
        # if printer is not None:
        #     options_list.append("--printer={0}".format(printer))

        return [print_cmd] + options_list

    def send_file_to_printer(self, cmd, file_path):
        file_dir, file_name = os.path.split(file_path)
        cmd.append(file_name)
        p = open_pipe(cmd, cwd=file_dir)
        ret = p.wait()

        if ret:
            raise EnvironmentError((cmd, ret, p.stdout.read()))

    def send_text_to_printer(self, cmd, text):
        p = open_pipe(cmd, stdin=subprocess.PIPE)
        p.communicate(text)
        ret = p.wait()

        if ret:
            raise EnvironmentError((cmd, ret, p.stdout.read()))

    def get_all_printers(self):
        printer_idx = 1
        printers = []
        settings = load_settings()
        while settings.has("printer_{0}".format(printer_idx)):
            printers.append(settings.get("printer_{0}".format(printer_idx)))
            printer_idx += 1

        return printers

    def print_file_callback(self, name_index):
        if name_index == -1: return

        printer_names = self.get_all_printers()
        printer = printer_names[name_index]

        file_path = self.window.active_view().file_name()
        if self.window.active_view().is_dirty():
            sublime.message_dialog("File has unsaved changes.")
            return
        elif not file_path:
            sublime.message_dialog("No file to print.")
            return

        cmd = self.printer_command()
        if cmd is not None:
            cmd.append("--printer={0}".format(printer))
            self.send_file_to_printer(cmd, file_path)

    def print_selection_callback(self, name_index):
        if name_index == -1: return

        settings = load_settings()
        printer_names = self.get_all_printers()
        printer = printer_names[name_index]

        view = self.window.active_view()
        if view.file_name():
            title = os.path.basename(view.file_name())
        else:
            title = "* Untitled *"

        text_parts = []
        for selection in view.sel():
            t = ""
            for line in view.lines(selection):
                if settings.get("print_line_numbers"):
                    t += "{0:>6}: ".format(str(view.rowcol(line.begin())[0] + 1))
                t += view.substr(line) + "\n"
            text_parts.append(t)
        text = "----------\n".join(text_parts)

        cmd = self.printer_command(title, False)
        if cmd is not None:
            cmd.append("--printer={0}".format(printer))
            self.send_text_to_printer(cmd, text)


    def print_clipboard_callback(self, name_index):
        if name_index == -1: return

        printer_names = self.get_all_printers()
        printer = printer_names[name_index]

        cmd = self.printer_command("* Clipboard *", False)
        if cmd is not None:
            cmd.append("--printer={0}".format(printer))
            self.send_text_to_printer(cmd, sublime.get_clipboard())


class PrintFileCommand(SublimePrint):
    '''
    Print the current file. This command assumes the file has been saved to
    disk. It will abort if not.
    '''
    def run(self):
        settings = load_settings()
        printer_names = self.get_all_printers()
        if settings.get("prompt_printer") == True:
            self.window.show_quick_panel(printer_names, self.print_file_callback)
        else:
            self.print_file_callback(printer_names.index(self.get_printer()))


class PrintSelectionCommand(SublimePrint):
    '''
    This command prints the current selection. If there are multiple
    selections, they will all be printed with a separator line between them.
    '''
    def run(self):
        settings = load_settings()
        printer_names = self.get_all_printers()
        if settings.get("prompt_printer") == True:
            self.window.show_quick_panel(printer_names, self.print_selection_callback)
        else:
            self.print_selection_callback(printer_names.index(self.get_printer()))


class PrintClipboardCommand(SublimePrint):
    '''
    This command prints the content of the clipboard.
    '''
    def run(self):
        settings = load_settings()
        printer_names = self.get_all_printers()
        if settings.get("prompt_printer") == True:
            self.window.show_quick_panel(printer_names, self.print_clipboard_callback)
        else:
            self.print_clipboard_callback(printer_names.index(self.get_printer()))

    def is_enabled(self):
        return sublime.get_clipboard() != ""
