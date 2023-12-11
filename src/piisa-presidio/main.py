import json
import textwrap
from enum import Enum
from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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
    en = "en"
    es = "es"
    it = "it"


class Policy(BaseModel):
    policy: SupportedPolicy
    entity: SupportedEntity


class Policies(BaseModel):
    policies: list[Policy]


class PiiProcessSimpleInput(BaseModel):
    text: str = Field(
        ...,
        example=textwrap.dedent(
            """
        Anjali Mehra was born on July 15, 1987 in the bustling city of New York. She is an accomplished author 
        and journalist who has written several best-selling novels and contributed to numerous publications. 
        Anjali grew up in a small apartment in Manhattan with her parents, both of whom were immigrants from India. 
        From a young age, she showed a keen interest in writing and storytelling, often regaling her family and 
        friends with tales of adventure and intrigue. After graduating from Columbia University with a degree in 
        English literature, Anjali began her career as a freelance writer for various magazines and websites. 
        Her work quickly gained recognition, and she soon landed a job at one of the most prestigious publishing 
        houses in the country. Over the years, Anjali has published several successful novels that have captivated
        readers around the world. Her latest book, "The Secret Garden," was released earlier this year and has
        already become a global sensation. In addition to her writing, Anjali is also known for her activism and
        philanthropy. She frequently speaks out against social justice issues and works tirelessly to raise awareness
        and funds for various causes. Despite her busy schedule, Anjali always makes time for her loved ones. She is 
        married to fellow author, David Chen, and they have two children together. When she's not working or volunteering, 
        Anjali can be found spending quality time with her family or exploring new places and cultures. If you want to 
        get in touch with Anjali, you can reach her at her fake phone number (212) 555-1234 or her made-up 
        address: 123 Main Street, New York, NY 10001.
        """
        ),
        description="The text to process",
    )
    lang: SupportedLanguages = Field(..., example="en", description="The language of the text")
    entities: list[SupportedEntity] = Field(
        [entity.name for entity in SupportedEntity],
        example=[entity.name for entity in SupportedEntity],
        description="The entities to process",
    )
    default_policy: SupportedPolicy = Field(
        "annotate", example="annotate", description="The default policy to apply to all entities"
    )
    config: dict = Field(
        {},
        example=[{"pii-transform:main:v1": {"policy": {"PERSON": "synthetic", "EMAIL_ADDRESS": "redact"}}}],
        description="The config to apply to the text",
    )


class PiiProcessOutput(BaseModel):
    output: str = Field(..., example="My name is <PERSON>.", description="The processed text")


@app.get("/")
def read_root():
    return {"message": "Welcome! See piisa.org for more information."}


# redirect /v1 to /docs
@app.get("/v1", name="redirect_to_docs")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


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
