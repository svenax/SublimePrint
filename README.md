# Super simple print function for Sublime Text 2

There's a lot of requests for printing in the discussion foras for
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

## External commands

* The documentation for *enscript* is, for instance,
  [here](http://linux.die.net/man/1/enscript)
* Other processors you'll have to find yourself.
