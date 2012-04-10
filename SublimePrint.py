import sublime
import sublime_plugin
import subprocess
from os.path import split

class PrintCommand(sublime_plugin.WindowCommand):
    def run(self):
        file_path = self.window.active_view().file_name()
        if not file_path:
            sublime.error_message("No file to print.")
            return

        file_dir, file_name = split(file_path)
        settings = sublime.load_settings('SublimePrint.sublime-settings')
        options = ["--%s=%s" % (k, v) for k, v in settings.get("options").iteritems() if v != ""]
        options += ["--%s" % k for k, v in settings.get("options").iteritems() if v == ""]
        cmd = [settings.get("command")] + options + [file_name]

        p = subprocess.Popen(cmd, cwd=file_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ret = p.wait()

        if ret:
            raise EnvironmentError((cmd, ret, p.stdout.read()))

    def is_enabled(self):
        return self.window.active_view() != None
