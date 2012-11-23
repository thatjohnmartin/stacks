#! /usr/bin/env python

import time
import os
import codecs
from collections import defaultdict

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stacks.settings'
    os.sys.path.append(os.environ['STACKS_ROOT'])

from stacks.www.models import Thing, Predicate, Node

types_lookup = set([
    ('/type/object/type', '/film/film'),
#    ('/film/directed_by', ''),
#    ('/film/actor', ''),
#    ('/film/producer', ''),
#    ('/film/writer', ''),
#    ('/film/film_genre', ''),
#    ('/film/film_series',''),
])

identifiers_lookup = set([
    ('/type/object/key', '/en'),
    ('/type/object/name', '/lang/en'),
])

properties_lookup = set([
    ('/type/object/key', '/wikipedia/en'),
    ('/type/object/key', '/authority/imdb/name'),
])

def ingest():
    start_time = time.time()

    freebase = codecs.open('/Users/johnm/Projects/freebase/freebase-datadump-quadruples.tsv', 'r', 'utf-8')

    line_number = 0
    max_line_number = None # i.e. all
    entities = defaultdict(dict)
    predicates = {}

    for prop in properties_lookup:
        pred, created = Predicate.objects.get_or_create(path=prop[0])
        if prop[0] not in predicates:
            predicates[prop[0]] = pred

    for line in freebase:
        line_number += 1
        if max_line_number and line_number > max_line_number:
            break

        object, predicate, subject, value = line.split('\t')

        if (predicate, subject) in types_lookup:
            entities[subject][object] = {}

    # rewind
    freebase.seek(0)
    line_number = 0

    for line in freebase:
        line_number += 1
        if max_line_number and line_number > max_line_number:
            break

        object, predicate, subject, value = line.split('\t')

        all_lookups = properties_lookup.union(identifiers_lookup)
        if (predicate, subject) in all_lookups and object in entities['/film/film']:
            entities['/film/film'][object][(predicate, subject)] = value.strip()

    freebase.close()

    for mid in entities['/film/film'].keys():
        props = entities['/film/film'][mid]
        slug = props.get(('/type/object/key', '/en'))
        name = props.get(('/type/object/name', '/lang/en'))

        if slug and name:
            thing = Thing.objects.create(name=name, mid=mid, slug=slug)

            for prop_lookup in properties_lookup:
                prop = props.get(prop_lookup)
                if prop:
                    Node.objects.create(
                        object=thing,
                        predicate=predicates[prop_lookup[0]],
                        context=prop_lookup[1],
                        value_str=props[prop_lookup],
                    )

    end_time = time.time()

    print "Processed %d lines" % line_number
    print "Found %d films" % len(entities['/film/film'])
    print "Run took %0.2f seconds" % (end_time - start_time)

if __name__ == "__main__":
    ingest()
