

SSO_STRUCTURE =
{
	"SSO_PdisorderC": ["GARBAGE_first", "ABDNCARS_first", "GRAFFITI_first", "GRAFREMO_first", "SGNSVAND_first"],
	"SSO_PdecayC": [],
	"SSO_NightUnsafe": [],
	"SSO_NEIGHSAFEr": [],
	"SSO_UNSAFEneigh": [],
	"SSO_StreetSAFE": [],
	"SSO_neighKids": [],
	"SSO_AmmenCNT": [],
	"SSO_publicCNT": [],
	"SSO_ABDNCARSr": []
};

/*SSO_STRUCTURE =
{
	??
		
	"SSO_PdecayC"
	"SSO_NightUnsafe"
	"SSO_NEIGHSAFEr"
	"SSO_UNSAFEneigh"
	
	"SSO_neighKids"
	
	"SSO_publicCNT"
	"SSO_ABDNCARSr"
	??
	"SSO_StreetSAFE": ["STRTPTRN_first", "STRTCOND_first", "STRTLGHT_first", "SDWKLITE_first", "TRFFCALM_first", "SPDLMT_first", "TRFLMT_first", "CROSWALK_first", "BIKELANE_first", "SPDHUMPS_first"],
	"Sidewalk?": ["SDWKCOND_first", "SDWKTREE_first", "SDWKCURB_first"],
	"SSO_PdisorderC": ["GARBAGE_first", "ABDNCARS_first", "GRAFFITI_first", "GRAFREMO_first", "SGNSVAND_first"],
	"SSO_AmmenCNT": ["AMENITIE_first", "TRASHCAN_first", "CYCLEBIN_first", "PHONE_first", "NEWSPAPR_first", "RESTROOM_first", "VENDMACH_first", "BENCHES_first", "BUSSTOP_first", "BIKERACK_first", "BIKEPATH_first", "TUBEENTR_first", "TUBECOND_first"],
	"Types of buildings?": ["RESID_first", "COMBISN_first", "INDUST_first", "VACLOT_first", "INTST_first", "RECFACIL_first"],
	"Residential Land usage?": ["DETACHED_first", "SMDTCHD_first", "TERRACE_first", "MNSNBLCK_first", "LRPF_first", "LRCE_first", "TBCE_first", "RESDBARS_first", "RESDABND_first", "RESDBALC_first", "RESDRATE_first", "RESDDETER_first", "GARDCOND_first", "GARDSECUR_first", "GARDDETER_first", "RESDDRWY_first"],
	"Commercial and Business land use": ["CHURCH_first", "SCHOOL_first", "DAYCARE_first", "LIBRARY_first", "HEALSERV_first", "POLICE_first", "LEISCENT_first", "FRESHMKT_first", "CORNSTOR_first", "LEGROC_first", "HESUPMKT_first", "BTCHSHOP_first", "FASTFOOD_first", "LOCALPUB_first", "CARWASH_first", "POUNDSHP_first", "BOUTIQUE_first", "PUBTYPE_first", "BISNSECR_first", "BISNABDN_first", "BISNGATE_first", "BISNFENC_first", "BISNCOND_first", "BISNPOOR_first"],
	"Recreational Facilities": ["PARK_first", "COUNPARK_first", "PLAYEQUP_first", "SPRTFILD_first", "SPRTSTND_first", "POOL_first", "RECCENTR_first", "TABLES_first", "TRAILS_first", "RECFCOND_first"],
	"Vacant lots": ["VLOTCOND_first"],
	"Signs": ["SIGNS_first", "CRMWATCH_first", "ALRMSYST_first", "BEWRDOG_first", "CHLDPLY_first", "NOLITTER_first", "ADVTBEER_first", "ADVTGAMB_first", "ADVTFSFD_first", "MUTPLANG_first", "EDUCSAY_first", "DRUGFREE_first", "NOBALL_first", "PLAYAREA_first", "PETLITER_first", "SIGNVLOT_first", "SIGNUNRD_first", "SIGNVAND_first"],
	"People": ["PEOPLE_first", "CHILDREN_first", "LOITER_first", "KIDACTIV_first", "WALKING_first", "FRNTHOME_first", "FRNTBISN_first", "WAITBUS_first"],
	"Overal condition": ["NEIGHSAFE_first", "CARQLTY_first", "NEIGHNIGHT_first", "LUXVECH_first", "CHARWLTH_first", "CHARMINR_first", "NEIGHLIVE_first"],
	"GSV": ["GSVWTHR_first", "GSVTIME_first", "GSVANMO_first", "BISFAIL_first", "RECFAIL_first", "RESFAIL_first", "VLOTFAIL_first", "N_first", "GARBAGEr", "GRAFFITIr", "GRAFREMOr", "SGNSVANDr"],
	"Other": ["PdisorderMISS", "streetcondr", "SDWKCONDr", "RESDDETERr", "GARDDETERr", "RECFCONDr", "BISNPOORr", "VLOTCONDr", "VLOTCONDr2", "StreetMISS", "PdecayMISS"]
};*/

