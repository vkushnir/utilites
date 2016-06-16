#!/usr/bin/python
"""
 This python module is used for
 generate rate_limit calculations.

 Written by : Vladimir Kushnir
 Created date: 16.06.2016
 Last modified: 16.06.2016
 Tested with : Python 2.7.11

    Simple usage example:

    ratelimit.py 1024

"""
# Import required python libraries
import sys
from optparse import OptionParser

__version__ = "1.00"
__copyright__ = "Vladimir Kushnir aka Kvantum i(c)2016"

__all__ = ['get_param',
           'calc',
           'out']

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
        print txt.format(kbps, kbps*1000, burst_normal, burst_max)
    elif mode == 'cisco-av':
        txt = "\n  QU;{0:d};{1:d};{2:d};D;{0:d};{1:d};{2:d}\n"
        print txt.format(kbps*1000, burst_normal, burst_max)
    else:
        sys.exit("Wrong output mode!")

def main():
    """Main procedure"""
    (kbps, burst_time, mode) = get_param()
    (burst_normal, burst_max) = calc(kbps, burst_time)
    out(kbps, burst_normal, burst_max, burst_time, mode)

if __name__ == "__main__":
    main()
