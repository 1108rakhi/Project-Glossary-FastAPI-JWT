from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "glossary_terms"

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "term": {"type": "text"},
                        "description": {"type": "text"},
                        
                    }
                }
            }
        )    

def index_term(id: int, term : str, description: str):
    doc = {"term":term, "description":description}
    es.index(index= INDEX_NAME, id=id, document = doc)

def delete_es_term(id:int):
    es.delete(index="glossary_terms", id=id)

