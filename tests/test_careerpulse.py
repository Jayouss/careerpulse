"""Test Suite for CareerPulse ATS AI Optimizer"""

import sys
import os
import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.parsers.skill_extractor import skill_extractor
from app.matcher.ats_scorer import ats_scorer
from app.generator.outreach_engine import outreach_engine
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_skill_extractor_normalization():
    sample = "Looking for an engineer skilled in Python, node.js, postgres, Docker, and k8s."
    data = skill_extractor.extract(sample)

    assert "Python" in data["skills"]
    assert "Node.js" in data["skills"]
    assert "PostgreSQL" in data["skills"]
    assert "Docker" in data["skills"]
    assert "Kubernetes" in data["skills"]
    assert data["total_unique_skills"] >= 5


def test_ats_scorer_high_match():
    job = "We need a Senior Backend Engineer with Python, FastAPI, PostgreSQL, Redis, and Docker."
    resume = "Backend Developer specializing in Python, FastAPI, PostgreSQL, Redis, Docker, and TypeScript."

    result = ats_scorer.score(job, resume)
    assert result["match_score_pct"] >= 75.0
    assert result["rating"] in ["STRONG_MATCH", "GOOD_MATCH"]
    assert "FastAPI" in result["matching_skills"]
    assert len(result["missing_skills"]) == 0


def test_ats_scorer_gap_detection():
    job = "Requirements: Go, Kubernetes, Terraform, AWS, and gRPC."
    resume = "Experienced in Python, Django, SQLite, and HTML."

    result = ats_scorer.score(job, resume)
    assert result["match_score_pct"] < 50.0
    assert "Kubernetes" in result["missing_skills"]
    assert "Terraform" in result["missing_skills"]
    assert len(result["recommendations"]) > 0


def test_outreach_engine_cold_email():
    email = outreach_engine.generate_cold_email(
        candidate_name="Jay",
        company_name="Acme Corp",
        role_title="Backend Engineer",
        matching_skills=["Python", "FastAPI", "Docker"],
        key_project_name="DocuGraph AI"
    )

    assert "Acme Corp" in email["subject"]
    assert "Jay" in email["body"]
    assert "DocuGraph AI" in email["body"]
    assert "https://github.com/Jayouss" in email["body"]


def test_api_match_and_tailor_endpoints():
    job_desc = "Seeking Backend Engineer proficient in Python, FastAPI, Docker, and PostgreSQL."
    resume_desc = "Software Engineer with expertise in Python, FastAPI, PostgreSQL, and Redis."

    # Match endpoint
    match_res = client.post("/api/v1/match", json={
        "job_description": job_desc,
        "resume_text": resume_desc
    })
    assert match_res.status_code == 200
    assert "match_score_pct" in match_res.json()
    assert "matching_skills" in match_res.json()

    # Tailor endpoint
    tailor_res = client.post("/api/v1/tailor", json={
        "candidate_name": "Jay",
        "company_name": "TechCorp",
        "role_title": "AI Backend Engineer",
        "job_description": job_desc,
        "resume_text": resume_desc
    })
    assert tailor_res.status_code == 200
    tailor_data = tailor_res.json()
    assert "outreach_email" in tailor_data
    assert "tailored_resume_bullets" in tailor_data
    assert len(tailor_data["tailored_resume_bullets"]) >= 3


def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
