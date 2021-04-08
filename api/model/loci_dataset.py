from pyldapi import Renderer, ContainerOfContainersRenderer, Profile
from os.path import dirname, realpath, join, abspath
from os.path import join
from flask import Response, render_template
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS
import api.config as config

TEMPLATES_DIR = join(
    dirname(dirname(realpath(__file__))),
    'view',
    'templates'
)


class LOCIDatasetRenderer(ContainerOfContainersRenderer):
    """
    Specialised implementation of the Renderer for displaying DCAT v2, VOID & Reg properties for the GNAF dataset as a
    whole. All content is contained in static HTML & RDT (turtle) files
    """
    def __init__(self, request, label, comment):
        # additional Profiles for this LOCI Dataset class thing
        # mem profile is added by the ContainerRegister class
        # alt is added by the Register class
        profiles = {
            'loci': Profile(
                'https://linked.data.gov.au/def/loci',
                'LocI Ontology',
                'A profile of several ontologies implemented to govern Linked Data resources published within the '
                'LocI project.',
                Renderer.RDF_MEDIA_TYPES,
                'text/turtle'
            ),
            'dcat': Profile(
                'https://www.w3.org/TR/vocab-dcat-2/',
                'Data Catalog Vocabulary v2',
                'A W3C RDF vocabulary for describing datasets',
                ['text/html'] + Renderer.RDF_MEDIA_TYPES,
                'text/html',
            ),
            'void': Profile(
                'http://rdfs.org/ns/void',
                'Vocabulary of Interlinked Data Ontology Profile',
                'VoID is \'an RDF Schema vocabulary for expressing metadata about RDF datasets\'',
                Renderer.RDF_MEDIA_TYPES,
                'text/turtle'
            )
        }
        super().__init__(
            request,
            config.DATASET_URI,
            label,
            comment,
            profiles,
            join(config.APP_DIR, 'cofc.ttl'),
            default_profile_token='dcat'
        )

    def render(self):
        # try returning alt profile from Renderer
        # or mem profile from ContainerRegister
        response = super().render()
        if response is not None:
            return response

        # it's another profile so get the data for it
        elif self.profile == 'loci':
            # VoID profile is only available in RDF
            if self.mediatype not in self.RDF_MEDIA_TYPES:
                self.mediatype = 'text/turtle'
            return self._render_rdf_from_file('loci.ttl', self.mediatype)
        elif self.profile == 'void':
            # VoID profile is only available in RDF
            if self.mediatype not in self.RDF_MEDIA_TYPES:
                self.mediatype = 'text/turtle'
            return self._render_rdf_from_file('void.ttl', self.mediatype)
        else:  # DCAT, default
            if self.mediatype == 'text/html':
                return render_template('home_dcat.html')
            else:
                if self.mediatype not in self.RDF_MEDIA_TYPES:
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
