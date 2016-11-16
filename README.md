# PyWeb
Apache doesn't run very well on Windows machines, so I'm creating this as a more efficient means to use the HyperText Transfer Protocol on any platform.

## No More Caching
I have done away with server caching as it's too hard to maintain with BOA script, a primary plugin; additionally, you can now make plugins.

## Plugins
Functionality for plugins has been added. This can be accomplished through the Plugins include. Just put your plugin in the "./Plugins/" folder and it will automatically run. Look at my example, BOA, for some help.

## BOA
BOA stands for "Binary Object Access." Essentially, it allows you to generate HTML through Python with access to the objects on the webserver like the request itself. This will allow for some funky implementation, depending on your fancy.

## Launching Instructions
1. Install Python 2.7
2. Download the PyWeb
3. Run \_\_init\_\_.py

## Dependencies
There are no dependencies at this time. Everything is running off of native Python 2.7 code.
