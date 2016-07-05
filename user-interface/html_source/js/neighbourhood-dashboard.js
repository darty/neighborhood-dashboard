var map = null; // Google map
var marker = null; // Location marker for family
var heatmap = null; // Crime heatmap
var localHeatmap = null; // Crime heatmap for street
var streetData = null; // Neighbourhood street definition
var areaData = null; // Neighbourhood area definition (800 meters)

var infowindow = null;

var crimePieData = null;

// Callback script elements
var crimeScriptElement = null;
var roadScriptElement = null;
var detectionScriptElement = null;

var familyIds = []; // List of family Ids to iterate through
var currentPosition = 0; // Currently selected family

// Visibility of items
var heatmapVisible = true;
var localHeatmapVisible = false;
var neighbourhoodVisible = true;
var streetVisible = false;

var poisVisible = false;
var poisAllVisible = false;

var infowindow = null;

var MONTHS = ['januari', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
// List to show/hide selected data
var contentIds = ["sso", "crime", "poi"];

var pie_colors = [
{color: '#8dd3c7', highlight: "#56beac"},
{color: '#ffffb3', highlight: "#ffff67"},
{color: '#bebada', highlight: "#8f88bf"},
{color: '#fb8072', highlight: "#f93d28"},
{color: '#80b1d3', highlight: "#478ebf"},
{color: '#fdb462', highlight: "#fc9016"},
{color: '#b3de69', highlight: "#92cd2d"},
{color: '#fccde5', highlight: "#f885bf"},
{color: '#d9d9d9', highlight: "#b3b3b3"},
{color: '#bc80bd', highlight: "#9d529e"},
{color: '#ccebc5', highlight: "#9ad78c"},
{color: '#ffed6f', highlight: "#ffe323"},
{color: "#F7464A", highlight: "#FF5A5E"},
{color: "#4D5360", highlight: "#616774"}
];

var preferred_pois = {
	"leisure": ["park", "pitch", "playground", "sports_centre"],
	"amenity": ["bar", "fast_food", "pub", "kindergarten", "library", "school", "community_centre", "place_of_worship", "police"],
	"public_transport": ["station", "platform", "stop_position", "stop_area"],
	"landuse": ["recreation_ground", "residential", "forest", "meadow", "industrial"],
	"place": ["city", "borough", "suburb", "town", "village", "hamlet", "farm"],
	// "population": ["number"]
};

var marker_icons = {
    "leisure": 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
	"amenity": 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
	"public_transport": 'http://maps.google.com/mapfiles/ms/micons/orange-dot.png',
	"landuse": 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
	"place": 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png',
};

var polygon_colors = {
    "leisure": '#FFFF00',
	"amenity": '#0000FF',
	"public_transport": '#FFA500',
	"landuse": '#00FF00',
	"place": '#8A2BE2',
};

function inPreferredList(c)
{
	for (key in preferred_pois)
	{
		types = preferred_pois[key];
		if (types.indexOf(c) != -1)
			return true;
	}
	return false;
}
	
/*function showMetaData(locationid) {
	var sso = document.getElementById('sso-canvas');
	var id = document.createElement('div');
	id.innerHTML = locationid;
	
	sso.appendChild(id);
}*/

// Converts from degrees to radians.
Math.radians = function(degrees) {
  return degrees * Math.PI / 180;
};
 
// Converts from radians to degrees.
Math.degrees = function(radians) {
  return radians * 180 / Math.PI;
};

var neighbourhoodRadius = 800; // 800 meter

var poiMarkers = {};
var poiAllMarkers = {};
var poiPolygons = {};
var poiAllPolygons = {};

/*function calculateEarthRadius(lat, lon)
{
	var a = 6378137.0; // Equatorial radius
	var b = 6356752.3; // Polar radius
	var t = Math.pow((Math.pow(a, 2) * Math.cos(lat)), 2) + Math.pow((Math.pow(b, 2) * Math.sin(lat)) , 2);
	var n = Math.pow(a * Math.cos(lat), 2) + Math.pow(b * Math.sin(lat), 2);
	return t / n;
}*/

function createLegend()
{
    var legend = document.getElementById('legend');
	legend.index = 1;
	legend.title = 'Legend';
	map.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend);

    var legendList = document.createElement('ul');
	legendList.setAttribute('class', 'legend-list');

	for (var i in polygon_colors)
	{
        var legendItem = document.createElement('li');
        legendItem.setAttribute('class', 'legend-item');

        var color = document.createElement('div');
        color.innerHTML = '<img/>';
        color.setAttribute('class', 'color-box');
        color.style.backgroundColor = polygon_colors[i];

        var text = document.createElement('div');
        text.setAttribute('class', 'text-box');
        text.innerHTML = ' ' + i;

        legendItem.appendChild(color);
        legendItem.appendChild(text);

        legendList.appendChild(legendItem);
	}

	legend.appendChild(legendList);
}

