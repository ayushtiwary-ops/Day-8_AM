"""Student Admission Decision System.

Day 8 AM -- if/elif/else, comparison and logical operators
IIT Gandhinagar | PG Diploma AI-ML & Agentic AI Engineering
"""

CUTOFFS = {"general": 75, "obc": 65, "sc_st": 55}
MIN_GPA = 7.0
SCHOLARSHIP_THRESHOLD = 95


def get_entrance_score():
    """Collect and validate entrance score (0-100)."""
    while True:
        try:
            score = float(input("Entrance Score (0-100): "))
            if 0 <= score <= 100:
                return score
            print("  Error: Score must be between 0 and 100.")
        except ValueError:
            print("  Error: Please enter a valid number.")


def get_gpa():
    """Collect and validate GPA (0-10)."""
    while True:
        try:
            gpa = float(input("GPA (0.0 - 10.0): "))
            if 0 <= gpa <= 10:
                return gpa
            print("  Error: GPA must be between 0 and 10.")
        except ValueError:
            print("  Error: Please enter a valid number.")


def get_recommendation():
    """Collect and validate recommendation letter status."""
    while True:
        rec = input("Recommendation Letter (yes/no): ").strip().lower()
        if rec in ("yes", "no"):
            return rec == "yes"
        print("  Error: Enter 'yes' or 'no'.")


def get_category():
    """Collect and validate student category."""
    valid = ("general", "obc", "sc_st")
    while True:
        cat = input("Category (general / obc / sc_st): ").strip().lower()
        if cat in valid:
            return cat
        print(f"  Error: Must be one of {valid}.")


def get_extracurricular():
    """Collect and validate extracurricular score (0-10)."""
    while True:
        try:
            score = float(input("Extracurricular Score (0-10): "))
            if 0 <= score <= 10:
                return score
            print("  Error: Score must be between 0 and 10.")
        except ValueError:
            print("  Error: Please enter a valid number.")


def calculate_bonus(entrance_score, has_rec, extra_score):
    """Apply bonus rules and return effective score details.

    Args:
        entrance_score (float): Raw entrance score.
        has_rec (bool): Whether student has a recommendation letter.
        extra_score (float): Extracurricular score.

    Returns:
        tuple: (effective_score, bonus_total, bonus_description)
    """
    bonus = 0
    parts = []

    if has_rec:
        bonus += 5
        parts.append("+5 (recommendation)")

    if extra_score > 8:
        bonus += 3
        parts.append("+3 (extracurricular)")

    effective = entrance_score + bonus
    desc = " ".join(parts) if parts else "none"
    return effective, bonus, desc


def evaluate_admission(entrance_score, gpa, has_rec, category, extra_score):
    """Core admission decision logic.

    Args:
        entrance_score (float): Raw entrance score.
        gpa (float): Student GPA.
        has_rec (bool): Recommendation letter status.
        category (str): Student category (general/obc/sc_st).
        extra_score (float): Extracurricular score.

    Returns:
        tuple: (result, reason, effective_score, bonus_desc)
    """
    effective_score, bonus, bonus_desc = calculate_bonus(
        entrance_score, has_rec, extra_score
    )
    cutoff = CUTOFFS[category]
    cat_display = category.upper().replace("_", "/")

    # scholarship auto-admit -- checked on raw score before bonus
    if entrance_score >= SCHOLARSHIP_THRESHOLD:
        return (
            "ADMITTED (Scholarship)",
            "Entrance score >= 95 -- automatic scholarship admit",
            effective_score,
            bonus_desc,
        )

    # GPA is a hard gate -- no bonus can override it
    if gpa < MIN_GPA:
        return (
            "REJECTED",
            f"GPA {gpa} is below the minimum requirement of {MIN_GPA}",
            effective_score,
            bonus_desc,
        )

    # score vs category cutoff
    if effective_score >= cutoff:
        return (
            "ADMITTED (Regular)",
            f"Meets {cat_display} cutoff ({effective_score:.0f} >= {cutoff}) "
            f"and GPA requirement ({gpa} >= {MIN_GPA})",
            effective_score,
            bonus_desc,
        )
    elif effective_score >= cutoff - 5:
        # within 5 of cutoff -> waitlist
        return (
            "WAITLISTED",
            f"Effective score {effective_score:.0f} is close to "
            f"{cat_display} cutoff of {cutoff} but does not meet it",
            effective_score,
            bonus_desc,
        )
    else:
        return (
            "REJECTED",
            f"Effective score {effective_score:.0f} does not meet "
            f"{cat_display} cutoff of {cutoff}",
            effective_score,
            bonus_desc,
        )


def print_result(entrance_score, gpa, has_rec, category, extra_score):
    """Print formatted admission decision."""
    result, reason, effective_score, bonus_desc = evaluate_admission(
        entrance_score, gpa, has_rec, category, extra_score
    )

    print("\n" + "=" * 50)
    print("ADMISSION DECISION".center(50))
    print("=" * 50)

    if bonus_desc != "none":
        print(f"  Bonus Applied   : {bonus_desc}")
    print(f"  Effective Score : {effective_score:.0f}")
    print("-" * 50)
    print(f"\n  Result  : {result}")
    print(f"  Reason  : {reason}")
    print("\n" + "=" * 50)


def main():
    """Run the student admission screening system."""
    print("\n===============================================")
    print("   UNIVERSITY ADMISSION SCREENING TOOL")
    print("   IIT Gandhinagar -- AI-ML PG Diploma")
    print("===============================================\n")

    entrance_score = get_entrance_score()
    gpa = get_gpa()
    has_rec = get_recommendation()
    category = get_category()
    extra_score = get_extracurricular()

    print_result(entrance_score, gpa, has_rec, category, extra_score)


if __name__ == "__main__":
    main()
