"""
Schemas of the AIoD resources.

Note that these objects are different from the ORM objects defined in the database. This leads to
code duplication, so it is not ideal. But it makes it possible to differentiate between the database
objects and the externally used AIoD schemas. The dataset, for example, contains keywords,
which should be a separate object inside a separate table in the database (so that we can easily
search for all datasets having the same keyword). In the external schema, a set of strings is
easier.
"""
from datetime import datetime
from typing import Set, List, Optional

from pydantic import BaseModel, Field


class AIoDDistribution(BaseModel):
    content_url: str = Field(max_length=150)
    content_size_kb: int | None
    description: str | None = Field(max_length=5000)
    name: str | None = Field(max_length=150)
    encoding_format: str | None = Field(max_length=150)


class AIoDMeasurementValue(BaseModel):
    variable: str | None
    technique: str | None


class AIoDPublication(BaseModel):
    """The complete metadata of a publication. For now, only a couple of fields are shown,
    we have to decide which fields to use."""

    id: int | None
    title: str | None = Field(max_length=250)
    url: str | None = Field(max_length=250)


class AIoDDataset(BaseModel):
    """
    The complete metadata of a dataset in AIoD format.
    """

    id: int | None
    description: str = Field(max_length=5000)
    name: str = Field(max_length=150)
    node: str = Field(max_length=30)
    node_specific_identifier: str = Field(max_length=250)
    same_as: str = Field(max_length=150)

    # Recommended fields
    creator: str | None = Field(max_length=150)
    date_modified: datetime | None
    date_published: datetime | None
    funder: str | None
    is_accessible_for_free: bool | None
    issn: str | None = Field(max_length=8, min_length=8)
    size: int | None
    spatial_coverage: str | None = Field(max_length=500)
    temporal_coverage_from: datetime | None
    temporal_coverage_to: datetime | None
    version: str | None = Field(max_length=150)

    # Relations
    license: str | None = Field(max_length=150)
    has_parts: Set[str] = Field(
        description="Identifiers of datasets that are part of this " "dataset.",
        default_factory=set,
    )
    is_part: Set[str] = Field(
        description="Identifiers of datasets this dataset is part of.", default_factory=set
    )
    alternate_names: Set[str] = Field(default_factory=set)
    citations: Set[str] | List[AIoDPublication] = Field(
        description="Identifiers of publications linked to this dataset, or the actual "
        "publications",
        default_factory=set,
    )
    distributions: List[AIoDDistribution] = []
    keywords: Set[str] = Field(default_factory=set)
    measured_values: List[AIoDMeasurementValue] = Field(default_factory=list)


class Tag(BaseModel):
    """The complete metadata for tags"""

    tag: str = Field(max_length=250)
    id: int | None


class BusinessCategory(BaseModel):
    """The complete metadata of a business category"""

    category: str = Field(max_length=250)
    id: int | None


class NewsCategory(BaseModel):
    """The complete metadata of a news category"""

    category: str = Field(max_length=250)
    parent_id: int | None
    id: int | None


class News(BaseModel):
    """The complete metadata for news entity"""

    title: str = Field(max_length=500)
    date_modified: datetime
    body: str = Field(max_length=2000)
    headline: str = Field(max_length=500)
    alternative_headline: Optional[str] = Field(max_length=500)
    section: str = Field(max_length=500)
    word_count: int

    media: Optional[list[str]]
    source: Optional[str]
    news_categories: Optional[list[str]]
    business_categories: Optional[list[str]]
    tags: Optional[list[str]]
    id: int | None
