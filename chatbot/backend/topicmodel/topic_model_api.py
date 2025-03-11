from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List

from chatbot.backend.topicmodel import simple_tm

# router
app = FastAPI()
simple_tm_router = APIRouter(prefix="/topic-model")


# schemas
class TopicModelRequest(BaseModel):
    # only useful qa pairs are submitted from frontrnd
    qa_pairs: List[str]


@simple_tm_router.post("/map-topics/")
def map_topics(request: TopicModelRequest):
    try:
        # map the topics
        topics = simple_tm.map_all_topics(qa_pairs=request.qa_pairs)
        return {
            "status": "success",
            "topics": topics,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
