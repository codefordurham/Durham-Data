"""
Import Durham's ArcGIS REST data.

ArcGIS REST query: http://resources.arcgis.com/en/help/rest/apiref/index.html?query.html
"""
#!/usr/bin/env python
import argparse
import itertools
import json
import logging
import os
import requests
import subprocess
import tempfile


logger = logging.getLogger(__name__)


class ArcGISResource(object):

    CONVERSION_MAP = {'.geojson': 'GeoJSON',
                      '.shp': 'ESRI Shapefile'}

    def __init__(self, uri):
        self.uri = uri

    def _paginate(self, iterable, step=1000):
        """Group iterable into pages of length step."""
        start = 0
        while start < len(iterable):
            end = start + step
            yield iterable[start:end]
            start = end

    def get(self, query):
        """Request JSON data from ArcGIS REST resource."""
        params = {'f': 'json', 'where': '1=1'}
        params.update(query)
        r = requests.get(self.uri, params=params)
        try:
            return r.json()
        except ValueError:
            raise Exception(r.text)

    def count(self):
        """Return count of all available objectIds for resource."""
        query = {'returnCountOnly': 'true'}
        return self.get(query)['count']

    def object_ids(self):
        """Return all available objectIds for resource."""
        query = {'returnIdsOnly': 'true', 'orderByFields': 'ObjectId ASC'}
        return self.get(query)['objectIds']

    def pages(self, limit=0):
        """Query pages from ArcGIS API by filtering ObjectIDs"""
        pages = list(self._paginate(self.object_ids()))
        logger.info('Total pages: {:,}'.format(len(pages)))
        for index, ids in enumerate(pages):
            where = 'ObjectId>={} AND ObjectId<={}'.format(ids[0], ids[-1])
            query = {'outFields': '*', 'where': where, 'outSR': 4326}
            yield self.get(query)

    def objects(self, limit=None):
        """Select all available objects"""
        objects = {}
        for index, page in enumerate(self.pages()):
            logger.debug('Page: {}'.format(index))
            if index == 0:
                objects.update(page)
                continue
            if limit and len(objects['features']) > limit:
                return objects
            objects['features'].extend(page['features'])
        return objects

    def download(self, dest, limit=None):
        _, ext = os.path.splitext(dest)
        if os.path.exists(dest):
            os.unlink(dest)
        # create temporary file
        logger.info("Total objects: {:,}".format(self.count()))
        tmp = tempfile.NamedTemporaryFile('w+', suffix='.json', delete=False)
        logger.debug("Created temporary JSON file {}".format(tmp.name))
        try:
            # write JSON
            json.dump(self.objects(limit), tmp)
            tmp.close()
            # convert file
            format_name = self.CONVERSION_MAP.get(ext, 'ESRI Shapefile')
            cmd = 'ogr2ogr -f {} {} {} OGRGeoJSON'.format(format_name, dest,
                                                          tmp.name)
            subprocess.check_call(cmd, shell=True)
        finally:
            os.unlink(tmp.name)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='REST URI')
    parser.add_argument('--indent', type=int, help='JSON Indent', default=2)
    parser.add_argument('--limit', type=int, help='Object limit')
    parser.add_argument('--dest', type=str, default='arcgis.geojson',
                        help='Destination file name and format')
    args = parser.parse_args()
    resource = ArcGISResource(args.uri)
    resource.download(dest=args.dest)


if __name__ == "__main__":
    main()
