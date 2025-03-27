from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

ELASTICSEARCH_HOST = "http://elasticsearch:9200"
INDEX_NAME = "india"

es = Elasticsearch(hosts=[ELASTICSEARCH_HOST], request_timeout=30)


def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "text": {"type": "text"}
                    }
                }
            },
        )

@app.on_event("startup")
def startup_event():
    create_index()  

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/get")
def get_best_match(query: str):
    res = es.search(
        index=INDEX_NAME,
        body={"query": {"match": {"text": query}}},
        size=1,  
    )
    if res["hits"]["hits"]:
        return res["hits"]["hits"][0]["_source"]
    return {"message": "No relevant document found"}

@app.post("/insert")
def insert_document():
    documents = [
        {"id": "1", "text": "India, officially the Republic of India, is a country in South Asia. It is the seventh-largest country by area and, since June 2023, the most populous country. Since gaining independence in 1947, it has remained the world's most populous democracy. Bounded by the Indian Ocean to the south, the Arabian Sea to the southwest, and the Bay of Bengal to the southeast, it shares land borders with Pakistan to the west, China, Nepal, and Bhutan to the north, and Bangladesh and Myanmar to the east. In the Indian Ocean, India is close to Sri Lanka and the Maldives, while its Andaman and Nicobar Islands share maritime borders with Thailand, Myanmar, and Indonesia."},
        {"id": "2", "text": "Modern humans arrived in the Indian subcontinent from Africa over 55,000 years ago. Their long period of isolation as hunter-gatherers contributed to high genetic diversity, second only to Africa. Settled life began in the western Indus River basin around 9,000 years ago, gradually evolving into the Indus Valley Civilization by the third millennium BCE. By 1200 BCE, an early form of Sanskrit, an Indo-European language, had spread into India from the northwest, influencing the emergence of Hinduism. The region's original Dravidian languages were gradually replaced in northern India. By 400 BCE, the caste system had emerged within Hinduism, while Buddhism and Jainism challenged hereditary social order. The Maurya and Gupta Empires brought early political unification and cultural advancements, but women's status declined, and untouchability became institutionalized. In South India, Dravidian kingdoms influenced Southeast Asia by exporting language scripts and religious traditions."},
        {"id": "3", "text": "During the early medieval period, Christianity, Islam, Judaism, and Zoroastrianism took root in India's coastal regions, while Muslim armies from Central Asia intermittently invaded the northern plains. The Delhi Sultanate integrated northern India into the broader Islamic world. In the south, the Vijayanagara Empire fostered a resilient Hindu culture. Sikhism emerged in Punjab, rejecting religious orthodoxy. The Mughal Empire, established in 1526, ushered in two centuries of relative peace and left behind a rich architectural heritage. The gradual expansion of British East India Company rule transformed India into a colonial economy while consolidating its territorial control. British Crown rule began in 1858, bringing slow political reforms, technological advancements, and modern education. A nationalist movement, driven by nonviolent resistance, played a decisive role in ending British rule in 1947. The British Indian Empire was then partitioned into two nations: India and Pakistan, resulting in mass migration and significant loss of life."},
        {"id": "4", "text": "Since becoming a federal republic in 1950, India has been governed through a democratic parliamentary system. It is a pluralistic, multilingual, and multi-ethnic society. Its population grew from 361 million in 1951 to over 1.4 billion in 2023. During this period, its nominal per capita income increased from $64 to $2,601, and its literacy rate rose from 16.6% to 74%. Once a largely impoverished country, India has transformed into a fast-growing economy and a major IT hub, with a growing middle class. Indian films and music have gained global influence. While the country has reduced poverty, economic inequality has risen. India is a nuclear-armed state with significant military expenditure and ongoing disputes over Kashmir with Pakistan and China. Socio-economic challenges include gender inequality, child malnutrition, and rising air pollution. India is one of the world's most biodiverse nations, with four biodiversity hotspots, and its wildlife has historically been protected by cultural and legal measures."},
    ]

    for doc in documents:
        es.index(index=INDEX_NAME, id=doc["id"], body=doc)

    return {"message": "Documents inserted!"}