function drawArea(lat, lon)
{
	var points = [];
	var earthRadius = 6378137;
	var latR = Math.radians(lat);
	var lonR = Math.radians(lon);
	
	var d = neighbourhoodRadius / earthRadius;
	for (var i = 0; i <= 360 ; i++)
	{
		var tc = Math.radians(i);
		var latX = Math.asin( (Math.sin(latR) * Math.cos(d)) + (Math.cos(latR) * Math.sin(d) * Math.cos(tc)) );
		var lonX = lonR;
		if (Math.cos(latX) != 0.0)
		{
			lonX = ((lonR - Math.asin( Math.sin(tc) * Math.sin(d) / Math.cos(latR)) + Math.PI) % (2 * Math.PI)) - Math.PI;
		}
		
		point = {};
		point['lat'] = Math.degrees(latX);
		point['lng'] = Math.degrees(lonX);
		points.push(point);
	}
	
	areaData = new google.maps.Polyline({
		path: points,
		geodesic: true,
		strokeColor: '#FF0000',
		strokeOpacity: 1.0,
		strokeWeight: 2
	});
	
	showNeighbourhood();
}

function initialize()
{
	map = new google.maps.Map(document.getElementById('map-content'), {
		zoom: 15,
		center: {lat: 0.0, lng: 0.0}
	});
	
	document.getElementById("prev-family").disabled = true;
	
	familyIds = [];
	for (var key in LOCATION_DATA) {
	  if (LOCATION_DATA.hasOwnProperty(key)) {
		familyIds.push(key);
	  }
	}

	createLegend();
	
	loadCurrentFamily();
}

function loadHeatmap(points)
{
	if (heatmap == null)
	{
		heatmap = new google.maps.visualization.HeatmapLayer({
			// data: points,
			map: map
		});
		heatmap.set('radius', 20);
	}
	heatmap.setData(points);
	
	showHeatmap();
}

function loadLocalHeatmap(points)
{
	if (localHeatmap == null)
	{
		localHeatmap = new google.maps.visualization.HeatmapLayer({
			// data: points,
			map: map
		});
		localHeatmap.set('radius', 20);
	}
	localHeatmap.setData(points);
	
	showLocalHeatmap();
}

