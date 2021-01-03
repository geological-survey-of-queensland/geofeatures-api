from flask import Blueprint, request, render_template, redirect, Response
from flask_cors import CORS
from pyldapi import ContainerRenderer
from rdflib import Namespace
from rdflib.namespace import SDO, TIME
from api.model import GeoFeatureRenderer, LOCIDatasetRenderer
import api.config as config
from os.path import join

routes = Blueprint('controller', __name__)
CORS(routes, automatic_options=True)


#
#   Dataset
#
@routes.route('/', strict_slashes=True)
def home():
    return LOCIDatasetRenderer(
        request,
        'Qld FoI Dataset',
        'The Dataset of Queensland\'s Geological Features of Interest'
    ).render()


@routes.route('/index.ttl')
def home_ttl():
    return redirect('/?_mediatype=text/turtle')


@routes.route('/data.ttl')
def data():
    d = open(join(config.APP_DIR, 'config', 'data.ttl'), 'rb').read().decode('utf-8')
    return Response(d, status=200, mimetype='text/turtle')


#
#   Register
#
def get_total(geo_feature_type_uri):
    q = '''SELECT (COUNT(*) AS ?c) WHERE {{?s a <{}>}}'''.format(geo_feature_type_uri)

    for r in config.G.query(q):
        return r[0]


def get_register(geo_feature_type_uri):
    q = '''PREFIX sdo: <https://schema.org/> SELECT ?uri ?name WHERE {{?uri a <{}> ; sdo:name ?name}} ORDER BY ?name'''.format(geo_feature_type_uri)

    r = []
    for row in config.G.query(q):
        r.append((
            str(row['uri']).replace(
                'http://linked.data.gov.au/dataset/qldgeofeatures/',
                'https://qgf.surroundaustralia.com/feature/'
            ),
            str(row['name'])
        ))

    return r


def container_response(container_uri, container_name, members):
    return ContainerRenderer(
        request,
        container_uri,
        'Container of ' + container_name,
        'Queensland\'s geological ' + container_name,
        config.DATASET_URI,
        config.DATASET_LABEL,
        members,
        len(members)
    ).render()


@routes.route('/feature/')
def features():
    container_uri = config.DATASET_URI + '/feature/'
    object_class = 'http://www.opengis.net/ont/geosparql#Feature'
    container_name = 'Features'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/basin/')
def basins():
    container_uri = config.DATASET_URI + '/basin/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Basin'
    container_name = 'Basins'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/craton/')
def cratons():
    container_uri = config.DATASET_URI + '/craton/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Craton'
    container_name = 'Cratons'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/depression/')
def depressions():
    container_uri = config.DATASET_URI + '/depression/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Depression'
    container_name = 'Depressions'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/graben/')
def grabens():
    container_uri = config.DATASET_URI + '/graben/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Graben'
    container_name = 'Grabens'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/orogen/')
def orogens():
    container_uri = config.DATASET_URI + '/orogen/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Orogen'
    container_name = 'Orogens'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/province/')
def provinces():
    container_uri = config.DATASET_URI + '/province/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Province'
    container_name = 'Provinces'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/subprovince/')
def subprovinces():
    container_uri = config.DATASET_URI + '/subprovince/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#SubProvince'
    container_name = 'Sub Provinces'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/trough/')
def troughs():
    container_uri = config.DATASET_URI + '/trough/'
    object_class = 'http://linked.data.gov.au/def/geofeatures#Trough'
    container_name = 'Troughs'

    return container_response(container_uri, container_name, get_register(object_class))


@routes.route('/ages')
def ages():
    init_ns = {
        'geo': Namespace("http://www.opengis.net/ont/geosparql#"),
        'sdo': SDO,
        'time': TIME
    }
    q = '''
        SELECT ?age ?uri ?name
        WHERE {
            ?uri a geo:Feature ;
                 time:hasTime ?age ;
                 sdo:name ?name .
        }
        ORDER BY ?age ?name
        '''
    previous_age = 'http://resource.geosciml.org/classifier/ics/ischart/Cambrian'
    current_provinces = []
    html = ''
    for r in config.G.query(q, initNs=init_ns):
        this_age = str(r['age'])
        if this_age == previous_age:
            current_provinces.append(
                '<a href="{}">{}</a>'.format(
                    str(r['uri']).replace('http://linked.data.gov.au/dataset/qldgeofeatures/',
                                          'https://qgf.surroundaustralia.com/feature/'),
                    str(r['name']))
            )
        else:
            html += '''\n\t\t<tr>
            <th><a href="{}">{}</a></th>
            <td>
                {}
            </td>
        </tr>'''.format(
                previous_age,
                previous_age.split('/')[-1],
                '<br />\n\t\t\t\t'.join(current_provinces)
            )
            current_provinces = []
            previous_age = this_age

    return render_template('ages.html', ages=html)


#
#   Individuals
#
@routes.route('/feature/<feature_id>')
def feature(feature_id):
    uri = "http://linked.data.gov.au/dataset/qldgeofeatures/" + feature_id
    return GeoFeatureRenderer(request, uri).render()
