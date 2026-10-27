"""ATS (Applicant Tracking System) Semantic Scorer and Skill Gap Analyzer"""

import math
import hashlib
from typing import Dict, Any, List, Set, Tuple
import numpy as np

from app.core.config import settings
from app.parsers.skill_extractor import skill_extractor


class ATSScorer:
    def __init__(self):
        self.dim = 256
        self.kw_weight = settings.KEYWORD_WEIGHT
        self.sem_weight = settings.SEMANTIC_WEIGHT

    def score(self, job_description: str, resume_text: str) -> Dict[str, Any]:
        """Perform full ATS evaluation: Keyword coverage, semantic match, and gap analysis."""
        # 1. Skill Extraction
        job_skills_data = skill_extractor.extract(job_description)
        resume_skills_data = skill_extractor.extract(resume_text)

        job_skills_set = set(job_skills_data["skills"])
        resume_skills_set = set(resume_skills_data["skills"])

        # 2. Skill Gap Calculations
        matching_skills = sorted(list(job_skills_set.intersection(resume_skills_set)))
        missing_skills = sorted(list(job_skills_set.difference(resume_skills_set)))
        bonus_skills = sorted(list(resume_skills_set.difference(job_skills_set)))

        # 3. Keyword Overlap & Skill Recall
        total_job_skills = max(len(job_skills_set), 1)
        keyword_recall = len(matching_skills) / total_job_skills

        # 4. Dense Semantic Similarity
        job_vec = self._embed_text(job_description)
        res_vec = self._embed_text(resume_text)
        cosine_sim = float(np.dot(job_vec, res_vec))
        semantic_score = max(0.0, min(1.0, cosine_sim))

        # 5. Composite ATS Match Score (0 - 100%)
        # In modern ATS, keyword coverage is the primary filter, enriched by semantic context
        composite_score = (0.60 * keyword_recall) + (0.40 * max(semantic_score, keyword_recall * 0.85))
        match_percentage = round(composite_score * 100, 1)

        # 6. ATS Rating Category
        if match_percentage >= 80.0:
            rating = "STRONG_MATCH"
            verdict = "Excellent callback potential. Resume naturally aligns with job requirements."
        elif match_percentage >= 60.0:
            rating = "GOOD_MATCH"
            verdict = "Competitive candidate. Adding 1-2 missing keywords will dramatically boost ATS rank."
        elif match_percentage >= 40.0:
            rating = "MODERATE_MATCH"
            verdict = "Potential match, but significant skill gaps detected. Customization strongly recommended."
        else:
            rating = "LOW_MATCH"
            verdict = "Low ATS keyword alignment. High risk of automated rejection by initial screening filter."

        # 7. Actionable Recommendations
        recommendations = self._generate_recommendations(missing_skills, match_percentage)

        return {
            "match_score_pct": match_percentage,
            "rating": rating,
            "verdict": verdict,
            "skill_metrics": {
                "job_skills_count": len(job_skills_set),
                "resume_skills_count": len(resume_skills_set),
                "matched_count": len(matching_skills),
                "missing_count": len(missing_skills),
            },
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "bonus_skills": bonus_skills[:10],
            "recommendations": recommendations,
        }

    def _embed_text(self, text: str) -> np.ndarray:
        """Deterministic normalized semantic vector representation."""
        words = text.lower().split()
        vec = np.zeros(self.dim, dtype=np.float32)

        if not words:
            vec[0] = 1.0
            return vec

        for i, word in enumerate(words):
            weight = 1.0 / (math.log(i + 2) + 0.1)
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            vec[idx] += weight

            if i < len(words) - 1:
                bigram = f"{word}_{words[i+1]}"
                h_bi = int(hashlib.md5(bigram.encode("utf-8")).hexdigest(), 16)
                idx_bi = h_bi % self.dim
                vec[idx_bi] += weight * 1.5

        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _generate_recommendations(self, missing_skills: List[str], score: float) -> List[str]:
        recs = []
        if missing_skills:
            top_missing = ", ".join(missing_skills[:4])
            recs.append(f"Incorporate missing core technologies: {top_missing} into your Technical Skills section.")
            recs.append(f"Add at least one project bullet point referencing practical usage of {missing_skills[0]}.")

        if score < 75.0:
            recs.append("Mirror key terminology from the job description directly in your professional summary.")

        recs.append("Ensure project impact is quantified with metrics (e.g. latency reduced by X%, throughput increased by Y%).")
        return recs


ats_scorer = ATSScorer()
