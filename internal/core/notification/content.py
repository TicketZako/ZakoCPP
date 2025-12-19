from pydantic import BaseModel, Field


class NotificationContent(BaseModel):
    """
    通知内容
    """

    title: str = Field(default="", description="标题")
    body: str = Field(default="", description="内容")
