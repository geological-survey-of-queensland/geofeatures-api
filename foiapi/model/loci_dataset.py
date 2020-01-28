from pyldapi import Renderer, Profile
from os.path import dirname, realpath, join, abspath
from os.path import join
from flask import Response, render_template
from rdflib import Graph
import foiapi.config as config

TEMPLATES_DIR = join(
    dirname(dirname(realpath(__file__))),
    'view',
    'templates'
)


class LOCIDatasetRenderer(Renderer):
    """
    Specialised implementation of the Renderer for displaying DCAT v2, VOID & Reg properties for the GNAF dataset as a
    whole. All content is contained in static HTML & RDT (turtle) files
    """
    def __init__(self, request, url=None, profile=None, mediatype=None):
        profiles = {
            'dcat': Profile(
                'Dataset Catalog Vocabulary - DCAT',
                'The DCAT profile, according to DCAT2',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/html',
                profile_uri='https://www.w3.org/TR/vocab-dcat-2/'
            ),
            'reg': Profile(
                'Registry Ontology Profile',
                'A \'core ontology for registry services\': items are listed in Registers with acceptance statuses',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/html',
                profile_uri='http://purl.org/linked-data/registry'
            ),
            'void': Profile(
                'Vocabulary of Interlinked Data Ontology Profile',
                'VoID is \'an RDF Schema vocabulary for expressing metadata about RDF datasets\'',
                Renderer.RDF_MIMETYPES,
                'text/turtle',
                profile_uri='http://rdfs.org/ns/void'
            ),
        }
        # push RofR properties up to the RofR constructor
        if url is None:
            url = request.url
        super().__init__(request, url, profiles, 'dcat')

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response
        # it's another view so get the data for it
        elif self.profile == 'reg':
            if self.mediatype == 'text/html':
                return render_template('home_reg.html')
            else:
                if self.mediatype not in self.RDF_MIMETYPES:
                    self.mediatype = 'text/turtle'
                return self._render_rdf_from_file('reg.ttl', self.mediatype)
        elif self.profile == 'void':
            # VoID profile is only available in RDF
            if self.mediatype not in self.RDF_MIMETYPES:
                self.mediatype = 'text/turtle'
            return self._render_rdf_from_file('void.ttl', self.mediatype)
        else:  # DCAT, default
            if self.mediatype == 'text/html':
                return render_template('home_dcat.html')
            else:
                if self.mediatype not in self.RDF_MIMETYPES:
                    self.mediatype = 'text/turtle'
                return self._render_rdf_from_file('dcat.ttl', self.mediatype)

    def _render_rdf_from_file(self, file, mediatype):
        if mediatype == 'text/turtle':
            txt = open(join(config.APP_DIR, 'view', file), 'rb').read().decode('utf-8')
            return Response(txt, mimetype='text/turtle')
        else:
            g = Graph().parse(join(config.APP_DIR, 'view', file), format='turtle')
            if mediatype == "_internal":
                return g
            elif mediatype in ['application/rdf+json', 'application/json']:
                return Response(
                    g.serialize(
                        destination=None,
                        format='json-ld',
                        encoding='utf-8'),
                    mimetype=mediatype
                )
            else:
                return Response(
                    g.serialize(
                        destination=None,
                        format=mediatype,
                        encoding='utf-8'),
                    mimetype=mediatype
                )
