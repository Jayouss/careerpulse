"""CareerPulse API v1 Endpoints"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.matcher.ats_scorer import ats_scorer
from app.parsers.skill_extractor import skill_extractor
from app.generator.outreach_engine import outreach_engine

router = APIRouter(tags=["CareerPulse Core"])


# --- Schemas ---
class MatchRequest(BaseModel):
    job_description: str = Field(..., json_schema_extra={"example": "We are seeking a Backend Engineer with Python, FastAPI, Docker, and PostgreSQL experience."})
    resume_text: str = Field(..., json_schema_extra={"example": "Software Engineer experienced in Python, FastAPI, Docker, TypeScript, and Redis."})


class TailorRequest(BaseModel):
    candidate_name: str = Field(default="Jay", json_schema_extra={"example": "Jay"})
    company_name: str = Field(..., json_schema_extra={"example": "Stripe"})
    role_title: str = Field(..., json_schema_extra={"example": "Backend Software Engineer"})
    job_description: str = Field(...)
    resume_text: str = Field(...)
    key_project: Optional[str] = "DocuGraph AI"


class ExtractSkillsRequest(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Proficient in Python, FastAPI, TypeScript, PostgreSQL, and Kubernetes."})


# --- Endpoints ---

@router.post("/api/v1/match")
async def match_resume_to_job(payload: MatchRequest):
    """Calculate ATS compatibility score, identify skill gaps, and return actionable advice."""
    if not payload.job_description.strip() or not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Both job_description and resume_text are required.")

    result = ats_scorer.score(payload.job_description, payload.resume_text)
    return result


@router.post("/api/v1/tailor")
async def generate_tailored_application(payload: TailorRequest):
    """Generate complete personalized application dossier: ATS score, customized email, and bullet points."""
    if not payload.job_description.strip() or not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Both job_description and resume_text are required.")

    match_result = ats_scorer.score(payload.job_description, payload.resume_text)

    email = outreach_engine.generate_cold_email(
        candidate_name=payload.candidate_name,
        company_name=payload.company_name,
        role_title=payload.role_title,
        matching_skills=match_result["matching_skills"],
        key_project_name=payload.key_project or "DocuGraph AI"
    )

    bullets = outreach_engine.generate_tailored_bullets(
        role_title=payload.role_title,
        matching_skills=match_result["matching_skills"]
    )

    return {
        "candidate": payload.candidate_name,
        "company": payload.company_name,
        "role": payload.role_title,
        "ats_metrics": match_result,
        "outreach_email": email,
        "tailored_resume_bullets": bullets
    }


@router.post("/api/v1/skills/extract")
async def extract_skills_endpoint(payload: ExtractSkillsRequest):
    """Extract and categorize tech stack entities from any text."""
    return skill_extractor.extract(payload.text)


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }
