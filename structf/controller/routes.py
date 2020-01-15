from flask import Blueprint, request, redirect, url_for, Response
from flask_cors import CORS
from pyldapi import RegisterRenderer, RegisterOfRegistersRenderer
from structf.model.province import ProvinceRenderer
import structf.config as config
import structf.controller.LOCIDatasetRenderer
import json
import requests
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, XSD, OWL
import structf.config as config


routes = Blueprint('controller', __name__)
CORS(routes, automatic_options=True)


def get_total(geo_feature_type_uri):
    q = '''SELECT (COUNT(*) AS ?c) WHERE {{?s a <{}>}}'''.format(geo_feature_type_uri)

    for r in config.G.query(q):
        return r[0]


def get_register(geo_feature_type_uri):
    q = '''SELECT ?uri ?name WHERE {{?uri a <{}> ; sdo:name ?name}} ORDER BY ?name'''.format(geo_feature_type_uri)

    r = []
    for row in config.G.query(q):
        r.append((str(row['uri']), str(row['name'])))

    return r


#
#   Register
#
@routes.route('/province/')
def provinces():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Province'
    object_name = 'Provinces'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/subprovince/')
def subprovinces():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#SubProvince'
    object_name = 'Sub Provinces'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/craton/')
def cratons():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Craton'
    object_name = 'Cratons'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/orogen/')
def orogens():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Orogen'
    object_name = 'Orogens'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/depression/')
def depressions():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Depression'
    object_name = 'Depressions'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/basin/')
def basins():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Basin'
    object_name = 'Basins'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


@routes.route('/trough/')
def troughs():
    object_class = 'http://linked.data.gov.au/def/sweetgeofeatures#Trough'
    object_name = 'Troughs'
    per_page = request.args.get('per_page', type=int, default=50)
    # total = get_total('http://linked.data.gov.au/def/sweetgeofeatures#Province')
    register = get_register(object_class)

    return RegisterRenderer(
        request,
        'http://localhost:5000/basin/',
        'Register of ' + object_name,
        'Queensland\'s geological ' + object_name,
        register,
        [object_class],
        len(register),  # we can do this, rather than call total from Graph since all registers here fit on one page
        super_register='http://localhost:5000/reg/',
        per_page=per_page
    ).render()


#
#   Individual
#
@routes.route('/province/<string:province_id>')
def feature(province_id):
    return ProvinceRenderer(request, request.url).render()


#
#   pages
#
@routes.route('/', strict_slashes=True)
def home():
    return structf.controller.LOCIDatasetRenderer.LOCIDatasetRenderer(request, url=config.URI_BASE).render()


@routes.route('/index.ttl')
def home_ttl():
    return structf.controller.LOCIDatasetRenderer.LOCIDatasetRenderer(request, view='dcat', format='text/turtle').render()


#
#   registers
#
@routes.route('/reg/')
def reg():
    return RegisterOfRegistersRenderer(
        request,
        config.DATA_URI_PREFIX,
        'Register of Registers',
        'The master register of this API',
        config.APP_DIR + '/rofr.ttl'
    ).render()


# @routes.route('/meshblock/')
# def meshblocks():
#     total = ASGSFeature.total_meshblocks()
#     if total is None:
#         return Response('ASGS Web Service is unreachable', status=500, mimetype='text/plain')
# 
#     return ASGSRegisterRenderer(
#         request,
#         config.URI_MESHBLOCK_INSTANCE_BASE,
#         'Register of ASGS Meshblocks',
#         'All the ASGS Meshblocks',
#         [config.URI_MESHBLOCK_CLASS],
#         total,
#         ASGSFeature,
#         super_register=config.DATA_URI_PREFIX,
#     ).render()
# 
# 
# @routes.route('/statisticalarealevel1/')
# def sa1s():
#     total = ASGSFeature.total_sa1s()
#     if total is None:
#         return Response('ASGS Web Service is unreachable', status=500, mimetype='text/plain')
# 
#     return ASGSRegisterRenderer(
#         request,
#         config.URI_SA1_INSTANCE_BASE,
#         'Register of ASGS Statistical Area Level 1 regions',
#         'All the ASGS Statistical Area Level 1 regions',
#         [config.URI_SA1_CLASS],
#         total,
#         ASGSFeature,
#         super_register=config.DATA_URI_PREFIX,
#     ).render()


#
#   instances
#