function loadCrimesCallback(data)
{
    crimePieData = [];

	crime_data = data['crimes'];
	stop_and_search_data = data['stop_and_search'];
	var category_data = {};
	
	var monthly_total = {};
	monthly_total['total'] = {};
	monthly_total['total_on_street'] = {};
	
	var total = {};
	total['count'] = 0;
	total['locations'] = [];
	
	var total_on_street = {};
	total_on_street['count'] = 0;
	total_on_street['locations'] = [];
	
	for (var key in crime_data)
	{
		var monthly = crime_data[key];
		for (var crime in monthly)
		{
			var cat = monthly[crime]['category'];
			if (category_data[cat] == null)
			{
				category_data[cat] = {};
				category_data[cat]['count'] = 0;
				category_data[cat]['locations'] = [];
			}
			if (monthly_total[cat] == null)
			{
				monthly_total[cat] = {};
			}
			if (monthly_total[cat][key] == null)
			{
				monthly_total[cat][key] = 0;
			}
			if (monthly_total['total'][key] == null)
			{
				monthly_total['total'][key] = 0;
			}
			category_data[cat]['count'] += 1;
			monthly_total[cat][key] += 1;
			monthly_total['total'][key] += 1;
			total['count'] += 1;
			if (monthly[crime]['location'] != null)
			{
				var lat = monthly[crime]['location']['latitude'];
				var lng = monthly[crime]['location']['longitude'];
				var point = new google.maps.LatLng(lat, lng);
				category_data[cat]['locations'].push(point);
				total['locations'].push(point);
				if (monthly[crime]['on_family_road'] == true)
				{
					if (monthly_total['total_on_street'][key] == null)
					{
						monthly_total['total_on_street'][key] = 0;
					}
					monthly_total['total_on_street'][key] += 1;
					total_on_street['count'] += 1;
					total_on_street['locations'].push(point);
				}
			}
		}
	}

    var counter = 0;
	for (c in category_data)
	{
	    idv_data = {};
	    idv_data['value'] = category_data[c]['count'];
	    var index = counter;
	    while (pie_colors.length <= index)
	    {
	        index -= pie_colors.length;
	    }
        idv_data['color'] = pie_colors[index]['color'];
        idv_data['highlight'] = pie_colors[index]['highlight'];
	    idv_data['label'] = c;

	    crimePieData.push(idv_data);
	    counter += 1;
	}
	
	category_data['total'] = total;
	category_data['total_on_street'] = total_on_street;
	
	loadHeatmap(category_data['total']['locations']);
	loadLocalHeatmap(category_data['total_on_street']['locations']);
	
	var crime_content = document.getElementById("crime-content");
	crime_content.innerHTML = '';
	
	var crimeList = document.createElement('table');
	crimeList.setAttribute('class', 'data-table');
	
	var crimeTitleElement = document.createElement('tr');
	
	var title1 = document.createElement('th');
	title1.setAttribute('class', 'text');
	title1.innerHTML = "Crime Type";
	var title2 = document.createElement('th');
	title2.setAttribute('class', 'value');
	title2.innerHTML = "Instance count";
	crimeTitleElement.appendChild(title1);
	crimeTitleElement.appendChild(title2);
	crimeList.appendChild(crimeTitleElement);
	
	var even = false;
	
	for (var c in category_data)
	{
		var category = category_data[c];
		
		var crimeElement = document.createElement('tr');
		if (c == 'total')
		{
			crimeElement.setAttribute('class', 'data-row-total');
		}
		else
		{
			if (even)
			{
				crimeElement.setAttribute('class', 'data-row-even');
			}
			else
			{
				crimeElement.setAttribute('class', 'data-row-odd');
			}
			even = !even;
		}
		var img = document.createElement('img');
		img.setAttribute('src', 'img/more.png');
		img.setAttribute('align', 'bottom');
		
		var text = document.createElement('td');
		text.appendChild(img);
		text.setAttribute('class', 'text');
		if (CATEGORY_DATA[c] != null)
		{
			text.innerHTML += CATEGORY_DATA[c];
		}
		else
		{
			text.innerHTML += c;
		}

		var value = document.createElement('td');
		value.setAttribute('class', 'value');
		value.innerHTML = category['count'];
		
		crimeElement.appendChild(text);
		crimeElement.appendChild(value);
		
		crimeList.appendChild(crimeElement);
		
		if (monthly_total[c] != null)
		{
			var id = "crime-" + c + "-subtable";
			crimeElement.setAttribute('onclick', 'toggleSubTable(\'' + id +'\',this);');
			
			var subTableElement = document.createElement('table');
			subTableElement.setAttribute('class', 'sub-data-table');
			
			for (cat_monthly_key in monthly_total[c])
			{
				var cat_monthly_count = monthly_total[c][cat_monthly_key];
				
				var subElement = document.createElement('tr');
				
				var subkeyDescription = cat_monthly_key;
				if (MONTHS[cat_monthly_key] != null)
				{
					subkeyDescription = MONTHS[cat_monthly_key];
				}
				var subkeyText = document.createElement('td');
				subkeyText.setAttribute('class', 'text');
				subkeyText.innerHTML = subkeyDescription;
				
				var subkeyValue = document.createElement('td');
				subkeyValue.innerHTML = cat_monthly_count;
				
				subElement.appendChild(subkeyText);
				subElement.appendChild(subkeyValue);
				subTableElement.appendChild(subElement);
			}
			
			var subtableRow = document.createElement('tr');
			subtableRow.setAttribute('id', id);
			subtableRow.setAttribute('class', 'sub-data-table-row-hidden');
			
			var subtableData = document.createElement('td');
			subtableData.setAttribute("colspan", "2");
			
			subtableData.appendChild(subTableElement);
			subtableRow.appendChild(subtableData);
			crimeList.appendChild(subtableRow);
		}
	}



	var crimeChart = document.createElement('canvas');
	crimeChart.setAttribute('class', 'crime-pie-chart');
	crimeChart.setAttribute('width', '300');
	crimeChart.setAttribute('height', '300');

	crime_content.appendChild(crimeChart);
	crime_content.appendChild(crimeList);

	var ctx = crimeChart.getContext("2d");
	window.myPie = new Chart(ctx).Pie(crimePieData);
}

