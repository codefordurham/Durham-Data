"""
Import Durham's ArcGIS REST data.

ArcGIS REST query: http://resources.arcgis.com/en/help/rest/apiref/index.html?query.html
"""
#!/usr/bin/env python
import argparse
import json
import logging
import requests
import itertools


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ArcGISResource(object):

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
        query['f'] = 'json'
        if 'where' not in query:
            query['where'] = '1=1'
        r = requests.get(self.uri, params=query)
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
            query = {'outFields': '*', 'where': where}
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='REST URI')
    parser.add_argument('--indent', type=int, help='JSON Indent')
    parser.add_argument('--limit', type=int, help='Object limit')
    args = parser.parse_args()
    resource = ArcGISResource(args.uri)
    logger.info("Total objects: {:,}".format(resource.count()))
    with open('arcgis.json', 'w') as outfile:
        json.dump(resource.objects(args.limit), outfile, indent=args.indent)


if __name__ == "__main__":
    main()
