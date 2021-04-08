from rdflib import Graph, URIRef, Namespace

g = Graph().parse("geofeaturesapi/config/data.ttl", format="turtle")

# for p, o in g.predicate_objects(URIRef("https://linked.data.gov.au/dataset/qldgeofeatures/" + "AdavaleBasin")):
#     print(p, o)

q = '''
    PREFIX time: <http://www.w3.org/2006/time#>
    PREFIX sdo: <https://schema.org/>
    SELECT ?age ?uri ?name
    WHERE {
        ?uri a geo:Feature ;
             time:hasTime ?age ;
             sdo:name ?name .
    }
    ORDER BY ?age ?name
    '''

for r in g.query(q, initNs={'geo': Namespace("http://www.opengis.net/ont/geosparql#")}):
    print(r)