function loadRoadCallback(data)
{
	// Clear
	for (classification in poiMarkers)
	{
        for (c in poiMarkers[classification])
        {
            for (index in poiMarkers[classification][c])
            {
                poiMarkers[classification][c][index].setMap(null);
            }
        }
    }
    for (classification in poiPolygons)
	{
        for (c in poiPolygons[classification])
        {
            for (index in poiPolygons[classification][c])
            {
                poiPolygons[classification][c][index].setMap(null);
            }
        }
	}
	
	poiMarkers = {};
	poiPolygons = {};

	for (classification in poiAllMarkers)
	{
        for (c in poiAllMarkers[classification])
        {
            for (index in poiAllMarkers[classification][c])
            {
                poiAllMarkers[classification][c][index].setMap(null);
            }
        }
    }
    for (classification in poiAllPolygons)
	{
        for (c in poiAllPolygons[classification])
        {
            for (index in poiAllPolygons[classification][c])
            {
                poiAllPolygons[classification][c][index].setMap(null);
            }
        }
	}

	poiAllMarkers = {};
	poiAllPolygons = {};
	
	var roadData = data['roads'];
	var points = [];
	for (var p in roadData['points'])
	{
		point = {};
		point['lat'] = roadData['points'][p][0];
		point['lng'] = roadData['points'][p][1];
		points.push(point);
	}
	
	streetData = new google.maps.Polyline({
		path: points,
		geodesic: true,
		strokeColor: '#FF0000',
		strokeOpacity: 1.0,
		strokeWeight: 2
	});

	showStreet();
	
	var poi_data = data['pois'];
	var closest_poi_data = data['closest_pois'];
		
	var poi_content = document.getElementById("poi-content");
	poi_content.innerHTML = '';
	
	var poiList = document.createElement('table');
	poiList.setAttribute('class', 'data-table');
	
	var poiTitleElement = document.createElement('tr');

	var title1 = document.createElement('th');
	title1.setAttribute('class', 'text');
	title1.innerHTML = "Class";
	
	var title2 = document.createElement('th');
	title2.setAttribute('class', 'text');
	title2.innerHTML = "Type";
	
	var title3 = document.createElement('th');
	title3.setAttribute('class', 'value');
	title3.innerHTML = "Count";
	
	var title4 = document.createElement('th');
	title4.setAttribute('class', 'distance');
	title4.innerHTML = "Closest";
	
	var title5 = document.createElement('th');
	title5.setAttribute('class', 'average_distance');
	title5.innerHTML = "Average";
	
	poiTitleElement.appendChild(title1);
	poiTitleElement.appendChild(title2);
	poiTitleElement.appendChild(title3);
	poiTitleElement.appendChild(title4);
	poiTitleElement.appendChild(title5);
	poiList.appendChild(poiTitleElement);
	
	var even = false;
	
	for (var classification in poi_data)
	{
	    poiMarkers[classification] = {};
        poiPolygons[classification] = {};

        poiAllMarkers[classification] = {};
        poiAllPolygons[classification] = {};

	    for (var c in poi_data[classification])
	    {
	        var preferred = inPreferredList(c);
            // if (!inPreferredList(c)) continue;

            if (preferred)
            {
                poiMarkers[classification][c] = [];
                poiPolygons[classification][c] = [];
            }

            poiAllMarkers[classification][c] = [];
            poiAllPolygons[classification][c] = [];

            var poi_count = poi_data[classification][c].length;

            for (poi_d in poi_data[classification][c])
            {
                poi_points = poi_data[classification][c][poi_d]["points"];
                if (poi_points.length == 1)
                {
                    if (preferred)
                    {
                        var preferredMarker = new google.maps.Marker({
                            position: new google.maps.LatLng(poi_points[0][0], poi_points[0][1]),
                            title: c,
                            icon: marker_icons[classification],
                            map: map,
                            poi_info: poi_data[classification][c][poi_d]
                        });
                        google.maps.event.addListener(preferredMarker, 'click', function() {
                            createMarkerInfoWindow(this);
                          });
                        poiMarkers[classification][c].push(preferredMarker);
                    }
                    var allMarker = new google.maps.Marker({
                        position: new google.maps.LatLng(poi_points[0][0], poi_points[0][1]),
                        title: c,
                        icon: marker_icons[classification],
                        map: map,
                            poi_info: poi_data[classification][c][poi_d]
                    });
                    google.maps.event.addListener(allMarker, 'click', function() {
                            createMarkerInfoWindow(this);
                          });
                    poiAllMarkers[classification][c].push(allMarker);
                }
                else
                {
                    var areaPoints = [];
                    for (index in poi_points)
                    {
                        areaPoints.push(new google.maps.LatLng(poi_points[index][0], poi_points[index][1]))
                    }
                    if (preferred)
                    {
                        var preferredPolygon = new google.maps.Polygon({
                            path: areaPoints,
                            geodesic: true,
                            strokeColor: polygon_colors[classification],
                            strokeOpacity: 1.0,
                            strokeWeight: 2,
                            fillColor: polygon_colors[classification],
                            fillOpacity: 0.35,
                            map: map,
                            poi_info: poi_data[classification][c][poi_d]
                        });
                        google.maps.event.addListener(preferredPolygon, 'click', function() {
                            createPolygonInfoWindow(this, event);
                          });
                        poiPolygons[classification][c].push(preferredPolygon);
                    }
                    var allPolygon = new google.maps.Polygon({
                        path: areaPoints,
                        geodesic: true,
                        strokeColor: polygon_colors[classification],
                        strokeOpacity: 1.0,
                        strokeWeight: 2,
                        fillColor: polygon_colors[classification],
                        fillOpacity: 0.35,
                        map: map,
                            poi_info: poi_data[classification][c][poi_d]
                    });
                    google.maps.event.addListener(allPolygon, 'click', function() {
                            createPolygonInfoWindow(this, event);
                          });
                    poiAllPolygons[classification][c].push(allPolygon);
                }
            }
            showPOIs();
            showAllPOIs();

            var poiElement = document.createElement('tr');

            if (even)
            {
                poiElement.setAttribute('class', 'data-row-even');
            }
            else
            {
                poiElement.setAttribute('class', 'data-row-odd');
            }
            even = !even;

            var classText = document.createElement('td');
            classText.setAttribute('class', 'text');
            classText.innerHTML = classification;

            var text = document.createElement('td');
            text.setAttribute('class', 'text');
            text.innerHTML = c;

            var value = document.createElement('td');
            value.setAttribute('class', 'value');
            value.innerHTML = poi_count;

            var distanceElement = document.createElement('td');
            distanceElement.setAttribute('class', 'distance');
            if (c in closest_poi_data[classification] && 'distance' in closest_poi_data[classification][c])
            {
                distanceElement.innerHTML = Math.round(closest_poi_data[classification][c]['distance'] * 100) / 100;
                distanceElement.innerHTML += ' m';
            }
            else
            {
                distanceElement.innerHTML = '/';
            }

            var avgDistanceElement = document.createElement('td');
            avgDistanceElement.setAttribute('class', 'average_distance');
            if (c in closest_poi_data[classification] && 'average_distance' in closest_poi_data[classification][c])
            {
                avgDistanceElement.innerHTML = Math.round(closest_poi_data[classification][c]['average_distance'] * 100) / 100;
                avgDistanceElement.innerHTML += ' m';
            }
            else
            {
                avgDistanceElement.innerHTML = '/';
            }

            poiElement.appendChild(classText);
            poiElement.appendChild(text);
            poiElement.appendChild(value);
            poiElement.appendChild(distanceElement);
            poiElement.appendChild(avgDistanceElement);

            poiList.appendChild(poiElement);
		}
	}
	poi_content.appendChild(poiList);
}