SSO_VARIABLES =
{
	"SSO_PdisorderC":
	{
		"description": "SSO - Physical disorder - count of items",
	},
	"SSO_PdecayC":
	{
		"description": "SSO - physical decay - count of items"
	},
	"SSO_NightUnsafe":
	{
		"description": "SSO - Feel unsafe walking in neighborhood at night - binary recode"
	},
	"SSO_NEIGHSAFEr":
	{
		"description": "SSO - Neighborhoood unsafe - binary recode"
	},
	"SSO_UNSAFEneigh":
	{
		"description": "SSO - Unsafe neighborhood - average of unsafe neigh and unsafe walking at night"
	},
	"SSO_StreetSAFE":
	{
		"description": "SSO - Street safety - count of street safety measures"
	},
	"SSO_neighKids":
	{
		"description": "SSO - Kids present in the neighborhood or signs of kids activities"
	},
	"SSO_AmmenCNT":
	{
		"description": "SSO - Count of different types of amenities"
	},
	"SSO_publicCNT":
	{
		"description": "SSO - Count of public courtesies available on street"
	},
	"SSO_ABDNCARSr":
	{
		"description": "SSO - Abandoned cars present on the street?"
	},
	"STRTPTRN_first":
	{
		"description": "Street PatternLayout1"
	},
	"STRTCOND_first":
	{
		"description": "Condition of the street15"
	},
	"STRTLGHT_first":
	{
		"description": "Is there outdoor lighting illuminating the street4"
	},
	"SDWKLITE_first":
	{
		"description": "Based on the characteristics of this blocks street lights estimate the percentage of illumination on the street at night"
	},
	"TRFFCALM_first":
	{
		"description": "Are there any traffic calming measures visible on the street"
	},
	"SPDLMT_first":
	{
		"description": "Speed Limit Signs24"
	},
	"TRFLMT_first":
	{
		"description": "Signs Limiting Traffic Type ie No Trucks Allowed"
	},
	"CROSWALK_first":
	{
		"description": "Crosswalk or Signs Signaling to Watch for Pedestrians Crossing Street ie School Crossing Elderly Crossing24"
	},
	"BIKELANE_first":
	{
		"description": "Designated Bike Lane Sign or Painted Street Markers4"
	},
	"SPDHUMPS_first":
	{
		"description": "Speed Reducing Humps4"
	},
	"SDWKCOND_first":
	{
		"description": "Condition of the sidewalk15"
	},
	"SDWKTREE_first":
	{
		"description": "Are there trees along the street between the sidewalk and the street15"
	},
	"SDWKCURB_first":
	{
		"description": "Is there a dropped curb between the sidewalk and the street"
	},
	"GARBAGE_first":
	{
		"description": "Is there strewn garbage litter broken glass clothes or papers on the block face in the streetsidewalkor public space5"
	},
	"ABDNCARS_first":
	{
		"description": "Are there abandoned cars cars with broken windows andor run down cars1"
	},
	"GRAFFITI_first":
	{
		"description": "Is there graffiti on buildings signs or walls1"
	},
	"GRAFREMO_first":
	{
		"description": "Is there evidence of graffiti that has been painted over1"
	},
	"SGNSVAND_first":
	{
		"description": "Do any of the street signs appear to be almost unreadable due to being badly faded or vandalized2"
	},
	"AMENITIE_first":
	{
		"description": "Are there any amenities on this street"
	},
	"TRASHCAN_first":
	{
		"description": "Trash cans nonresidential2"
	},
	"CYCLEBIN_first":
	{
		"description": "Recycling bins nonresidential"
	},
	"PHONE_first":
	{
		"description": "Public phones2"
	},
	"NEWSPAPR_first":
	{
		"description": "Newspaper dispenser2"
	},
	"RESTROOM_first":
	{
		"description": "Restrooms3"
	},
	"VENDMACH_first":
	{
		"description": "Vending machines3"
	},
	"BENCHES_first":
	{
		"description": "Benches not a bus stop chairs andor ledges for sitting3"
	},
	"BUSSTOP_first":
	{
		"description": "Bus stops with seating3"
	},
	"BIKERACK_first":
	{
		"description": "Bike racks3"
	},
	"BIKEPATH_first":
	{
		"description": "Is there a bike path or sign indicating a bike path visible"
	},
	"TUBEENTR_first":
	{
		"description": "Is there a tube entrance or a train station on this street"
	},
	"TUBECOND_first":
	{
		"description": "In general how would you rate the condition of the tube entrancetrain station of the street segment"
	},
	"RESID_first":
	{
		"description": "Residential"
	},
	"COMBISN_first":
	{
		"description": "CommercialBusiness"
	},
	"INDUST_first":
	{
		"description": "Industrial Warehouse Manufacturing"
	},
	"VACLOT_first":
	{
		"description": "Vacant Lots or Open Space"
	},
	"INTST_first":
	{
		"description": "Institutional schools churches etc"
	},
	"RECFACIL_first":
	{
		"description": "Recreational Facilities Parks or Playgrounds"
	},
	"DETACHED_first":
	{
		"description": "Detached"
	},
	"SMDTCHD_first":
	{
		"description": "SemiDetached"
	},
	"TERRACE_first":
	{
		"description": "Terrace"
	},
	"MNSNBLCK_first":
	{
		"description": "Mansion blocks"
	},
	"LRPF_first":
	{
		"description": "Lowrise private flats"
	},
	"LRCE_first":
	{
		"description": "Lowrise Council estate"
	},
	"TBCE_first":
	{
		"description": "Tower block council estate"
	},
	"RESDBARS_first":
	{
		"description": "Are there any residential units that have bargratings on residential doors or windows1"
	},
	"RESDABND_first":
	{
		"description": "Are there any residential units that appear to be burned out boarded up or abandoned12"
	},
	"RESDBALC_first":
	{
		"description": "Are there any residential units where the balconies are poorly kept or cluttered with personal effects12"
	},
	"RESDRATE_first":
	{
		"description": "In general how would you rate the condition of most of the residential units in the block face1"
	},
	"RESDDETER_first":
	{
		"description": "Are there ANY residential units on the street that appear to be in poorbadly deteriorated condition"
	},
	"GARDCOND_first":
	{
		"description": "In general how would you rate the condition of MOST of the residential front gardens on the block face2"
	},
	"GARDSECUR_first":
	{
		"description": "Are there any residential front gardens on the street that appear to have security measures such as barbed wire or broke"
	},
	"GARDDETER_first":
	{
		"description": "Are there any residential front gardens on the street that appear to be in poorbadly deteriorated condition"
	},
	"RESDDRWY_first":
	{
		"description": "What is the percentage of residential units on this street have private driveways"
	},
	"CHURCH_first":
	{
		"description": "Church or Community Center1"
	},
	"SCHOOL_first":
	{
		"description": "Elementary or Secondary School or Religious School"
	},
	"DAYCARE_first":
	{
		"description": "Day care or preschool3"
	},
	"LIBRARY_first":
	{
		"description": "Library"
	},
	"HEALSERV_first":
	{
		"description": "Health or social services3"
	},
	"POLICE_first":
	{
		"description": "Police department or fire department3"
	},
	"LEISCENT_first":
	{
		"description": "Leisure centre"
	},
	"FRESHMKT_first":
	{
		"description": "Organic grocerFresh food marketstand1"
	},
	"CORNSTOR_first":
	{
		"description": "Corner stores SainsburyTesco"
	},
	"LEGROC_first":
	{
		"description": "Low end grocery stores TOT Iceland"
	},
	"HESUPMKT_first":
	{
		"description": "High end supermarket Waitrose"
	},
	"BTCHSHOP_first":
	{
		"description": "Butchers shop"
	},
	"FASTFOOD_first":
	{
		"description": "Fast foodTake out restaurant1 Fried chicken outlets"
	},
	"LOCALPUB_first":
	{
		"description": "Local pub"
	},
	"CARWASH_first":
	{
		"description": "Hand car washes"
	},
	"POUNDSHP_first":
	{
		"description": "Pound shops"
	},
	"BOUTIQUE_first":
	{
		"description": "Boutiques independent shops"
	},
	"PUBTYPE_first":
	{
		"description": "What type of pub is visible"
	},
	"BISNSECR_first":
	{
		"description": "Are there any commercial or industrial properties that have bargratings on doors or windows1"
	},
	"BISNABDN_first":
	{
		"description": "Are there any commercial or industrial properties that appear to be burned out boarded up or abandoned12"
	},
	"BISNGATE_first":
	{
		"description": "Are there any commercial or industrial properties that appear to have pull down metal security blinds grills or iron gat"
	},
	"BISNFENC_first":
	{
		"description": "Are there any commercial or industrial properties with metal fencing over head height1"
	},
	"BISNCOND_first":
	{
		"description": "In general how would you rate the condition of most of the commercial or industrial units in the block face1"
	},
	"BISNPOOR_first":
	{
		"description": "Are there any commercial or industrial units on the street that appear to be in poorbadly deteriorated condition"
	},
	"PARK_first":
	{
		"description": "Park"
	},
	"COUNPARK_first":
	{
		"description": "Council Park"
	},
	"PLAYEQUP_first":
	{
		"description": "Playground equipment ieslide swings"
	},
	"SPRTFILD_first":
	{
		"description": "Sportsplaying fieldscourts"
	},
	"SPRTSTND_first":
	{
		"description": "Sports standsseating"
	},
	"POOL_first":
	{
		"description": "Pools"
	},
	"RECCENTR_first":
	{
		"description": "Recreation Centre"
	},
	"TABLES_first":
	{
		"description": "Tables andor grills"
	},
	"TRAILS_first":
	{
		"description": "Bikewalking trails"
	},
	"RECFCOND_first":
	{
		"description": "In general how would you rate the condition of recreational facilities in the block face1"
	},
	"VLOTCOND_first":
	{
		"description": "In general how would you rate the condition of vacant lots andor open spaces in the block face5"
	},
	"SIGNS_first":
	{
		"description": "Does this street segment contains signs"
	},
	"CRMWATCH_first":
	{
		"description": "Neighborhood crime watch signs1"
	},
	"ALRMSYST_first":
	{
		"description": "Alarm systemSecurity warning signs1"
	},
	"BEWRDOG_first":
	{
		"description": "Beware of dog1"
	},
	"CHLDPLY_first":
	{
		"description": "Thanks for driving slowlyChildren at play"
	},
	"NOLITTER_first":
	{
		"description": "Thanks for not littering"
	},
	"ADVTBEER_first":
	{
		"description": "Sign advertising beer whiskey or other alcohol not labeling for business1"
	},
	"ADVTGAMB_first":
	{
		"description": "Sign advertising gamblingslot machines"
	},
	"ADVTFSFD_first":
	{
		"description": "Sign advertising fast food not labeling for business1"
	},
	"MUTPLANG_first":
	{
		"description": "Signs in multiple languages5"
	},
	"EDUCSAY_first":
	{
		"description": "Inspirationaleducation sayings2"
	},
	"DRUGFREE_first":
	{
		"description": "Drug Free Zone2"
	},
	"NOBALL_first":
	{
		"description": "No ball games or signs restricting children from playing"
	},
	"PLAYAREA_first":
	{
		"description": "Play Priority Area or signs that encourage use of vacant space"
	},
	"PETLITER_first":
	{
		"description": "Pick up your pet litter"
	},
	"SIGNVLOT_first":
	{
		"description": "Are there any signs for promoting organized community activities"
	},
	"SIGNUNRD_first":
	{
		"description": "This street segment contains visible signs but they are unable to be coded due to unreadable or blurry text"
	},
	"SIGNVAND_first":
	{
		"description": "This street segment contains visible signs but they are unable to be coded due to vandalism"
	},
	"PEOPLE_first":
	{
		"description": "Are people visible on the block face1"
	},
	"CHILDREN_first":
	{
		"description": "Are any children visible on the block face1"
	},
	"LOITER_first":
	{
		"description": "Is there any evidence of people 2 or more loitering on the street eg just hanging out or congregating for no apparent re"
	},
	"KIDACTIV_first":
	{
		"description": "Is there any evidence of kids participating in physical activities in the neighborhood eg playing ball games skateboardi"
	},
	"WALKING_first":
	{
		"description": "Walking to a destination2"
	},
	"FRNTHOME_first":
	{
		"description": "In front of home ie front garden or vehicle2"
	},
	"FRNTBISN_first":
	{
		"description": "In front of a business2"
	},
	"WAITBUS_first":
	{
		"description": "Waiting for a bus2"
	},
	"NEIGHSAFE_first":
	{
		"description": "This neighborhood appears to be a safe place to live"
	},
	"CARQLTY_first":
	{
		"description": "How would you rate the quality of the majority of cars visible on this street"
	},
	"NEIGHNIGHT_first":
	{
		"description": "I would feel safe walking in this neighborhood at night"
	},
	"LUXVECH_first":
	{
		"description": "What is the percentage of cars that appear to be high end luxury vehicles in this neighborhood"
	},
	"CHARWLTH_first":
	{
		"description": "The houses in this neighborhood appear to be best characterized as"
	},
	"CHARMINR_first":
	{
		"description": "This neighborhood appears to be an area best characterized by"
	},
	"NEIGHLIVE_first":
	{
		"description": "This is a neighborhood that I could live in"
	},
	"GSVWTHR_first":
	{
		"description": "For the block observed the weather at time at Google Street View captures appears to be"
	},
	"GSVTIME_first":
	{
		"description": "For the block observed the Google Street View capture appears to be taken at the following time of day"
	},
	"GSVANMO_first":
	{
		"description": "Does there appear to be any inconsistencies in the Google Street View images for this street segment"
	},
	"BISFAIL_first":
	{
		"description": "Are you absolutely positive that there are no CommercialBusiness units on this street"
	},
	"RECFAIL_first":
	{
		"description": "Are you absolutely positive that there are no Recreational Facilities units on this street"
	},
	"RESFAIL_first":
	{
		"description": "Are you absolutely positive that there are no residential units on this street"
	},
	"VLOTFAIL_first":
	{
		"description": "Are you absolutely positive that there are no Vacant Lots andor Open Spaces units on this street"
	},
	"N_first":
	{
		"description": "Number of raters for each neighborhood"
	},
	"GARBAGEr":
	{
		"description": "Garbage present on the street?"
	},
	"GRAFFITIr":
	{
		"description": "Graffitti present on the street?"
	},
	"GRAFREMOr":
	{
		"description": "Graffitti painted over present on the street?"
	},
	"SGNSVANDr":
	{
		"description": "Unreadable and faded signs present on the street?"
	},
	"PdisorderMISS":
	{
		"description": "Physical disorder - count of missing items"
	},
	"streetcondr":
	{
		"description": "Street condition - recode binary"
	},
	"SDWKCONDr":
	{
		"description": "Sidewalk condition - recode binary"
	},
	"RESDDETERr":
	{
		"description": "Reisdential units in poor/badly deteriorated condition - recode binary"
	},
	"GARDDETERr":
	{
		"description": "Reisdential gardens in poor/badly deteriorated condition - recode binary"
	},
	"RECFCONDr":
	{
		"description": "Recreational facilities in poor/bad condition - recode binary"
	},
	"BISNPOORr":
	{
		"description": "Commercial units in poor/badly deteriorated condition - recode binary"
	},
	"VLOTCONDr":
	{
		"description": "Vacant lots in fair/bad condition - recode binary"
	},
	"VLOTCONDr2":
	{
		"description": "Vacant lots in BAD condition - recode binary"
	},
	"StreetMISS":
	{
		"description": "Street safety - missing items"
	},
	"PdecayMISS":
	{
		"description": "physical decay - count of missing items"
	}
};