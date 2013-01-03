# Super simple print function for Sublime Text 2

There's a lot of requests for printing in the Sublime Text discussion forum.
Personally, I very rarely need printing, but I can appreciate that some do.

So here's a really simple solution to the problem. Nothing more than sending
the data to an external program that does the printing.

The program used, and various options are selected in the settings file.
As default, I use *enscript* since that is available in a standard install
for both Mac and Linux. You could use *a2ps* or even *lpr* instead, with
suitable options. Windows users are left out at the moment, though I know
you can do similar things there.

## Configuration

Add whatever options you need in the settings file. Note that options without
a value (i.e. `--option`) need to be specified with an empty string as value,
due to the JSON dictionary format.

The given print command will be searched inside path '/usr/bin' and
'/usr/local/bin'. An absolute path should be given if it resides in another
directory.

### Supported print options

* Print the entire file from the active view.
* Print the selected text from the active view.
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

## Install enscript

Check whether enscript is installed already:

    $ which enscript

If SublimePrint does not print, edit the user settings and change the *command*
value to the absolute path shown by the *which* command. In most cases, this is
not needed.

### Linux

Given CUPS is already installed and you can successful print from other programs
but *enscript* can not be found:

    [Debian based]$ sudo apt-get install enscript

    [RedHat based]$ sudo yum install enscript

### OS X

    [Homebrew]$ brew install enscript

## Known limitations

* Only saved documents can be printed via menu 'Print Entire File'.
  The workaround for unsaved or modified files is to select all lines and use
  'Print Selection'.
* No preview.
* Printer selection via properties file only.
* Windows not yet implemented.

## External commands

* The documentation for *enscript* is, for instance,
  [here](http://linux.die.net/man/1/enscript)
* Other processors you'll have to find yourself.
