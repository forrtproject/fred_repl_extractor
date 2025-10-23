# Desired structure or Replica
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field


@dataclass
class ReplicationStudy:
    """Data model for replication studies"""
    replication_doi: str
    replication_reference: str
    original_doi: Optional[str] = None
    original_reference: Optional[str] = None
    replication_title: Optional[str] = None
    original_title: Optional[str] = None
    abstract: Optional[str] = None