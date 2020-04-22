from pyldapi import Renderer, Profile
from rdflib import Graph, URIRef, Namespace, BNode
from rdflib.namespace import RDF, SDO, TIME
from geofeaturesapi.config import G
from flask import Response, render_template


class GeoFeatureRenderer(Renderer):
    def __init__(self, request, geofeature_uri):
        # prepare views (Alt view included by default)
        profiles = {
            'geofeature': Profile(
                'http://example.com/profile/geofeature',
                'Geological Features Profile',
                'This view shows the basic *feature* properties of a geological features, such as it\'s geometry, '
                'and also some geological properties, such as it\'s geologic age.',
                [
                    "text/html",
                    "text/turtle",
                    "application/rdf+xml",
                    "application/ld+json",
                    "text/n3",
                    "text/n-triples"
                ],
                'text/html'
            ),
            'loci': Profile(
                'http://linked.data.gov.au/def/loci',
                'LocI Ontology',
                'A profile of several ontologies implemented to govern Linked Data resources published within the '
                'LocI project.',
                Renderer.RDF_MEDIA_TYPES,
                'text/turtle'
            )
        }
        # initialise super class
        self.uri = geofeature_uri
        super(GeoFeatureRenderer, self).__init__(request, self.uri, profiles, 'geofeature')

    def _render_rdf(self, g, mediatype, headers):
        if mediatype in ['application/rdf+json', 'application/json']:
            resp = g.serialize(format='json-ld', encode='utf-8').decode('utf-8')
        else:
            resp = g.serialize(format=mediatype, encode='utf-8').decode('utf-8')

        return Response(
            resp,
            status=200,
            mimetype=mediatype,
            headers=headers
        )

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response

        # it's another profile so get the data for it
        else:
            # extract properties from RDF
            mini_graph = Graph()
            SF = Namespace('http://linked.data.gov.au/dataset/qldgeofeatures/')
            mini_graph.bind('sf', SF)
            SGF = Namespace('http://linked.data.gov.au/def/geofeatures#')
            mini_graph.bind('sgf', SGF)
            GEO = Namespace("http://www.opengis.net/ont/geosparql#")
            mini_graph.bind('geo', GEO)
            mini_graph.bind('sdo', SDO)
            mini_graph.bind('time', TIME)
            GEOX = Namespace("http://linked.data.gov.au/def/geox#")
            mini_graph.bind('geox', GEOX)
            GT = Namespace('http://resource.geosciml.org/classifier/ics/ischart/')
            mini_graph.bind('geotime', GT)

            props = {
                'uri': self.uri,
                str(RDF.type): {
                    'label': 'Type',
                    'values': []
                },
                str(SDO.name): {
                    'label': 'Name',
                    'values': []
                },
                str(TIME.hasTime): {
                    'label': 'Has time',
                    'values': []
                },
                str(GEO.hasGeometry): {
                    'label': 'Has geometry',
                    'values': []
                }
            }

            found = False
            for p, o in G.predicate_objects(URIRef(self.uri)):
                found = True

                # for HTML printing
                if str(p) in props.keys():
                    if p == GEO.hasGeometry:  # handling the BNs
                        geom = []
                        for p2, o2 in G.predicate_objects(o):
                            if p2 in [GEO.asWKT, GEOX.hasRole]:
                                geom.append((str(p2), str(o2)))
                        props.get(str(p))['values'].append(sorted(geom))
                    else:
                        props.get(str(p))['values'].append(str(o))  # handling simple literals or URIs

                # for RDF serialization
                mini_graph.add((URIRef(self.uri), p, o))

                if type(o) == BNode:
                    for p2, o2 in G.predicate_objects(o):
                        mini_graph.add((o, p2, o2))

            # if no rows are returned, the URI was unknown
            if not found:
                return Response(
                    'A Feature with ID {} was not found.'.format(self.uri),
                    status=404,
                    mimetype='text/plain'
                )

            if self.profile == 'geofeature':
                if self.mediatype in Renderer.RDF_MEDIA_TYPES:
                    return self._render_rdf(mini_graph, self.mediatype, self.headers)
                else:  # only HTML for now
                    return Response(
                        render_template(
                            'geofeature.html',
                            props=props
                        ),
                        status=200,
                        mimetype=self.mediatype,
                        headers=self.headers
                    )
            else:  # self.profile == 'loci':
                # LocI profile only has RDF
                # return same result as geofeature for now
                # (geofeature will have more properties not in loci in the future)
                return self._render_rdf(mini_graph, self.mediatype, self.headers)


# this class is for testing only
class Mock:
    def __init__(self):
        self.values = {
            '_profile': 'geofeature',
            '_mediatype': 'text/html'
        }


# this main method is for testing only
if __name__ == '__main__':
    request = Mock()

    # import pprint
    # pprint.pprint(request.view)
    p = GeoFeatureRenderer(request, 'http://linked.data.gov.au/dataset/qldgeofeatures/BarnardProvince')
    print()
    print(p.render())
