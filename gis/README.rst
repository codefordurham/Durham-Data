Durham GIS data
===============

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --python=/usr/bin/python3.3 durham-gis
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements.txt

Download a ArcGIS REST resource::

    python download.py --indent=2 http://gisweb2.ci.durham.nc.us/arcgis/rest/services/DurhamMaps/Parcels/MapServer/1/query

Convert it to GeoJSON::

    ogr2ogr -f GeoJSON geo.json arcgis.json OGRGeoJSON
