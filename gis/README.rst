Durham GIS data
===============

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --python=/usr/bin/python3.4 durham-gis
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements.txt


Schools
-------

Download Durham Public School data::

    export GISROOT=http://gisweb2.ci.durham.nc.us/arcgis/rest/services
    python download.py --dest schools/schools.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/0/query
    python download.py --dest schools/districts-middle.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/1/query
    python download.py --dest schools/districts-high.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/2/query
    python download.py --dest schools/districts-elementary.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/3/query
    python download.py --dest schools/districts-elementary-year-round.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/4/query
    python download.py --dest schools/districts-middle-year-round.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/5/query
    python download.py --dest schools/districts-elementary-magnet-walk.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/6/query
    python download.py --dest schools/districts-holt-easley.geojson $GISROOT/DurhamMaps/DPS_Schools/MapServer/7/query
    python download.py --dest schools/districts-elementary-student-assignment.geojson $GISROOT/DurhamMaps/DPS_ElementaryStudentAssignment/MapServer/4/query


DPS_ElementaryStudentAssignment/MapServer/4
