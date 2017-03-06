#!/usr/bin/env python
#   ____                      _        ____  _       _   _            
#  / ___| ___ _ __   ___ _ __(_) ___  |  _ \| | ___ | |_| |_ ___ _ __ 
# | |  _ / _ \ '_ \ / _ \ '__| |/ __| | |_) | |/ _ \| __| __/ _ \ '__|
# | |_| |  __/ | | |  __/ |  | | (__  |  __/| | (_) | |_| |_  __/ |   
#  \____|\___|_| |_|\___|_|  |_|\___| |_|   |_|\___/ \__|\__\___|_|   
#
# Created by Shahar Gino at February 2017
#
# Usage:  % generic_plotter.py -h

from time import time
import datetime
from sys import argv, exit
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib import cm as cmx
from matplotlib import colors
from getopt import getopt, GetoptError

# ---------------------------------------------------------------------------------------------------------------
class PlotObj:

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    def __init__(self, x_var, y_vars, plot_type, plot_attr, debug_en, quiet_mode):
        """ Constructor """
        self.x_var = x_var
        self.y_vars = y_vars
        self.plot_type = plot_type
        self.plot_attr = plot_attr
        self.debug_en = debug_en
        self.quiet_mode = quiet_mode
        self.figure, self.ax = plt.subplots()
        self.figure_rdy = False
        self.cmap = self.get_cmap(100)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    def build(self):
        """ Builds a figure to be later on plotted and/or saved """

        # Figure's title:
        fig_name = self.plot_type
        fig_name_match = [s for s in self.plot_attr if "--fig_name=" in s]
        if fig_name_match:
            fig_name = str(fig_name_match).split('=')[1].split("'")[0]

        # X-label:
        xlabel = 'x-axis'
        xlabel_match = [s for s in self.plot_attr if "--xlabel=" in s]
        if xlabel_match:
            xlabel = str(xlabel_match).split('=')[1].split("'")[0]

        # Y-label:
        ylabel = 'y-axis'
        ylabel_match = [s for s in self.plot_attr if "--ylabel=" in s]
        if ylabel_match:
            ylabel = str(ylabel_match).split('=')[1].split("'")[0]

        # Y-labels:
        ylabels = (len(self.y_vars) * 'none ').split()
        ylabels_match = [s for s in self.plot_attr if "--ylabels=" in s]
        if ylabels_match:
            ylabels = str(ylabels_match).split('=')[1].split("'")[0].split(';')

        # Histogram Bins:
        hist_bins = 20
        hist_bins_match = [s for s in self.plot_attr if "--hist_bins=" in s]
        if hist_bins_match:
            hist_bins = int(str(hist_bins_match).split('=')[1].split("'")[0])

        # Build data:
        self.figure_rdy = True
        self.figure.canvas.set_window_title(fig_name)
        plt.title(fig_name)

        # XY:
        if self.plot_type == 'xy':
            idx = 0
            for y_var in self.y_vars:
                self.ax.plot(self.x_var, y_var, '--', linewidth=2, label=ylabels[idx])
                idx += 1

            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            plt.grid(True)
            self.ax.legend(loc='lower right')

        # Bars:
        elif self.plot_type == 'bars':
            idx = 0
            width = 0.35
            ind = arange(len(self.x_var))
            for y_var in self.y_vars:
                x = []
                for x_ in y_var:
                    x.append(float(x_))
                self.ax.bar(left=ind+idx*width, height=x, width=width, color=self.cmap(10*idx))
                idx += 1

            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            plt.xticks(ind + width, self.x_var)
            plt.grid(True)
            self.ax.legend(loc='lower right')

        # Scatter:
        elif self.plot_type == 'scatter':
            plt.scatter(self.x_var, self.y_vars, label=ylabels[0])
            plt.grid(True)
            self.ax.legend(loc='lower right')

        # Histogram:
        elif self.plot_type == 'hist':
            x = []
            for x_ in self.x_var:
                x.append(float(x_))
            plt.hist(x, hist_bins, normed=1, facecolor='green', alpha=0.5)
            plt.grid(True)

        else:
            print 'Error: Cannot build figure, due to an unsupported plot type (%s)' % self.plot_type
            self.figure_rdy = False

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    def show(self):
        """ Shows a built figure on the screen """

        if self.figure_rdy:
            plt.show()
        else:
            print "Error: Cannot show figure, since Plot is not defined"

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    def save(self):
        """ Saves a built figure into a file """

        # Filename:
        saveas_match = [s for s in self.plot_attr if "--saveas=" in s]
        if saveas_match:
            filename = str(saveas_match).split('=')[1].split("'")[0]
        else:
            d = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
            filename = 'figure_' + d + '.png'

        if self.figure_rdy:
            self.figure.savefig(filename, dpi=100)  # use dpi=1000 for higher quality (larger file..)
            if not self.quiet_mode:
                print "Figure has been saved as: %s" % filename
        else:
            print "Error: Cannot save figure to a PNG file, since Plot is not defined"

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    @staticmethod
    def get_cmap(n):
        """Returns a function that maps each index in 0, 1, ... N-1 to a distinct RGB color."""

        color_norm = colors.Normalize(vmin=0, vmax=n-1)
        scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')

        def map_index_to_rgb_color(index):
            return scalar_map.to_rgba(index)

        return map_index_to_rgb_color

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    def __str__(self):
        """ print method """

        if not self.quiet_mode:
            if self.debug_en:
                return "PlotObj: x_var=%s, y_vars=%s, plot_type=%s, plot_attr=%s)" % \
                    (self.x_var, self.y_vars, self.plot_type, self.plot_attr)
            else:
                return "PlotObj: #x_var=%d, #y_vars=%d, plot_type=%s, #plot_attr=%d)" % \
                    (len(self.x_var), len(self.y_vars), self.plot_type, len(self.plot_attr))
        else:
            return ""

