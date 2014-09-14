Durham, North Carolina GIS data
===============================

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --python=/usr/bin/python3.4 durham-gis
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements.txt


City and County Boundaries
--------------------------

To download, run::

    export GISROOT=http://gisweb2.ci.durham.nc.us/arcgis/rest/services
    python download.py --dest durham-county.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/2/query
    python download.py --dest durham-city-county.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/10/query
    python download.py --dest durham-parks.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/6/query


Centerlines
-----------

To download, run::

    export GISROOT=http://gisweb2.ci.durham.nc.us/arcgis/rest/services
    python download.py --dest durham-highways.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/3/query
    python download.py --dest durham-streets.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/4/query
    python download.py --dest durham-railroads.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/1/query
    python download.py --dest durham-trails.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/5/query


Points of Interest
------------------

To download, run::

    export GISROOT=http://gisweb2.ci.durham.nc.us/arcgis/rest/services
    python download.py --dest durham-parks.geojson $GISROOT/DurhamMaps/Parks/FeatureServer/0/query
    python download.py --dest durham-parks-areas.geojson $GISROOT/DurhamMaps/StreetBaseMap/MapServer/6/query


Durham Public Schools (DPS)
---------------------------

To download, run::

    export GISROOT=http://gisweb2.ci.durham.nc.us/arcgis/rest/services
    python download.py --dest schools/schools.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/0/query
    python download.py --dest schools/districts-middle.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/1/query
    python download.py --dest schools/districts-high.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/2/query
    python download.py --dest schools/districts-elementary.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/3/query
    python download.py --dest schools/districts-elementary-year-round.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/4/query
    python download.py --dest schools/districts-middle-year-round.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/5/query
    python download.py --dest schools/districts-elementary-magnet-walk.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/6/query
    python download.py --dest schools/districts-holt-easley.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/7/query


