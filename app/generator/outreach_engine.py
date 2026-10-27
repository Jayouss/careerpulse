"""Personalized Outreach Email and Resume Bullet Point Synthesis Engine"""

from typing import Dict, Any, List
from app.core.config import settings


class OutreachEngine:
    def generate_cold_email(
        self,
        candidate_name: str,
        company_name: str,
        role_title: str,
        matching_skills: List[str],
        key_project_name: str = "DocuGraph AI"
    ) -> Dict[str, str]:
        """Generate a personalized, high-converting cold outreach email."""
        skills_str = ", ".join(matching_skills[:3]) if matching_skills else "Python, TypeScript, and Distributed Systems"
        
        subject = f"Application: {role_title} at {company_name} - {candidate_name} ({skills_str})"

        body = (
            f"Hi Hiring Team at {company_name},\n\n"
            f"I came across the {role_title} opening at {company_name} and was immediately drawn to your engineering focus. "
            f"With strong experience building high-throughput systems and AI platforms using {skills_str}, "
            f"I believe I could make an immediate contribution to your team.\n\n"
            f"Recently, I architected and deployed {key_project_name} - a production-grade platform focusing on "
            f"decoupled microservices, low-latency execution, and resilient event processing with automated CI/CD.\n\n"
            f"You can review my code and system architecture directly on GitHub: https://github.com/Jayouss\n\n"
            f"I would love the opportunity to learn more about your upcoming technical milestones and discuss how my background aligns with {company_name}'s goals. "
            f"Would you be open to a brief 10-minute conversation sometime this week?\n\n"
            f"Best regards,\n"
            f"{candidate_name}\n"
            f"GitHub: https://github.com/Jayouss\n"
        )

        return {
            "subject": subject,
            "body": body
        }

    def generate_tailored_bullets(self, role_title: str, matching_skills: List[str]) -> List[str]:
        """Generate XYZ-formula resume bullet points highlighting technical impact."""
        bullets = [
            f"Architected and deployed decoupled backend services utilizing {matching_skills[0] if matching_skills else 'Python/TypeScript'}, reducing request latency by 35% across high-concurrency API workloads.",
            f"Designed and implemented resilient data processing and event delivery pipelines with automated CI/CD workflows, achieving 99.9% uptime and zero unhandled message loss.",
            f"Implemented semantic caching and automated validation guardrails, cutting third-party compute expenses by 40% while preserving sub-millisecond response times."
        ]
        return bullets


outreach_engine = OutreachEngine()
