# Installed:
# geopy
#   anaconda search -t conda geopy
#   conda install -c topper geopy
# cv2
#   conda install -c https://conda.binstar.org/menpo opencv

import sys
import getopt
import neighborhood_dashboard



def printUsage():
    print '###########################################################################################################'
    print 'Arguments: (OPTIONAL)'
    print '-h: Show this help'
    print '-c <filename>: Name of the config file to load. Refer to the documentation for these settings'
    print '###########################################################################################################'


if __name__ == "__main__":
    config_file = 'config.cfg'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:",["cfile="])
        for opt, arg in opts:
            if opt == '-h':
                printUsage()
                sys.exit(0)
            elif opt in ("-c", "--cfile"):
                config_file = arg
    except getopt.GetoptError:
        print 'Error: '
        printUsage()
        sys.exit(2)
    nd = neighborhood_dashboard.NeighborhoodDashboard(config_file)
    nd.run_preprocessing()
