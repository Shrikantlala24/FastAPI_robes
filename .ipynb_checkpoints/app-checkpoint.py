from fastapi import FastAPI


from typing import Annotation, Literal
from pydantic import BaseModel, Field, computed_field


class Patient(BaseModel) :
    