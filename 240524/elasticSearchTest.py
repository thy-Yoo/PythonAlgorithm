
import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
import warnings

# 경고 무시 설정
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
# 인증서 검증에 관한 경고가 뜨던데, 비활성화를 위해 넣어주었다. 개발 환경에서만 이용하도록 하자.

# 로깅 설정
logging.basicConfig(level=logging.INFO)

try:
    # 엘라스틱서치 클라이언트 생성
    es = Elasticsearch(
        ["https://127.0.0.1:9200"], # 본인 시스템에서 열어둔 Elasticserch 서버의 URL
        basic_auth=("elastic", "elastic1234"), # 본인 시스템에 설치한 elastic의 ID와 PW
        verify_certs=False # 인증서를 검증하지 않도록 설정한다.
    )

    # 인덱스 생성
    index_name = "my_index" # 인덱스의 이름을 정의
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name) # 기존재 하지 않으면 해당 이름으로 인덱스 생성
    """
     인덱스가 무엇일까?
     RDBMS 가 테이블을 사용한다면, Elasticsearch 는 인덱스 개념을 사용하는 듯 하다.
     - Elasticsearch 에서 Index 는 데이터가 저장되는 기본 단위이며, JSON 문서를 저장한다.
     - 하나의 Index 는 여러 개의 shard로 분할될 수 있으며, 각 샤드는 여러 노드에 분산될 수 있다.
     - 또한 인덱스는 mapping 이라는 schema 를 가지고 있다.
     
     RDBMS에서 
     table 내에 수많은 rows 들이 있는데,
     하나의 data content 가 하나의 row 이고,
     data content 의 속성 값들이 각 columns 에 해당 하는 값들이 된다면,
     
     Elasticsearch 에서는 
     index 내에 수많은 documents 들이 있고,
     하나의 data content 가 하나의 Document 이고,
     data content 의 속성 값들은 각 field 에 해당 하는 값들이다
     
     .. 라고 보면 될 것 같다.
     
     
     만약 RDBMS 에서 아래와 같은 데이터 구조를 만들었다면,
     
     CREATE TABLE employees (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        age INT,
        department VARCHAR(50)
    );
    INSERT INTO employees (id, name, age, department) VALUES (1, 'John Doe', 30, 'Engineering');

    Elasticsearch 에서는 아래와 같은 데이터 구조를 구성한다고 한다.
    참고로, properties 내의 key 값들이 사용자가 정의 할 수 있는 columns 에 해당하는 값들이며
    mapping/mappings/properties 라는 속성은 Elasticsearch 내에 예약된 키워드로 고정적인 속성이라고 한다.
    # 매핑 정의
    mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "age": {"type": "integer"},
                "department": {"type": "text"}
            }
        }
    }
    # 인덱스 생성
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
    # 문서 추가
    doc = {
        "name": "John Doe",
        "age": 30,
        "department": "Engineering"
    }
    es.index(index=index_name, id=1, document=doc)
    """

    # 문서 추가 (문서는 row 같은 역할로, 네이밍이 없는 값임)
    doc = {
        "title": "Hello Elasticsearch",
        "content": "This is a test document."
    }
    res = es.index(index=index_name, id=1, document=doc)
    logging.info("Indexing result: %s", res['result'])

    # 데이터 검색
    query = { # 데이터 검색을 위한 쿼리문을 작성한다.
        "query": {
            "match": { # match 라는 쿼리는 아래 필드에서 아래 데이터를 '포함' 하는 document 를 찾는다.
                "title": "Hello"
            }
        }
    }
    res = es.search(index=index_name, body=query) # 데이터를 검색한다.
    logging.info("Got %d Hits:", res['hits']['total']['value'])
    # hits 는 전체 검색 결과를 포함하는 객체이다. hits.total.value 의 구조로 검색된 총 문서의 수를 뽑을 수 있다.

    for hit in res['hits']['hits']:
        logging.info(hit["_source"])

except ConnectionError as e:
    logging.error("Connection error: %s", e)
except NotFoundError as e:
    logging.error("Not found error: %s", e)
except Exception as e:
    logging.error("An error occurred: %s", e)
