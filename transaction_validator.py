"""
Smart Transaction Validator - Fraud Detection Rule Engine
Day 8 AM Part E Bonus | IIT Gandhinagar PG Diploma AI-ML
"""

SINGLE_LIMIT = 50000
DAILY_LIMIT = 100000
CATEGORY_LIMITS = {
    "food": 5000,
    "electronics": 30000,
    "travel": None,
    "other": None,
}


def get_limits(is_vip):
    """Return limits, doubled if VIP customer."""
    m = 2 if is_vip else 1
    single = SINGLE_LIMIT * m
    daily = DAILY_LIMIT * m
    cat = {k: (v * m if v else None) for k, v in CATEGORY_LIMITS.items()}
    return single, daily, cat


def validate_transaction(amount, category, hour, daily_spent, is_vip=False):
    """Run rule engine. Returns (decision, reason)."""
    single_limit, daily_limit, cat_limits = get_limits(is_vip)

    # BLOCK rules come first - they override everything
    if amount > single_limit:
        return "BLOCKED", "Exceeds single transaction limit of Rs {:,.0f}".format(single_limit)

    if daily_spent + amount > daily_limit:
        return "BLOCKED", "Would exceed daily limit of Rs {:,.0f} (spent so far: Rs {:,.0f})".format(
            daily_limit, daily_spent
        )

    # FLAG rules
    flags = []

    if hour < 6 or hour >= 23:
        flags.append("unusual hour ({:02d}:00 - outside 06:00 to 23:00)".format(hour))

    cat_limit = cat_limits.get(category)
    if cat_limit is not None and amount >= cat_limit:
        flags.append("{} amount Rs {:,.0f} >= category limit Rs {:,.0f}".format(
            category, amount, cat_limit
        ))

    if flags:
        return "FLAGGED", " | ".join(flags)

    return "APPROVED", "All checks passed"


def get_validated_float(prompt, min_val=0, allow_zero=False):
    """Prompt for a float with basic validation."""
    while True:
        try:
            val = float(input(prompt))
            if allow_zero and val < 0:
                print("  Cannot be negative.")
                continue
            elif not allow_zero and val <= min_val:
                print("  Must be greater than {}.".format(min_val))
                continue
            return val
        except ValueError:
            print("  Enter a valid number.")


def main():
    print("")
    print("=" * 52)
    print("   SMART TRANSACTION VALIDATOR")
    print("   Rule-based Fraud Detection Engine")
    print("=" * 52)

    amount = get_validated_float("Transaction amount (Rs): ")

    while True:
        category = input("Category (food/travel/electronics/other): ").strip().lower()
        if category in CATEGORY_LIMITS:
            break
        print("  Enter: food, travel, electronics, or other.")

    while True:
        try:
            hour = int(input("Hour of transaction (0-23): "))
            if 0 <= hour <= 23:
                break
            print("  Must be 0-23.")
        except ValueError:
            print("  Enter a whole number.")

    daily_spent = get_validated_float("Amount already spent today (Rs): ", allow_zero=True)

    while True:
        vip = input("VIP customer? (yes/no): ").strip().lower()
        if vip in ("yes", "no"):
            is_vip = vip == "yes"
            break
        print("  Enter yes or no.")

    if is_vip:
        print("  [VIP] All limits are doubled for this customer.")

    decision, reason = validate_transaction(amount, category, hour, daily_spent, is_vip)

    print("")
    print("  Transaction : Rs {:,.0f} | {} | {:02d}:00".format(amount, category, hour))
    print("  Decision    : {}".format(decision))
    print("  Reason      : {}".format(reason))
    print("=" * 52)


if __name__ == "__main__":
    main()