function loadDetectionCallback(data)
{
	var detection_content = document.getElementById("detection-content");
	detection_content.innerHTML = '';
	
	var base_folder = "streetviewimages/";
	for (i in data)
	{
		point_data = data[i];
		for (detected_img in point_data['detections'])
		{
			fname = point_data['detections'][detected_img];
			imageElement = document.createElement('img');
			imageElement.setAttribute('src', base_folder + fname);	
			
			detection_content.appendChild(imageElement);
		}
	}
}

function loadSSO(familyId)
{
	contentDiv = document.getElementById('sso-content');
	contentDiv.innerHTML = '';
	
	var ssoList = document.createElement('table');
	ssoList.setAttribute('class', 'data-table');
	
	// Heading
	var ssoTitleElement = document.createElement('tr');
	var title1 = document.createElement('th');
	title1.setAttribute('class', 'text');
	title1.innerHTML = "SSO Type";
	var title2 = document.createElement('th');
	title2.setAttribute('class', 'value');
	title2.innerHTML = "Value";
	ssoTitleElement.appendChild(title1);
	ssoTitleElement.appendChild(title2);
	ssoList.appendChild(ssoTitleElement);

	if (typeof SSO_DATA === 'undefined' || typeof SSO_DATA[familyId] === 'undefined')
	{
		contentDiv.innerHTML = '<div class=\'no-data-content\'>No data available</div>';
		return;
	}
	var data = SSO_DATA[familyId];	
	var even = false;
	
	for (var key in SSO_STRUCTURE)
	{
		var ssoElement = document.createElement('tr');
		if (even)
		{
			ssoElement.setAttribute('class', 'data-row-even');
		}
		else
		{
			ssoElement.setAttribute('class', 'data-row-odd');
		}
		even = !even;
		
		var ssoDescription = key;
		if(SSO_VARIABLES.hasOwnProperty(key))
		{
			ssoDescription = SSO_VARIABLES[key]["description"];
		}
		var img = document.createElement('img');
		if (SSO_STRUCTURE[key].length > 0)
		{
			img.setAttribute('src', 'img/more.png');
		}
		else
		{
			img.setAttribute('src', 'img/empty.png');
		}
		img.setAttribute('align', 'bottom');
		
		var text = document.createElement('td');
		text.appendChild(img);
		text.setAttribute('class', 'text');
		text.innerHTML += ssoDescription;
		
		var dataValue = '/';
		if (data.hasOwnProperty(key) && data[key] != "")
		{
			dataValue = data[key];
		}
		var value = document.createElement('td');
		value.setAttribute('class', 'value');
		value.innerHTML = dataValue;
		
		ssoElement.appendChild(text);
		ssoElement.appendChild(value);
		
		ssoList.appendChild(ssoElement);
		
		if (SSO_STRUCTURE[key].length > 0)
		{
			var id = key + "-subtable";
			ssoElement.setAttribute('onclick', 'toggleSubTable(\'' + id +'\',this);');
			
			var subTableElement = document.createElement('table');
			subTableElement.setAttribute('class', 'sub-data-table');
		
			for (var subkey in SSO_STRUCTURE[key])
			{
				var subElement = document.createElement('tr');
				
				var subkeyDescription = SSO_STRUCTURE[key][subkey];
				if(SSO_VARIABLES.hasOwnProperty(subkeyDescription))
				{
					subkeyDescription = SSO_VARIABLES[subkeyDescription]["description"];
				}
				
				var subkeyText = document.createElement('td');
				subkeyText.setAttribute('class', 'text');
				subkeyText.innerHTML = subkeyDescription;
				
				var subDataValue = '/';
				if (data.hasOwnProperty(key) && data[key] != "")
				{
					subDataValue = data[key];
				}
				var subkeyValue = document.createElement('td');
				subkeyValue.innerHTML = subDataValue;
				
				subElement.appendChild(subkeyText);
				subElement.appendChild(subkeyValue);
				subTableElement.appendChild(subElement);
			}
			
			
			var subtableRow = document.createElement('tr');
			subtableRow.setAttribute('id', id);
			subtableRow.setAttribute('class', 'sub-data-table-row-hidden');
			
			var subtableData = document.createElement('td');
			subtableData.setAttribute("colspan", "2");
			
			subtableData.appendChild(subTableElement);
			subtableRow.appendChild(subtableData);
			ssoList.appendChild(subtableRow);
		}
	}
	
	contentDiv.appendChild(ssoList);
}

