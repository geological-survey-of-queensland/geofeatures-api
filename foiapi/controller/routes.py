from flask import Blueprint, request, render_template, redirect
from flask_cors import CORS
from pyldapi import RegisterRenderer, RegisterOfRegistersRenderer
from foiapi.model import ProvinceRenderer, LOCIDatasetRenderer
import foiapi.config as config


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
#   Dataset
#
@routes.route('/', strict_slashes=True)
def home():
    return LOCIDatasetRenderer(
        request,
        profile='dcat',
        mediatype='text/turtle'
    ).render()


@routes.route('/index.ttl')
def home_ttl():
    return redirect('/?_mediatype=text/turtle')


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


@routes.route('/reg/')
def reg():
    return RegisterOfRegistersRenderer(
        request,
        config.DATA_URI_PREFIX,
        'Register of Registers',
        'The master register of this API',
        config.APP_DIR + '/rofr.ttl'
    ).render()


@routes.route('/ages')
def ages():
    q = '''
        PREFIX time: <http://www.w3.org/2006/time#>
        PREFIX sdo: <https://schema.org/>
        SELECT ?age ?uri ?name
        WHERE {
            ?uri a <http://linked.data.gov.au/def/sweetgeofeatures#Province> ;
                 time:hasTime ?age ;
                 sdo:name ?name .
        }
        ORDER BY ?age ?name
        '''
    current_age = 'http://resource.geosciml.org/classifier/ics/ischart/Cambrian'
    current_provinces = []
    html = ''
    for r in config.G.query(q):
        this_age = str(r['age'])
        if this_age == current_age:
            current_provinces.append(
                '<a href="{}">{}</a>'.format(
                    str(r['uri']).replace('http://linked.data.gov.au/dataset/qld-structural-framework/',
                                          'http://localhost:5000/'),
                    str(r['name']))
            )
        else:
            html += '''\n\t<tr>
            <th><a href="{}">{}</a></th>
            <td>
                {}
            </td>
        </tr>'''.format(
                this_age,
                this_age.split('/')[-1],
                '<br />\n\t\t\t'.join(current_provinces)
            )
        current_age = this_age

    return render_template('ages.html', ages=html)


#
#   Individuals
#
@routes.route('/province/<province_id>')
def feature(province_id):
    return ProvinceRenderer(request, request.base_url).render()
