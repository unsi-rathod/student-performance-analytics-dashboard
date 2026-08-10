"""
==========================================================
Student Performance Analytics Project
Phase 4 - AI-Assisted Intervention Notes (Prototype)

Author  : Unsi Rathod
Purpose : Turn flagged at-risk students into short, personalized
          coaching notes using an LLM (Claude) -- grounded in
          each student's actual scores, not generic advice.

This script:
1. Reads the feature-engineered dataset
2. Filters to students flagged Needs_Intervention == 'Yes'
3. For each one, builds a data-grounded prompt and calls the
   Claude API to generate a short coaching note that explicitly
   distinguishes a COMPREHENSION gap (can't recognize/recall the
   concept -- shows up in MCQ / short-answer weakness) from an
   EXECUTION gap (understands but can't apply/articulate it --
   shows up in Long Answer / Case Based weakness).
4. Falls back to a rule-based templated note if no API key is
   set, so the script is always runnable and demoable without
   requiring credentials.
5. Saves results to a CSV for review or import into Power BI.
==========================================================
"""

import logging
import os
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

INPUT_FILE = Path("student_performance_feature_engineered.csv")
OUTPUT_FILE = Path("intervention_notes.csv")

# ---------------------------------------------------------
# Which question types signal which kind of gap
# ---------------------------------------------------------

COMPREHENSION_TYPES = {"MCQ", "2-Mark Questions", "2 - Mark"}
EXECUTION_TYPES = {"Long Answer", "Case Based", "3-Mark Questions", "3 - Mark"}


def classify_gap_type(weakest_section: str) -> str:
    """
    Maps a student's weakest question type to a gap category.
    """
    if weakest_section in COMPREHENSION_TYPES:
        return "comprehension"
    if weakest_section in EXECUTION_TYPES:
        return "execution"
    return "mixed"


# ---------------------------------------------------------
# Load and filter
# ---------------------------------------------------------

def load_flagged_students(path: Path) -> pd.DataFrame:
    logging.info("Reading feature-engineered dataset...")
    df = pd.read_csv(path)

    required = [
        "NAME", "SECTION", "Annual_Percentage", "Improvement_Percentage",
        "Risk_Level", "Needs_Intervention", "Weakest_Section", "Growth_Category",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    flagged = df[df["Needs_Intervention"] == "Yes"].copy()
    logging.info(f"{len(flagged)} students flagged for intervention.")
    return flagged


# ---------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------

def build_prompt(row: pd.Series) -> str:
    gap_type = classify_gap_type(row["Weakest_Section"])

    return f"""You are an academic coach writing a short, practical note for a
teacher about one student who has been flagged for intervention.

Student data:
- Section: {row['SECTION']}
- Annual score: {row['Annual_Percentage']}%
- Change from Half-Yearly to Annual: {row['Improvement_Percentage']} points ({row['Growth_Category']})
- Risk level: {row['Risk_Level']}
- Weakest question type: {row['Weakest_Section']} (likely a {gap_type} gap)

Write a 2-3 sentence coaching note for the teacher that:
1. States plainly whether this looks like a comprehension gap (can't
   recognize/recall the concept) or an execution gap (understands the
   concept but struggles to apply or articulate it), based on the
   weakest question type above.
2. Suggests one concrete, specific next step for the teacher to try.
Do not use generic phrases like "needs more practice" without saying
what kind of practice. Keep it to 3 sentences maximum."""


# ---------------------------------------------------------
# Rule-based fallback (no API key needed)
# ---------------------------------------------------------

def fallback_note(row: pd.Series) -> str:
    gap_type = classify_gap_type(row["Weakest_Section"])

    if gap_type == "comprehension":
        return (
            f"{row['NAME']} shows a comprehension gap, weakest in "
            f"{row['Weakest_Section']} -- suggesting difficulty recognizing "
            f"or recalling the underlying concept rather than applying it. "
            f"Recommend a short concept-recap session before assigning more "
            f"practice problems."
        )
    if gap_type == "execution":
        return (
            f"{row['NAME']} shows an execution gap, weakest in "
            f"{row['Weakest_Section']} -- likely understands the material "
            f"but struggles to structure or articulate a full answer. "
            f"Recommend guided practice writing out step-by-step solutions "
            f"rather than re-teaching the concept itself."
        )
    return (
        f"{row['NAME']} shows a mixed performance pattern, weakest in "
        f"{row['Weakest_Section']}. Recommend a short one-on-one check-in "
        f"to pinpoint whether the issue is conceptual or applied before "
        f"assigning targeted practice."
    )


# ---------------------------------------------------------
# Claude API call
# ---------------------------------------------------------

def generate_note_with_claude(client, row: pd.Series) -> str:
    prompt = build_prompt(row)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    flagged = load_flagged_students(INPUT_FILE)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = None

    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            logging.info("ANTHROPIC_API_KEY found -- using Claude for notes.")
        except ImportError:
            logging.warning(
                "anthropic package not installed (pip install anthropic). "
                "Falling back to rule-based notes."
            )
    else:
        logging.warning(
            "No ANTHROPIC_API_KEY set -- using rule-based fallback notes. "
            "Set the environment variable and install `anthropic` to "
            "generate real LLM-written notes."
        )

    notes = []
    for _, row in flagged.iterrows():
        if client:
            try:
                note = generate_note_with_claude(client, row)
            except Exception as error:
                logging.error(f"API call failed for {row['NAME']}: {error}")
                note = fallback_note(row)
        else:
            note = fallback_note(row)

        notes.append({
            "NAME": row["NAME"],
            "SECTION": row["SECTION"],
            "Annual_Percentage": row["Annual_Percentage"],
            "Risk_Level": row["Risk_Level"],
            "Weakest_Section": row["Weakest_Section"],
            "Gap_Type": classify_gap_type(row["Weakest_Section"]),
            "Intervention_Note": note,
        })

    result_df = pd.DataFrame(notes)
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "=" * 55)
    print("INTERVENTION NOTES GENERATED")
    print("=" * 55)
    print(f"Students processed : {len(result_df)}")
    print(f"Output file         : {OUTPUT_FILE}")
    print("=" * 55)
    print("\nSample notes:\n")
    for note in result_df["Intervention_Note"].head(3):
        print(f"- {note}\n")


if __name__ == "__main__":
    main()