function loadCrime(familyId)
{
	var crime_content = document.getElementById("crime-content");
	crime_content.innerHTML = '<div class=\'no-data-content\'>No data available</div>';
	
	if (crimeScriptElement != null)
	{
		document.head.removeChild(crimeScriptElement);
		delete crimeScriptElement;
	}
	
	var scriptName = "data/crimes/police-data-" + familyId + ".js";
	var element = document.createElement('script');
	element.setAttribute("type","text/javascript");
	element.setAttribute("src", scriptName);
	document.getElementsByTagName('head')[0].appendChild(element);
	
	crimeScriptElement = element;
}

function loadRoad(familyId)
{
	var poi_content = document.getElementById("poi-content");
	poi_content.innerHTML = '<div class=\'no-data-content\'>No data available</div>';
	
	if (roadScriptElement != null)
	{
		document.head.removeChild(roadScriptElement);
		delete roadScriptElement;
	}
	
	var scriptName = "data/roads/road-data-" + familyId + ".js";
	var element = document.createElement('script');
	element.setAttribute("type","text/javascript");
	element.setAttribute("src", scriptName);
	document.getElementsByTagName('head')[0].appendChild(element);
	
	roadScriptElement = element;
}

function loadDetection(familyId)
{
	var detection_content = document.getElementById("detection-content");
	// detection_content.innerHTML = '<div class=\'no-data-content\'>No data available</div>';
	detection_content.innerHTML = '';
	
	if (detectionScriptElement != null)
	{
		document.head.removeChild(detectionScriptElement);
		delete detectionScriptElement;
	}
	
	var scriptName = "data/detection/detection-data-" + familyId + ".js";
	var element = document.createElement('script');
	element.setAttribute("type","text/javascript");
	element.setAttribute("src", scriptName);
	document.getElementsByTagName('head')[0].appendChild(element);
	
	detectionScriptElement = element;
}