# ---------------------------------------------------------------------------------------------------------------
class Struct:
    """Python Structing flow"""

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# ---------------------------------------------------------------------------------------------------------------
def usage():
    """ Usage information """

    print 'Usage:  generic_plotter.py -x <X-Variable> -y <Y-variables> -t <PlotType> [--attr=<PlotAttributes>] [--debug] [--quiet]'
    print ''
    print 'Usages Examples: '
    print '        (-) generic_plotter.py -x "1 2 3" -y "1 2 3,4 5 6" -t "xy" --attr="--fig_name=myFigure1 --saveas=example1.png --xlabel=Time[us] --ylabel=Throughput[MBps] --ylabels=line1;line2"'
    print '        (-) generic_plotter.py -x "test1 test2 test3" -y "1 2 3,4 5 6" -t "bars" --attr="--fig_name=myFigure4 --saveas=example4.png --xlabel=TestName --ylabel=Throughput[MB/s]"'
    print '        (-) generic_plotter.py -x "1 2 3" -y "1 2 3" -t "scatter" --attr="--fig_name=myFigure2 --saveas=example2.png --ylabels=line1"'
    print '        (-) generic_plotter.py -x "10 10 10 20 30 30" -t "hist" --attr="--fig_name=myFigure3 --saveas=example3.png --hist_bins=20"'
    print ''
    print 'Notes:  (-) All variables are expected to be retrieved as strings (delimited by spaces).'
    print '        (-) Supported PlotType:  xy, bars, scatter, hist'
    print '        (-) Supported PlotAttributes:  --fig_name, --saveas, --xlabel, --ylabel, --ylabels'
    print '        (-) The -x and -y flags can contain a filename path, which contains the string vector (e.g. -x "./x_file.txt, where ./x_file.txt contains: "1 2 3")'
    print '        (-) Useful command for substituting new-lines with spaces (in files):  tr "\\n" " " < myFile'
    print ''
    print 'Additional information:  http://matplotlib.org/gallery.html'
    print ''

# ---------------------------------------------------------------------------------------------------------------
def main(_argv):
    """ Main function """

    # Default parameters:
    args = Struct(
        x_var="",
        y_vars="",
        plot_type="",
        plot_attr="",
        debug_en=False,
        quiet_mode=False
    )

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # User-Arguments parameters (overrides Defaults):
    try:
        opts, user_args = getopt(_argv, "hx:y:t:", ["attr=", "debug", "quiet"])

        for opt, user_arg in opts:
            if opt == '-h':
                usage()
                exit()
            elif opt in "-x":
                args.x_var = user_arg
            elif opt in "-y":
                args.y_vars = user_arg
            elif opt in "-t":
                args.plot_type = user_arg
            elif opt in "--attr":
                args.plot_attr = user_arg
            elif opt in "--debug":
                args.debug_en = True
            elif opt in "--quiet":
                args.quiet_mode = True

    except GetoptError:
        usage()
        exit(2)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # Main course:
    if not args.x_var or (not args.y_vars and args.plot_type != 'hist') or not args.plot_type:
        usage()
        exit(2)

    # Files --> Strings (x,y):
    if '/' in args.x_var:
        f = open(args.x_var, 'r')
        args.x_var = f.readlines()[0]
        f.close()
    if '/' in args.y_vars:
        f = open(args.y_vars, 'r')
        args.y_vars = f.readlines()[0]
        f.close()

    # Strings --> Lists:
    x_var = args.x_var.split()
    if ',' in args.y_vars:
        y_vars_ = args.y_vars.split(',')
        y_vars = []
        for y_var in y_vars_:
            y_vars.append(str(y_var).split())
    else:
        y_vars = [args.y_vars.split()]
    plot_attr = args.plot_attr.split()

    # Plot generation:
    print "Generating a plotting object"
    plot_obj = PlotObj(x_var, y_vars, args.plot_type, plot_attr, args.debug_en, args.quiet_mode)
    plot_obj.build()
    print plot_obj

    print "Showing figure"
    plot_obj.show()

    print "Saving figure into a file"
    plot_obj.save()

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    if len(argv) < 3:
        usage()

    else:
        t0 = time()
        print 'Start'

        main(argv[1:])

        t1 = time()
        t_elapsed_sec = t1 - t0
        print('Done! (%.2f sec)' % t_elapsed_sec)
