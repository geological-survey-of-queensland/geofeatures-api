from pyldapi import Renderer, Profile
from rdflib import Graph, URIRef, Namespace, BNode
from foiapi.config import G
from flask import Response, render_template


class ProvinceRenderer(Renderer):
    def __init__(self, request, province_uri):
        province_uri = province_uri.replace(
            'http://localhost:5000/',
            'http://linked.data.gov.au/dataset/qld-structural-framework/')
        # prepare views (Alt view included by default)
        profiles = {
            'geofoi': Profile(
                'Geological Features of Interest Profile',
                'This view shows the basic *feature* properties of a geological FoI, such as it\'s geometry, '
                'and also some geological properties, such as it\'s geologic age.',
                [
                    "text/html",
                    "text/turtle",
                    "application/rdf+xml",
                    "application/ld+json",
                    "text/n3",
                    "text/n-triples"
                ],
                'text/html',
                profile_uri='http://example.com/profile/geofoi'
            )
        }
        # initialise super class
        self.uri = province_uri
        super(ProvinceRenderer, self).__init__(request, province_uri, profiles, 'geofoi')

    def render(self):
        # try returning alternates and all view
        response = super().render()
        if response is not None:
            return response

        # it's another view so get the data for it
        else:
            # extract properties from RDF
            mini_graph = Graph()
            props = {
                'uri': self.uri,
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': {
                    'label': 'Type',
                    'values': []
                },
                'https://schema.org/name': {
                    'label': 'Name',
                    'values': []
                },
                'http://www.w3.org/2006/time#hasTime': {
                    'label': 'Has time',
                    'values': []
                },

                'http://www.opengis.net/ont/geosparql#hasGeometry': {
                    'label': 'Has geometry',
                    'values': []
                },
            }
            found = False
            for p, o in G.predicate_objects(URIRef(self.uri)):
                found = True

                # for HTML printing
                if str(p) in props.keys():
                    if str(p) == 'http://www.opengis.net/ont/geosparql#hasGeometry':  # handling the BNs
                        geom = []
                        for p2, o2 in G.predicate_objects(o):
                            if str(p2) in [
                                'http://linked.data.gov.au/def/geox#asWKT',
                                'http://linked.data.gov.au/def/geox#hasRole'
                            ]:
                                geom.append((str(p2), str(o2)))
                        props.get(str(p))['values'].append(sorted(geom))
                    else:
                        props.get(str(p))['values'].append(str(o))  # handling simple literals or URIs

                # for RDF serialization
                mini_graph.add((URIRef(self.uri), p, o))

                if type(o) == BNode:
                    for p2, o2 in G.predicate_objects(o):
                        mini_graph.add((o, p2, o2))

            SF = Namespace('http://linked.data.gov.au/dataset/qld-structural-framework/')
            mini_graph.bind('sf', SF)
            SGF = Namespace('http://linked.data.gov.au/def/sweetgeofeatures#')
            mini_graph.bind('sgf', SGF)
            GEO = Namespace("http://www.opengis.net/ont/geosparql#")
            mini_graph.bind('geo', GEO)
            SDO = Namespace("https://schema.org/")
            mini_graph.bind('sdo', SDO)
            TIME = Namespace("http://www.w3.org/2006/time#")
            mini_graph.bind('time', TIME)
            GEOX = Namespace("http://linked.data.gov.au/def/geox#")
            mini_graph.bind('geox', GEOX)
            GT = Namespace('http://resource.geosciml.org/classifier/ics/ischart/')
            mini_graph.bind('geotime', GT)
            
            # if no rows are returned, the URI was unknown
            if not found:
                return Response(
                    'Province (or a sub class of Province) with ID {} not found.'.format(self.uri),
                    status=404,
                    mimetype='text/plain'
                )

            if self.format in Renderer.RDF_MIMETYPES:
                if self.format in ['application/rdf+json', 'application/json']:
                    resp = mini_graph.serialize(format='json-ld', encode='utf-8').decode('utf-8')
                else:
                    resp = mini_graph.serialize(format=self.format, encode='utf-8').decode('utf-8')

                return Response(
                    resp,
                    status=200,
                    mimetype=self.format
                )
            else:  # only HTML for now
                return render_template(
                    'province.html',
                    props=props
                )


# this class is for testing only
class Mock:
    def __init__(self):
        self.values = {
            '_profile': 'geofoi',
            '_mediatype': 'text/html'
        }


# this main method is for testing only
if __name__ == '__main__':
    request = Mock()

    # import pprint
    # pprint.pprint(request.view)
    p = ProvinceRenderer(request, 'http://linked.data.gov.au/dataset/qld-structural-framework/feature/BarnardProvince')
    print()
    print(p.render())