function loadCurrentFamily()
{
	if (areaData)
	{
		areaData.setMap(null);
		areaData = null;
	}
	if(heatmap)
	{
		heatmap.setMap(null);
		heatmap = null;
	}
	if(localHeatmap)
	{
		localHeatmap.setMap(null);
		localHeatmap = null;
	}
	
	var currentId = familyIds[currentPosition];
	document.getElementById("family-id").value = currentId;
	
	var locationLat = LOCATION_DATA[currentId]['latitude'];
	var locationLng = LOCATION_DATA[currentId]['longitude'];
	var location = new google.maps.LatLng(locationLat, locationLng);
	
	if (marker == null)
	{
		marker = new google.maps.Marker();
		marker.setMap(map);
	}
	marker.setPosition(location);
	marker.setTitle(currentId);
	
    map.panTo(marker.getPosition());
	
	loadSSO(currentId);
	
	loadCrime(currentId);
	
	loadRoad(currentId);
	
	loadDetection(currentId);
	
	drawArea(parseFloat(locationLat), parseFloat(locationLng));
}

function enableButtons()
{
	if (currentPosition == 0)
	{
		document.getElementById("prev-family").disabled = true;
		document.getElementById("next-family").disabled = false;
	}
	else if (currentPosition == (familyIds.length - 1))
	{
		document.getElementById("prev-family").disabled = false;
		document.getElementById("next-family").disabled = true;
	}
	else
	{
		document.getElementById("prev-family").disabled = false;
		document.getElementById("next-family").disabled = false;
	}
}

function previousFamily()
{
	if (currentPosition > 0)
	{
		currentPosition -= 1;
	}
	enableButtons();
	loadCurrentFamily();
}

function nextFamily()
{
	if (currentPosition < familyIds.length)
	{
		currentPosition += 1;
	}
	enableButtons();
	loadCurrentFamily();
}

function skipToFamily(id)
{
	for (f in familyIds)
	{
		if (familyIds[f] == id)
		{
			currentPosition = f;
			enableButtons();
			loadCurrentFamily();
			return;
		}
	}
	alert('Family ID not found!');
	document.getElementById('family-id').value = familyIds[currentPosition];
}

function showData(id)
{
	for (var key in contentIds)
	{
		var content = contentIds[key] + "-content";
		var menu = contentIds[key] + "-title";
		var element = document.getElementById(content);
		var menuElement = document.getElementById(menu);
		if (contentIds[key] == id)
		{
			element.setAttribute('class', 'data-content-item');
			menuElement.setAttribute('class', 'data-menu-item-selected');
		}
		else
		{
			element.setAttribute('class', 'data-content-item-hidden');
			menuElement.setAttribute('class', 'data-menu-item');
		}
	}
}

function showStreet()
{
	if (streetVisible)
	{
		streetData.setMap(map);
	}
	else
	{
		streetData.setMap(null);
	}
}

function showHeatmap()
{
	if (heatmap != null)
	{
		if (heatmapVisible)
		{
			heatmap.setMap(map);
		}
		else
		{
			heatmap.setMap(null);
		}
	}
}

function showLocalHeatmap()
{
	if (localHeatmap != null)
	{
		if (localHeatmapVisible)
		{
			localHeatmap.setMap(map);
		}
		else
		{
			localHeatmap.setMap(null);
		}
	}
}

function showNeighbourhood()
{
	if (areaData != null)
	{
		if (neighbourhoodVisible)
		{
			areaData.setMap(map);
		}
		else
		{
			areaData.setMap(null);
		}
	}
}

