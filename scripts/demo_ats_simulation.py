"""CareerPulse: Interactive ATS Optimization & Application Demonstration Script

Demonstrates:
1. Parsing & Normalizing Job Description Requirements
2. Candidate Skill Extraction & Gap Detection
3. ATS Compatibility Scoring (Dense Semantic Similarity + Keyword Recall)
4. Personalized Cold Outreach Email Generation
5. Tailored XYZ-formula Resume Bullet Points Synthesis
"""

import sys
import os
import json

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.parsers.skill_extractor import skill_extractor
from app.matcher.ats_scorer import ats_scorer
from app.generator.outreach_engine import outreach_engine


def print_header(title: str):
    print("\n" + "=" * 75)
    print(f">> {title.upper()}")
    print("=" * 75)


def run_demo():
    print_header("CareerPulse - ATS Resume Optimizer & Application Tailor")

    # Sample Job Description
    job_description = """
    Role: Backend & AI Engineer at Nexus Systems (YC W24)
    Location: Remote
    
    About the Role:
    We are building real-time autonomous agent workflows. We are seeking a Backend & AI Engineer
    with deep hands-on experience in Python (FastAPI), TypeScript (Node.js), and PostgreSQL (pgvector).
    
    Requirements:
    - Proficiency in Python, FastAPI, and asynchronous backend development.
    - Hands-on experience with TypeScript / Node.js and real-time WebSockets.
    - Experience building RAG pipelines, vector search, and semantic caching.
    - Solid understanding of message queues (Redis), rate limiting, and event-driven architecture.
    - Docker containerization, automated CI/CD with GitHub Actions, and unit testing.
    - Bonus: Knowledge of OWASP LLM security, prompt injection defense, and Kubernetes.
    """

    # Candidate Resume Summary (Based on user's portfolio)
    candidate_resume = """
    Jay — AI & Backend Engineer
    GitHub: https://github.com/Jayouss
    
    Technical Summary:
    Full-lifecycle backend and AI engineer specializing in decoupled microservices,
    high-throughput event relays, and LLM security.
    
    Core Skills:
    - Languages: Python, TypeScript, JavaScript, SQL
    - Backend: FastAPI, Node.js, Express, REST APIs, WebSockets, gRPC
    - AI & Data: RAG, pgvector, Vector Search, Semantic Cache, PyTorch
    - Systems: Redis, PostgreSQL, SQLite, Message Queue, Rate Limiting, Idempotency, HMAC
    - DevOps: Docker, Docker Compose, GitHub Actions, CI/CD, Git, Linux
    - Security: OWASP Top 10 for LLMs, Prompt Injection Firewall, PII Masking
    
    Featured Projects:
    1. DocuGraph AI: Production Decoupled Agentic RAG Platform (FastAPI + Node.js Gateway)
    2. HookPulse: Resilient Webhook Relay with Exponential Backoff and DLQ
    3. PromptShield: Sub-millisecond LLM Security Gateway and PII Redactor
    """

    # -------------------------------------------------------------
    # Step 1: Extract Skills
    # -------------------------------------------------------------
    print_header("Step 1: Skill Extraction & Categorization")
    job_skills = skill_extractor.extract(job_description)
    print(f"🎯 Job Extracted Skills ({job_skills['total_unique_skills']}):")
    for cat, items in job_skills["by_category"].items():
        print(f"   - {cat.replace('_', ' ').title()}: {', '.join(items)}")

    # -------------------------------------------------------------
    # Step 2: ATS Scoring & Gap Analysis
    # -------------------------------------------------------------
    print_header("Step 2: ATS Match Scoring & Gap Analysis")
    result = ats_scorer.score(job_description, candidate_resume)

    print(f"📊 ATS Match Score: {result['match_score_pct']}% [{result['rating']}]")
    print(f"💡 Verdict: {result['verdict']}")
    print(f"\n✅ Matching Skills ({len(result['matching_skills'])}):")
    print(f"   {', '.join(result['matching_skills'])}")
    
    if result["missing_skills"]:
        print(f"\n⚠️ Missing / Gap Skills ({len(result['missing_skills'])}):")
        print(f"   {', '.join(result['missing_skills'])}")
    else:
        print("\n✨ Zero Core Skill Gaps Detected!")

    print("\n📋 ATS Optimization Recommendations:")
    for rec in result["recommendations"]:
        print(f"   • {rec}")

    # -------------------------------------------------------------
    # Step 3: Personalized Cold Email Outreach
    # -------------------------------------------------------------
    print_header("Step 3: Personalized Cold Outreach Email")
    email = outreach_engine.generate_cold_email(
        candidate_name="Jay",
        company_name="Nexus Systems",
        role_title="Backend & AI Engineer",
        matching_skills=result["matching_skills"],
        key_project_name="DocuGraph AI & PromptShield"
    )

    print(f"Subject: {email['subject']}\n")
    print(email['body'])

    # -------------------------------------------------------------
    # Step 4: Tailored Resume Bullet Points
    # -------------------------------------------------------------
    print_header("Step 4: Tailored Resume Bullet Points (XYZ Formula)")
    bullets = outreach_engine.generate_tailored_bullets(
        role_title="Backend & AI Engineer",
        matching_skills=result["matching_skills"]
    )
    for b in bullets:
        print(f"  * {b}")

    print_header("Demonstration Completed Successfully!")


if __name__ == "__main__":
    run_demo()
