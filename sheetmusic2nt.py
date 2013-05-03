import rdflib
import yaml
from rdflib.namespace import Namespace
from lxml import etree
from rdflib import plugin 

# setup SPARQL
plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

conf = yaml.load(open('mapping.yml'))

tree = etree.parse('sheetmusic_export_2013_05_03.xml')
graph = rdflib.Graph()

for name in conf['namespaces']:
    conf['namespaces'][name] = Namespace(conf['namespaces'][name])
ns = conf['namespaces']

count = 1
for record in tree.getroot():
    pid = rdflib.URIRef('http://oregondigital.org/ns/' + str(count))
    for tag in record:
        if tag.tag in conf['mappings']:
            predicate = conf['mappings'][tag.tag].split(':')
            if tag.text != None:
              graph.add((pid, ns[predicate[0]][predicate[1]], rdflib.Literal(tag.text)))
    count += 1

full_outfile = open('sheetmusic.nt', 'w')
full_outfile.write(graph.serialize(format='nt'))
full_outfile.close()

query = """SELECT ?record ?p ?o WHERE 
{{?record <http://multimedialab.elis.ugent.be/users/samcoppe/ontologies/Premis/premis.owl#originalName> "P0120_2567" . 
?record ?p ?o} UNION
{?record <http://multimedialab.elis.ugent.be/users/samcoppe/ontologies/Premis/premis.owl#originalName> "P0120_2569" . 
?record ?p ?o} UNION
{?record <http://multimedialab.elis.ugent.be/users/samcoppe/ontologies/Premis/premis.owl#originalName> "P0120_2570" . 
?record ?p ?o}}
"""

q = graph.query(query)
sample_items = q.result
sample_graph = rdflib.Graph()
for triple in sample_items:
    sample_graph.add(triple)

sample_outfile = open('sheetmusic_sample.nt', 'w')
sample_outfile.write(sample_graph.serialize(format='nt'))
sample_outfile.close()
