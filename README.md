# PyWeb
Apache doesn't run very well on Windows machines, so I'm creating this as a more efficient means to use the HyperText Transfer Protocol on any platform.

## Caching
This webserver is capable of creating it's own cache using LZ77. You can turn this on or off in the Config.ini file located in the resources folder. It is enabled by default and generates a compressed file. It *is* recommended.

## Launching Instructions
1. Install Python 2.7
2. Download the PyWeb
3. Install the requirements.txt (pip install -r requirements.txt)
4. Run \_\_init\_\_.py

## Dependencies
This project uses the following Python libraries:
  - BitArray

## Known Issues
- Currently, only htm, html, and php files are cached by default.
- Not capable of PhP, yet.
- Does not properly structure headers, so browsers are not capable of rendering the html file.
