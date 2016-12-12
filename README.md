# Neighborhood Dashboard

# About

![Neighborhood Dashboard](https://github.com/darty/neighborhood-dashboard/blob/master/main.jpg "Neighborhood Dashboard")

The Neighborhood Dashboard (ND) is an open tool used to quickly collect and aggregate spatial data including Open Street Map data, volunteered geographic information (VGI) or open geospatial data through any standard API or platform around different point of interests (POIs) (e.g. home locations of subjects from social science research). The collected data can be viewed and inspected in a web browser and exported for further analysis. The ND, an open-source tool, is freely available online and is being used by research teams to capture key features of the neighborhoods where children and adolescents in longitudinal and intervention-based studies live and attend school. Ideally, this tool will help place valuable data into the hands of researchers, community members and policy-makers who are trying to understand and improve the health of local communities and children.

Neighborhood Dashboard: An Open Tool for Child Health and Neighborhood Researchers
*Donald Degraen, Joy R. Piontak, Candice L. Odgers, Johannes Schöning

## Pre-compiled Binaries

Pe-compiled binaries for Windows 10 and Windows 7 can be found on the following links:

[Windows 10](http://81.7.15.7/~donald/nd/prebuild-windows10-30-11-2016.zip)

[Windows 7](http://81.7.15.7/~donald/nd/prebuild-windows7-30-11-2016.zip)

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

