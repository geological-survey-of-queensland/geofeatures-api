import rdflib
from os.path import dirname, realpath, join
import pickle
from rdflib import Namespace

APP_DIR = dirname(dirname(realpath(__file__)))

with open(join(APP_DIR, 'foiapi', 'config', 'data.pickle'), 'rb') as f:
    G = pickle.load(f)
    f.close()

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
current_age = ''
current_provinces = []
html = ''
for r in G.query(q):
    this_age = str(r['age'])
    if this_age == current_age:
        current_provinces.append(
            '<a href="{}">{}</a>'.format(
                str(r['uri']).replace('http://linked.data.gov.au/dataset/qld-structural-framework/', 'http://localhost:5000/'),
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

print(html)
