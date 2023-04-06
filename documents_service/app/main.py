from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

class CreateDocModel(BaseModel):
    title: str
    body: str

class Document:
    def __init__(self, id: int, title: str, value: str) -> None:
        self.id = id
        self.title = title
        self.value = value

documents: List[Document] = [#для 10
   # Document(0, 'First doc', 'rtgdrtgrdtg'),
   # Document(1,'Second', 'dfvdssdfdgfgdfg')
]

def add_document(content:CreateDocModel):
    id = len(documents)
    documents.append(Document(id,content.title,content.body))
    return id

app = FastAPI()

################jaeger
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource(attributes={
    SERVICE_NAME: "docs-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

# Merrily go about tracing!
###############

###############
##########Prometheus
from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
###############

@app.get("/v1/docs")
async def get_docs():
    return documents #массив

@app.post("/v1/docs")
async def add_doc(content: CreateDocModel):
    add_document(content)
    return documents[-1]

@app.get("/v1/docs/{id}")
async def get_docs_by_id(id: int):
    result = [i for i in documents if i.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code=404, detail="Document not found")

@app.get("/__health")
async def check_service():
    return