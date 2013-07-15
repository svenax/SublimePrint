# Simple print function for Sublime Text 2 and 3

There are lots of requests for printing in the Sublime Text discussion forum.
Personally, I very rarely need printing, but I can appreciate that some do.

So here's a simple solution to the problem. Nothing more than sending the data
to an external program that does the printing.

The program used, and various options are selected in the settings file.
As default, I use `enscript` since that is available in a standard install
for both Linux, Mac and possiby Windows. You could use `a2ps` or even `lpr`
instead, with suitable options.

**Note:** The code in `SublimePrint.py` actually depends on enscript a bit
at the moment. I may clean that up in case there are requests for it.

## Configuration

Add whatever options you need in the settings file. Note that options without
a value (i.e. `--option`) need to be specified with an empty string as value,
due to the JSON dictionary format.

The given print command will be searched for inside path `/usr/bin` and
`/usr/local/bin`. An absolute path should be given if it resides in another
directory.

### Supported print options

* Print the entire file of the active view.
* Print the selected text of the active view.
  Multiple selections are supported.
* Print clipboard content.

### Select a printer

A list of all available printers will be created in the user specific
*SublimePrint.sublime-settings* file at the first time something is printed.
The available printers have key format *printer_(a number)*. The selected
printer is defined under key *used_printer*. The value of *used_printer*
defaults to the default printer.

To re-create the list of available printers, delete key *used_printer* and all
occurrences of *printer_(a number)* from the user specific
*SublimePrint.sublime-settings* and print some short text.

If you instead always want to print on the default printer, you can set
*cache_printer_names* to false in the user configuration file. Doing that will
cause the printer list to always be generated.

## Install enscript

Check whether enscript is installed already:

    $ which enscript

If SublimePrint does not print, edit the user settings and change the *command*
value to the absolute path shown by the *which* command. In most cases, this is
not needed.

### Linux

Given CUPS is already installed and you can successful print from other programs
but *enscript* can not be found:

    [Debian]$ sudo apt-get install enscript

    [RedHat]$ sudo yum install enscript

### OS X

    [Homebrew]$ brew install enscript

### Windows

Enscript is available for Windows from several providers, for instance
[this one](http://gnuwin32.sourceforge.net/packages/enscript.htm). I have
not verified that this works, though. If someone wants to try, please do so.

## Known limitations

* Only saved documents can be printed with 'Print Entire File'.
  The workaround for unsaved or modified files is to select all lines and use
  'Print Selection'.
* No preview or print dialog.
* Printer selection via properties file only.

## External commands

* The documentation for *enscript* is, for instance,
  [here](http://linux.die.net/man/1/enscript)
* Other processors you'll have to find yourself.

## History

10 Apr 2012
: First version. Only supports 'Print Entire File'.

1 Oct 2012
: Many additions by Kai Ellinger, including 'Print Selection',
  'Print Clipboard', and printer setup.

4 Jan 2013
: Total rewrite of code to elliminate duplication and to
  simplify things. Submitted to Package Control.

29 Jun 2013
: Some tweaks to make the code compatible with Python 3, and thus
  with Sublime Text 3.

30 Jun 2013
: Don't call `sys.exit()`, since that makes Sublime Text hang.

15 Jul 2013
: Added *cache_printer_names* setting for those who always want to use
  the default printer.