function showPOIs()
{
	var toSetMap = null;
	if (poisVisible)
	{
		toSetMap = map;
	}
	for (classification in poiMarkers)
	{
        for (c in poiMarkers[classification])
        {
            for (index in poiMarkers[classification][c])
            {
                poiMarkers[classification][c][index].setMap(toSetMap);
            }
        }
    }
    for (classification in poiPolygons)
	{
        for (c in poiPolygons[classification])
        {
            for (index in poiPolygons[classification][c])
            {
                poiPolygons[classification][c][index].setMap(toSetMap);
            }
        }
    }
    toggleLegend(poisVisible, poisAllVisible);
}

function showAllPOIs()
{
	var toSetMap = null;
	if (poisAllVisible)
	{
		toSetMap = map;
	}
	for (classification in poiAllMarkers)
	{
        for (c in poiAllMarkers[classification])
        {
            for (index in poiAllMarkers[classification][c])
            {
                poiAllMarkers[classification][c][index].setMap(toSetMap);
            }
        }
    }
    for (classification in poiAllPolygons)
	{
        for (c in poiAllPolygons[classification])
        {
            for (index in poiAllPolygons[classification][c])
            {
                poiAllPolygons[classification][c][index].setMap(toSetMap);
            }
        }
    }
    toggleLegend(poisVisible, poisAllVisible);
}

function togglePOIs()
{
	poisVisible = !poisVisible;
	if (poisVisible && poisAllVisible)
	{
		poisAllVisible = false;
	}
	showPOIs();
	showAllPOIs();
}

function toggleAllPOIs()
{
    poisAllVisible = !poisAllVisible;
	if (poisVisible && poisAllVisible)
	{
		poisVisible = false;
	}
	showPOIs();
	showAllPOIs();
}

function toggleStreet()
{
	streetVisible = !streetVisible;
	showStreet();
}

function toggleHeatmap()
{
	heatmapVisible = !heatmapVisible;
	if (heatmapVisible && localHeatmapVisible)
	{
		localHeatmapVisible = false;
	}
	showHeatmap();
	showLocalHeatmap();
}

function toggleLocalHeatmap()
{
	localHeatmapVisible = !localHeatmapVisible;
	if (heatmapVisible && localHeatmapVisible)
	{
		heatmapVisible = false;
	}
	showHeatmap();
	showLocalHeatmap();
}

function toggleNeighbourhood()
{
	neighbourhoodVisible = !neighbourhoodVisible;
	showNeighbourhood();
}

function toggleSubTable(id, sender)
{
	var element = document.getElementById(id);
	if(element)
	{
		var style = element.getAttribute('class');
		var img = sender.getElementsByTagName('img')[0];
		if (style == "sub-data-table-row-hidden")
		{
			element.setAttribute('class', 'sub-data-table-row');
			img.setAttribute('src', 'img/less.png');
		}
		else
		{
			element.setAttribute('class', 'sub-data-table-row-hidden');
			img.setAttribute('src', 'img/more.png');
		}
	}
}

function toggleLegend(visible, visibleAll)
{
    var element = document.getElementById('legend');
	if(element)
	{
	    if (visible || visibleAll)
	        element.setAttribute('class', 'legend-visible');
	    else
	        element.setAttribute('class', 'legend-hidden');
	}
}



function createMarkerInfoWindow(marker)
{
    if(infowindow)
    {
        infowindow.setMap(null);
        infowindow = null;
    }
    poi_info = marker['poi_info'];
    var contentString = "";
    for (var tag in poi_info['tags'])
    {
        contentString += tag + ': ' + poi_info['tags'][tag] + '<br/>';
    }
    contentString += 'distance: ' + poi_info['distance'];
    infowindow = new google.maps.InfoWindow({
        content: contentString
      });
      infowindow.open(map, marker);
}

function createPolygonInfoWindow(polygon, event)
{
    if(infowindow)
    {
        infowindow.setMap(null);
        infowindow = null;
    }
    poi_info = polygon['poi_info'];
    var contentString = "";
    for (var tag in poi_info['tags'])
    {
        contentString += tag + ': ' + poi_info['tags'][tag] + '<br/>';
    }
    contentString += 'distance: ' + poi_info['distance'];

    var bounds = new google.maps.LatLngBounds();
    var polygonCoords = polygon.getPath();
    for (i = 0; i < polygonCoords.getLength(); i++) {
        bounds.extend(polygonCoords.getAt(i));
    }
    infowindow = new google.maps.InfoWindow;
    infowindow.setContent(contentString);
    infowindow.setPosition(bounds.getCenter());
    infowindow.open(map);
}