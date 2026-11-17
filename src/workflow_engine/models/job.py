import uuid
from datetime import datetime, UTC
from typing import Any

from sqlalchemy import DateTime, String, Integer, CheckConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from workflow_engine.database.base import Base
from workflow_engine.core.job import JobStatus

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    task_name: Mapped[str] = mapped_column(
        String(258),
        nullable=False
    )
    status: Mapped[JobStatus] = mapped_column(
        SQLEnum(
            JobStatus,
            name="job_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=JobStatus.PENDING,
        server_default="pending",
        nullable=False
    )
    parameters: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False
    )
    attempts: Mapped[int] = mapped_column(
        Integer(),
        default=0,
        server_default="0",
        nullable=False
    )
    max_attempts: Mapped[int] = mapped_column(
        Integer(),
        default=3,
        server_default="3",
        nullable=False
    )
    worker_id: Mapped[str | None] = mapped_column(
        String(258),
        nullable=True
    )
    claim_generation: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False
    )
    lease_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("attempts >= 0", name="ck_jobs_attempts"),
        CheckConstraint("max_attempts >= 1", name="ck_jobs_max_attempts")
    )

