"""Tech Skill Extraction and Normalization Engine"""

import re
from typing import Dict, List, Set, Any


class SkillExtractor:
    def __init__(self):
        # Comprehensive Tech Stack Taxonomy
        self.taxonomy: Dict[str, List[str]] = {
            "languages": [
                "python", "typescript", "javascript", "golang", "go", "rust",
                "java", "c++", "c#", "ruby", "php", "sql", "bash"
            ],
            "backend_frameworks": [
                "fastapi", "django", "flask", "express", "nestjs", "nodejs",
                "node.js", "spring boot", "fiber", "gin", "graphql", "rest api", "grpc"
            ],
            "ai_and_ml": [
                "rag", "langchain", "llamaindex", "vector search", "pgvector",
                "embeddings", "pytorch", "tensorflow", "openai", "llm", "nlp",
                "huggingface", "semantic cache", "reranker", "agentic"
            ],
            "databases_and_cache": [
                "postgresql", "postgres", "mysql", "mongodb", "redis",
                "sqlite", "dynamodb", "elasticsearch", "cassandra", "qdrant"
            ],
            "devops_and_cloud": [
                "docker", "kubernetes", "k8s", "aws", "gcp", "azure", "linux",
                "ci/cd", "github actions", "terraform", "helm", "nginx", "git"
            ],
            "architecture_and_systems": [
                "microservices", "event-driven", "websockets", "message queue",
                "rate limiting", "idempotency", "dead letter queue", "caching",
                "distributed systems", "owasp", "security", "hmac"
            ]
        }

        # Canonical aliases mapping with standard casing
        self.aliases: Dict[str, str] = {
            "fastapi": "FastAPI",
            "postgresql": "PostgreSQL",
            "postgres": "PostgreSQL",
            "mysql": "MySQL",
            "mongodb": "MongoDB",
            "sqlite": "SQLite",
            "dynamodb": "DynamoDB",
            "redis": "Redis",
            "node": "Node.js",
            "nodejs": "Node.js",
            "node.js": "Node.js",
            "golang": "Go",
            "go": "Go",
            "py": "Python",
            "python": "Python",
            "ts": "TypeScript",
            "typescript": "TypeScript",
            "js": "JavaScript",
            "javascript": "JavaScript",
            "ci/cd": "CI/CD",
            "owasp": "OWASP",
            "k8s": "Kubernetes",
            "kubernetes": "Kubernetes",
            "docker": "Docker",
            "github action": "GitHub Actions",
            "github actions": "GitHub Actions",
            "rest": "REST API",
            "restful": "REST API",
            "rest api": "REST API",
            "graphql": "GraphQL",
            "grpc": "gRPC",
            "llm": "LLM",
            "llms": "LLM",
            "rag": "RAG",
            "vectors": "Vector Search",
            "vector search": "Vector Search",
            "pgvector": "pgvector",
            "langchain": "LangChain",
            "llamaindex": "LlamaIndex",
            "pytorch": "PyTorch",
            "tensorflow": "TensorFlow"
        }

    def extract(self, text: str) -> Dict[str, Any]:
        """Extract and categorize tech skills from job descriptions or resumes."""
        if not text:
            return {"total_unique_skills": 0, "skills": [], "by_category": {}}

        text_lower = text.lower()
        extracted_skills: Set[str] = set()
        skills_by_category: Dict[str, List[str]] = {}

        for category, keywords in self.taxonomy.items():
            found_in_category = []
            for kw in keywords:
                # Word boundary search
                pattern = r'(?:\b|_)' + re.escape(kw) + r'(?:\b|_)'
                if re.search(pattern, text_lower):
                    canonical_name = self.aliases.get(kw, kw.title() if len(kw) > 3 else kw.upper())
                    extracted_skills.add(canonical_name)
                    if canonical_name not in found_in_category:
                        found_in_category.append(canonical_name)

            if found_in_category:
                skills_by_category[category] = sorted(found_in_category)

        sorted_all = sorted(list(extracted_skills))
        return {
            "total_unique_skills": len(sorted_all),
            "skills": sorted_all,
            "by_category": skills_by_category
        }


skill_extractor = SkillExtractor()
