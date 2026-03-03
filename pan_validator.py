"""
PAN Card Validator - Part D (AI-Augmented Task)
Day 8 AM | IIT Gandhinagar PG Diploma AI-ML

PAN Format: 5 uppercase letters, 4 digits, 1 uppercase letter
Example: ABCDE1234F  The 4th character = taxpayer type.

--- PART D DOCUMENTATION ---
Prompt used:
"Write a Python program that validates an Indian PAN card number format
using if-else conditions. PAN format: 5 uppercase letters, 4 digits,
1 uppercase letter (e.g., ABCDE1234F). The 4th character indicates the
type of taxpayer."

AI evaluation (what it got right / wrong):
Right: basic length check, letter/digit position checks, uppercase check
Wrong: did not validate the 4th character against known taxpayer codes,
       used regex which the assignment asked to avoid with if-else,
       no meaningful error messages telling user which position failed,
       did not strip whitespace before checking (edge case),
       no interactive loop for multiple inputs.
This version fixes all of the above.
"""

TAXPAYER_TYPES = {
    "P": "Individual (Person)",
    "C": "Company",
    "H": "Hindu Undivided Family",
    "F": "Firm / Partnership",
    "A": "Association of Persons",
    "T": "Trust",
    "B": "Body of Individuals",
    "L": "Local Authority",
    "J": "Artificial Juridical Person",
    "G": "Government Entity",
}


def validate_pan(pan):
    """Check PAN number character by character. Returns (bool, message)."""
    if not pan:
        return False, "PAN cannot be empty"

    pan = pan.strip().upper()

    if len(pan) != 10:
        return False, "Must be exactly 10 characters (got {})".format(len(pan))

    # Positions 1-3: any uppercase letter
    for i in range(3):
        if not pan[i].isalpha():
            return False, "Position {} must be a letter, got '{}'".format(i + 1, pan[i])

    # Position 4: letter AND must be a known taxpayer type
    if not pan[3].isalpha():
        return False, "Position 4 must be a letter (taxpayer type), got '{}'".format(pan[3])
    if pan[3] not in TAXPAYER_TYPES:
        return False, "Position 4 '{}' is not a valid taxpayer type code".format(pan[3])

    # Position 5: letter (first letter of name/surname)
    if not pan[4].isalpha():
        return False, "Position 5 must be a letter, got '{}'".format(pan[4])

    # Positions 6-9: digits
    for i in range(5, 9):
        if not pan[i].isdigit():
            return False, "Position {} must be a digit, got '{}'".format(i + 1, pan[i])

    # Position 10: letter (check character)
    if not pan[9].isalpha():
        return False, "Position 10 must be a letter, got '{}'".format(pan[9])

    return True, "Valid PAN | Taxpayer Type: " + TAXPAYER_TYPES[pan[3]]


def main():
    print("")
    print("=" * 48)
    print("       INDIAN PAN CARD VALIDATOR")
    print("  Format: AAAAA9999A  (5L + 4D + 1L)")
    print("=" * 48)

    while True:
        pan_input = input("\nEnter PAN (or q to quit): ").strip()
        if pan_input.lower() == "q":
            break
        valid, msg = validate_pan(pan_input)
        tag = "VALID  " if valid else "INVALID"
        print("  [{}] {}".format(tag, msg))

    print("Exiting.")


if __name__ == "__main__":
    main()
