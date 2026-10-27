"""CareerPulse CLI Tool for Terminal Operations"""

import sys
import os
import argparse
import json

# Ensure console UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.matcher.ats_scorer import ats_scorer
from app.generator.outreach_engine import outreach_engine
from app.parsers.skill_extractor import skill_extractor


def main():
    parser = argparse.ArgumentParser(description="CareerPulse — ATS Optimizer & Application Tailor CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Match command
    match_parser = subparsers.add_parser("match", help="Match resume against job description")
    match_parser.add_argument("--job", required=True, help="Job description text or file path")
    match_parser.add_argument("--resume", required=True, help="Resume text or file path")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract tech stack skills from text")
    extract_parser.add_argument("--text", required=True, help="Text to extract skills from")

    args = parser.parse_args()

    if args.command == "match":
        job_text = open(args.job, encoding="utf-8").read() if os.path.exists(args.job) else args.job
        res_text = open(args.resume, encoding="utf-8").read() if os.path.exists(args.resume) else args.resume

        result = ats_scorer.score(job_text, res_text)
        print("\n" + "=" * 60)
        print(f"📊 ATS MATCH SCORE: {result['match_score_pct']}% ({result['rating']})")
        print("=" * 60)
        print(f"Verdict: {result['verdict']}")
        print(f"\n✅ Matching Skills ({len(result['matching_skills'])}): {', '.join(result['matching_skills'])}")
        print(f"❌ Missing Core Skills ({len(result['missing_skills'])}): {', '.join(result['missing_skills'])}")
        print("\n💡 Recommendations:")
        for r in result["recommendations"]:
            print(f"  - {r}")

    elif args.command == "extract":
        text = open(args.text, encoding="utf-8").read() if os.path.exists(args.text) else args.text
        skills = skill_extractor.extract(text)
        print(json.dumps(skills, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
