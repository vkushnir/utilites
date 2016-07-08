#!/usr/bin/python
"""
 This python module is used for
 generate rate_limit calculations.

 Written by : Vladimir Kushnir
 Created date: 16.06.2016
 Last modified: 08.07.2016
 Tested with : Python 2.7.11

    Simple usage example:

    ratelimit.py 1024

"""
# Import required python libraries
import sys
from optparse import OptionParser
from platform import system
# Windows Clipboard Support
import ctypes

OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
CF_UNICODETEXT = 13

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalSize = ctypes.windll.kernel32.GlobalSize
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

unicode_type = type(u'')

__version__ = "1.01"
__copyright__ = "Vladimir Kushnir aka Kvantum i(c)2016"

__all__ = ['get_param',
           'calc',
           'out']

def put_clipboard(msg):
    """Put message to clipboard"""
    if system() == 'Windows':
        if not isinstance(msg, unicode_type):
            msg = msg.decode('mbcs')
        data = msg.encode('utf-16le')
        OpenClipboard(None)
        EmptyClipboard()
        handle = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(data) + 2)
        pcontents = GlobalLock(handle)
        ctypes.memmove(pcontents, data, len(data))
        GlobalUnlock(handle)
        SetClipboardData(CF_UNICODETEXT, handle)
        CloseClipboard()

def get_param(arguments=None):
    """Parse Command-Line parameters"""
    parser = OptionParser(usage="%prog <kbps> [options]", version="%prog "+__version__)
    parser.set_defaults(burst_time=1.5, mode='cisco-rt')
    #parser.add_option('-l', '--rate-limit', dest='kbps', type="int", help="Rate limit in kbps")
    parser.add_option('-t', '--burst-time', dest='burst_time', type='float',
                      help="Burst time in seconds")
    parser.add_option('-m', '--output-mode', dest='mode', choices=['cisco-rt', 'cisco-av'],
                      help="Output mode ('cisco-rt'/'cisco-av')")

    (opt, args) = parser.parse_args(arguments)

    if len(args) != 1:
        parser.error("You must cpecify kbps rate!")

    return (int(args[0]), opt.burst_time, opt.mode)

def calc(kbps, burst_time=1.5):
    """Calculate Normal and Max Burst values"""
    bps = kbps * 1000
    burst_normal = int(round(bps / 8 * burst_time, 0))
    burst_max = 2 * burst_normal

    return (burst_normal, burst_max)

def out(kbps, burst_normal, burst_max, burst_time, mode='cisco-rt'):
    """Print out formatted strings with calculated values"""
    if mode == 'cisco-rt':
        txt = """!
  bandwidth {0:d}
    rate-limit input {1:d} {2:d} {3:d} conform-action transmit exceed-action drop
    rate-limit output {1:d} {2:d} {3:d} conform-action transmit exceed-action drop
!"""
        txt = txt.format(kbps, kbps*1000, burst_normal, burst_max)
        msg = txt
    elif mode == 'cisco-av':
        txt = "\n  QU;{0:d};{1:d};{2:d};D;{0:d};{1:d};{2:d}\n".format(kbps*1000, burst_normal, burst_max)
        msg = "QU;{0:d};{1:d};{2:d};D;{0:d};{1:d};{2:d}".format(kbps*1000, burst_normal, burst_max)
    else:
        sys.exit("Wrong output mode!")
    print txt
    put_clipboard(msg)

def main():
    """Main procedure"""
    (kbps, burst_time, mode) = get_param()
    (burst_normal, burst_max) = calc(kbps, burst_time)
    out(kbps, burst_normal, burst_max, burst_time, mode)

if __name__ == "__main__":
    main()
