# Neighborhood Dashboard

# About

The Neighborhood Dashboard (ND) is an open tool developed by researchers from Hasselt University (Belgium) and Duke University (USA) to quickly collect and aggregate spatial data (for example volunteered geographic information (VGI) or open geospatial data through any API or platform) around different point of interests (POIs) (e.g. home locations of subjects from social science research). The collected data can be viewed and inspected in any web browser and later used for further analysis. This document is a quick start guide to help users to install and to use the software.

## Pre-compiled Binaries

Pe-compiled binaries for Windows 10 and Windows 7 can be found on the following links:

[Windows 10](http://81.7.15.7/~donald/nd/prebuild-windows10-09-11-2016.zip)

[Windows 7](http://81.7.15.7/~donald/nd/prebuild-windows7-09-11-2016.zip)

## Getting Started

Please find the manual for the Neighborhood Dashboard on the following link:

[ND Manual](http://81.7.15.7/~donald/nd/Tutorial_NBDashboard_v5.pdf)

### Configuration

In order to configure the ND, you have to rename the file 'config_example.cfg' to 'config.cfg' and edit it according to your needs. The following is an example of a configuration. Please note that the API-keys for Google StreetView and the Walkability API have been replaced by `xx`.

```
[files]
location = ../input/family_locations.csv
sso = ../input/sso_variables.csv
urbanicity = ../input/urbanicity.csv

[settings]
year = 2012
output-directory = ../output/html
fake-requests = 1
fake-requests-count = 9
streetview-detection = 1

[api-keys]
gsv = xx
walkability = xx

[debug]
generate-kml = 1
```

### Running the Neighborhood Dashboard

The Neighborhood Dashboard can be run using either one of the pre-compiled binaries or directly running the python scripts.

### Browsing the output

