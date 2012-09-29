# Super simple print function for Sublime Text 2

There's a lot of requests for printing in the discussion forum for
Sublime Text. Personally, I very rarely need printing, but I can appreciate
that some do.

So here's a really simple solution to the problem. Nothing more than sending
the file attached to the current view to an external program that does the
printing.

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

## Select a printer

A list of all available printers will be created in the user specific 'SublimePrint.sublime-settings' file. 
The available printers have key format "printer_?". The selected printer is defined under key "used_printer".

To re-create the list of available printers, delete all keys "used_printer" and "printer_?" from the user specific 
'SublimePrint.sublime-settings' and print an empty page.

## Install enscript

Check whether enscript is installed already:

$ which enscript

If SublimePrint does not print, edit the user settings and change the "command" 
value to the absolute path shown by the *which* command. In most cases, this is 
not needed. 

### Linux

Given CUPS is already installed and you can successful print from other programs 
but *enscript* can not be found:

[Debian based]$ sudo apt-get install enscript

[RedHat based]$ sudo yum install enscript 

### Mac OS

[Homebrew]$ brew install enscript

## External commands

* The documentation for *enscript* is, for instance,
  [here](http://linux.die.net/man/1/enscript)
* Other processors you'll have to find yourself.
