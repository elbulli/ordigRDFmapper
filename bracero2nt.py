import rdflib
import yaml
from rdflib.namespace import Namespace
from lxml import etree

conf = yaml.load(open('mapping.yml'))

tree = etree.parse('bracero_metadata.xml')
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
            graph.add((pid, ns[predicate[0]][predicate[1]], rdflib.Literal(tag.text)))
    count += 1

outfile = open('braceros.nt', 'w')
outfile.write(graph.serialize(format='nt'))
outfile.close()
            
        
