from pydantic import BaseModel, Field

class TaskSchema(BaseModel):
    id: int
    title: str 
    description: str | None = None
    status: str 