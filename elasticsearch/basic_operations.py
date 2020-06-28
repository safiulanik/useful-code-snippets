# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
# Connect to the elastic cluster
es=Elasticsearch([{'host':'localhost','port':9200}])
es
# output: <Elasticsearch([{'host': 'localhost', 'port': 9200}])>


# prepare data
e1={
    "first_name":"nitin",
    "last_name":"panwar",
    "age": 27,
    "about": "Love to play cricket",
    "interests": ['sports','music'],
}
print e1
# output: {'interests': ['sports', 'music'], 'about': 'Love to play cricket', 'first_name': 'nitin', 'last_name': 'panwar', 'age': 27}


# now let's store this document in Elasticsearch 
res = es.index(index='megacorp',doc_type='employee',id=1,body=e1)
"""
Simple! There was no need to perform any administrative tasks first, 
like creating an index or specifying the type of data that each field 
contains. We could just index a document directly. Elasticsearch ships 
with defaults for everything, so all the necessary administration tasks 
were taken care of in the background, using default values.
"""


# let's insert some more documents
e2={
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}
e3={
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
res=es.index(index='megacorp',doc_type='employee',id=2,body=e2)
print res['created']
# output: False
res=es.index(index='megacorp',doc_type='employee',id=3,body=e3)
print res['created']
# output: True


# retrieving a document
res=es.get(index='megacorp',doc_type='employee',id=3)
print res
# output: {u'_type': u'employee', u'_source': {u'interests': [u'forestry'], u'age': 35, u'about': u'I like to build cabinets', u'last_name': u'Fir', u'first_name': u'Douglas'}, u'_index': u'megacorp', u'_version': 1, u'found': True, u'_id': u'3'}

# you will get the actual document in ‘_source’ field
print res['_source']
# output: {u'interests': [u'forestry'], u'age': 35, u'about': u'I like to build cabinets', u'last_name': u'Fir', u'first_name': u'Douglas'}


# deleting a document
res=es.delete(index='megacorp',doc_type='employee',id=3)
print res['result']
# output: deleted


# search lite
res= es.search(index='megacorp',body={'query':{}})
print res['hits']['hits']
# output: [{u'_score': 1.0, u'_type': u'employee', u'_id': u'4', u'_source': {u'interests': [u'sports', u'music'], u'age': 27, u'about': u'Love to play football', u'last_name': u'pafdfd', u'first_name': u'asd'}, u'_index': u'megacorp'}, {u'_score': 1.0, u'_type': u'employee', u'_id': u'2', u'_source': {u'interests': [u'music'], u'age': 32, u'about': u'I like to collect rock albums', u'last_name': u'Smith', u'first_name': u'Jane'}, u'_index': u'megacorp'}, {u'_score': 1.0, u'_type': u'employee', u'_id': u'1', u'_source': {u'interests': [u'sports', u'music'], u'age': 27, u'about': u'Love to play cricket', u'last_name': u'panwar', u'first_name': u'nitin'}, u'_index': u'megacorp'}]


# match operator
res= es.search(index='megacorp',body={'query':{'match':{'first_name':'nitin'}}})
print res['hits']['hits']
# output: [{u'_score': 0.2876821, u'_type': u'employee', u'_id': u'1', u'_source': {u'interests': [u'sports', u'music'], u'age': 27, u'about': u'Love to play cricket', u'last_name': u'panwar', u'first_name': u'nitin'}, u'_index': u'megacorp'}]


# bool operator
res= es.search(index='megacorp',body={
        'query':{
            'bool':{
                'must':[{
                        'match':{
                            'first_name':'nitin'
                        }
                    }]
            }
        }
    })
print res['hits']['hits']
# output: [{u'_score': 0.2876821, u'_type': u'employee', u'_id': u'1', u'_source': {u'interests': [u'sports', u'music'], u'age': 27, u'about': u'Love to play cricket', u'last_name': u'panwar', u'first_name': u'nitin'}, u'_index': u'megacorp'}]


# filter operator
res= es.search(index='megacorp',body={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        'first_name':'nitin'
                    }
                },
                "filter":{
                    "range":{
                        "age":{
                            "gt":25
                        }
                    }
                }
            }
        }
    })
print res['hits']['hits']
# output: [{u'_score': 0.2876821, u'_type': u'employee', u'_id': u'1', u'_source': {u'interests': [u'sports', u'music'], u'age': 27, u'about': u'Love to play cricket', u'last_name': u'panwar', u'first_name': u'nitin'}, u'_index': u'megacorp'}]
res= es.search(index='megacorp',body={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        'first_name':'nitin'
                    }
                },
                "filter":{
                    "range":{
                        "age":{
                            "gt":27
                        }
                    }
                }
            }
        }
    })
print res['hits']['hits']
# output: []


# full text search
e4={
    "first_name":"asd",
    "last_name":"pafdfd",
    "age": 27,
    "about": "Love to play football",
    "interests": ['sports','music'],
}
res=es.index(index='megacorp',doc_type='employee',id=4,body=e4)
print res['created']
# output: False
res= es.search(index='megacorp',doc_type='employee',body={
        'query':{
            'match':{
                "about":"play cricket"
            }
        }
    })
for hit in res['hits']['hits']:
    print hit['_source']['about'] 
    print hit['_score']
    print '**********************'
# output: Love to play football
# output: 0.7549128
# output: **********************
# output: Love to play cricket
# output: 0.5753642
# output: **********************


# phrase search
res= es.search(index='megacorp',doc_type='employee',body={
        'query':{
            'match_phrase':{
                "about":"play cricket"
            }
        }
    })
for hit in res['hits']['hits']:
    print hit['_source']['about'] 
    print hit['_score']
    print '**********************'
# output: Love to play cricket
# output: 0.5753642
# output: **********************


# aggregations
res= es.search(index='megacorp',doc_type='employee',body={
        "aggs": {
            "all_interests": {
            "terms": { "field": "interests" }
            }
        }
    })
