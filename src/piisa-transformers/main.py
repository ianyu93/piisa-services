import json
from enum import Enum
from typing import Union

from fastapi import FastAPI
from pii_data.types import PiiEnum
from pii_transform.api.e2e import PiiTextProcessor
from pii_transform.defs import FMT_CONFIG_TRANSFORM
from pii_transform.helper import substitution
from pydantic import BaseModel, Field

app = FastAPI()


# all the possible policies in substitution.POLICIES
class SupportedPolicy(str, Enum):
    annotate = "annotate"
    custom = "custom"
    hash = "hash"
    label = "label"
    passthrough = "passthrough"
    placeholder = "placeholder"
    redact = "redact"
    synthetic = "synthetic"


class SupportedEntity(str, Enum):
    AGE = "AGE"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    BLOCKCHAIN_ADDRESS = "BLOCKCHAIN_ADDRESS"
    CREDIT_CARD = "CREDIT_CARD"
    DATE = "DATE"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    GOV_ID = "GOV_ID"
    IP_ADDRESS = "IP_ADDRESS"
    KEY = "KEY"
    LICENSE_PLATE = "LICENSE_PLATE"
    LOCATION = "LOCATION"
    MEDICAL = "MEDICAL"
    NORP = "NORP"
    ORG = "ORG"
    OTHER = "OTHER"
    PASSWORD = "PASSWORD"
    PERSON = "PERSON"
    PHONE_NUMBER = "PHONE_NUMBER"
    USERNAME = "USERNAME"


class SupportedLanguages(str, Enum):
    de = "de"
    en = "en"
    es = "es"
    fr = "fr"
    it = "it"
    pt = "pt"


class Policy(BaseModel):
    policy: SupportedPolicy
    entity: SupportedEntity


class Policies(BaseModel):
    policies: list[Policy]


class PiiProcessSimpleInput(BaseModel):
    text: str = Field(
        ...,
        example="My name is John Smith, 13 years old, my phone number is example@google.com",
        description="The text to process",
    )
    lang: SupportedLanguages = Field(..., example="en", description="The language of the text")
    entities: list[SupportedEntity] = Field(
        ..., example=["AGE", "PERSON", "EMAIL_ADDRESS"], description="The entities to process"
    )
    default_policy: SupportedPolicy = Field(
        ..., example="annotate", description="The default policy to apply to all entities"
    )
    config: dict = Field(
        {},
        example={"pii-transform:main:v1": {"policy": {"PERSON": "synthetic", "EMAIL_ADDRESS": "redact"}}},
        description="The config to apply to the text",
    )


class PiiProcessOutput(BaseModel):
    output: str = Field(..., example="My name is <PERSON>.", description="The processed text")


@app.get("/")
def read_root():
    return {"message": "Welcome! See piisa.org for more information."}


@app.get("/config-options/policy")
def read_config_options_policy():
    return {"policy": sorted(substitution.POLICIES)}


@app.get("/config-options/entities")
def read_config_options_entities():
    return {"entities": sorted(PiiEnum.__dict__["_member_names_"])}


@app.get("/config-options/languages")
def read_config_options_languages():
    return {"languages": sorted(SupportedLanguages.__dict__["_member_names_"])}


@app.post("/pii-process", response_model=PiiProcessOutput)
def pii_process(input: PiiProcessSimpleInput):
    tasks = [PiiEnum.__dict__[task] for task in input.entities]
    processor = PiiTextProcessor(lang=input.lang, default_policy=input.default_policy, config=input.config, tasks=tasks)
    return {"output": processor(input.text)}


# TODO: Add a route to post transform
