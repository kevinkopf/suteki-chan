from datetime import datetime
from typing import Literal, List
from pydantic import BaseModel, Field


class CommentEventModel(BaseModel):
    suteki_request_type: Literal['Note Hook']
    object_kind: str
    event_type: str
    user: dict
    project_id: int
    project: dict
    repository: dict
    object_attributes: dict
    commit: dict | None
    merge_request: dict | None
    issue: dict | None
    snippet: dict | None


class DeploymentEventModel(BaseModel):
    suteki_request_type: Literal['Deployment Hook']
    object_kind: str
    status: str
    status_changed_at: datetime
    deployment_id: int
    deployable_id: int
    deployable_url: str
    environment: str
    environment_tier: str
    environment_slug: str
    environment_external_url: str
    project: dict
    short_sha: str
    user: dict
    user_url: str
    commit_url: str
    commit_title: str


class FeatureFlagEventModel(BaseModel):
    suteki_request_type: Literal['Feature Flag Hook']
    object_kind: str
    project: dict
    user: dict
    user_url: str
    object_attributes: dict


class GroupMemberEventModel(BaseModel):
    suteki_request_type: Literal['Member Hook']
    created_at: datetime
    updated_at: datetime
    group_name: str
    group_path: str
    group_id: int
    user_username: str
    user_name: str
    user_email: str
    user_id: int
    group_access: str
    group_plan: str | None
    expires_at: datetime = None
    event_name: str


class IssueEventModel(BaseModel):
    suteki_request_type: Literal['Issue Hook']
    object_kind: str
    event_type: str
    user: dict
    project: dict
    object_attributes: dict
    repository: dict
    assignees: List[dict]
    assignee: dict
    labels: List[dict]
    changes: dict


class JobEventModel(BaseModel):
    suteki_request_type: Literal['Job Hook']
    object_kind: str
    ref: str
    tag: bool
    before_sha: str
    sha: str
    build_id: int
    build_name: str
    build_stage: str
    build_status: str
    build_created_at: datetime
    build_started_at: datetime = None
    build_finished_at: datetime = None
    build_duration: float | None
    build_queued_duration: float
    build_allow_failure: bool
    build_failure_reason: str
    retries_count: int
    pipeline_id: int
    project_id: int
    project_name: str
    user: dict
    commit: dict
    repository: dict
    runner: dict
    environment: str | None


class MergeRequestEventModel(BaseModel):
    suteki_request_type: Literal['Merge Request Hook']
    object_kind: str
    event_type: str
    user: dict
    project: dict
    repository: dict
    object_attributes: dict
    labels: List[dict]
    changes: dict
    assignees: List[dict]
    reviewers: List[dict]


class PipelineEventModel(BaseModel):
    suteki_request_type: Literal['Pipeline Hook']
    object_kind: str
    object_attributes: dict
    merge_request: dict
    user: dict
    project: dict
    commit: dict
    source_pipeline: dict
    builds: List[dict]


class PushEventModel(BaseModel):
    suteki_request_type: Literal['Push Hook']
    object_kind: str
    event_name: str
    before: str
    after: str
    ref: str
    checkout_sha: str
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    user_avatar: str
    project_id: int
    project: dict
    repository: dict
    commits: List[dict]
    total_commits_count: int


class ReleaseEventModel(BaseModel):
    suteki_request_type: Literal['Release Hook']
    id: int
    created_at: datetime
    description: str
    name: str
    released_at: datetime
    tag: str
    object_kind: str
    project: dict
    url: str
    action: str
    assets: dict
    commit: dict


class SubgroupEventModel(BaseModel):
    suteki_request_type: Literal['Subgroup Hook']
    created_at: datetime
    updated_at: datetime
    event_name: str
    name: str
    path: str
    full_path: str
    group_id: int
    parent_group_id: int
    parent_name: str
    parent_path: str
    parent_full_path: str


class TagEventModel(BaseModel):
    suteki_request_type: Literal['Tag Push Hook']
    object_kind: str
    event_name: str
    before: str
    after: str
    ref: str
    checkout_sha: str
    user_id: int
    user_name: str
    user_avatar: str
    project_id: int
    project: dict
    repository: dict
    commits: List[dict]
    total_commits_count: int


class WikiPageEventModel(BaseModel):
    suteki_request_type: Literal['Wiki Page Hook']
    object_kind: str
    user: dict
    project: dict
    wiki: dict
    object_attributes: dict


class Model(BaseModel):
    event: CommentEventModel | \
         DeploymentEventModel | \
         FeatureFlagEventModel | \
         GroupMemberEventModel | \
         IssueEventModel | \
         JobEventModel | \
         MergeRequestEventModel | \
         PipelineEventModel | \
         PushEventModel | \
         ReleaseEventModel | \
         SubgroupEventModel | \
         TagEventModel | \
         WikiPageEventModel \
         = Field(..., discriminator='suteki_request_type')
