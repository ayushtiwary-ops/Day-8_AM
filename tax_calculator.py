"""
Indian Income Tax Calculator - New Regime FY 2024-25
Day 8 AM - Part B Stretch Problem
"""

STANDARD_DEDUCTION = 75000

TAX_SLABS = [
    (300000,  0.00),
    (700000,  0.05),
    (1000000, 0.10),
    (1200000, 0.15),
    (1500000, 0.20),
    (None,    0.30),
]

SLAB_LABELS = ["0 to 3L", "3L to 7L", "7L to 10L", "10L to 12L", "12L to 15L", "Above 15L"]


def format_inr(amount):
    amount = round(amount, 2)
    s = f"{amount:.2f}"
    rupees, paise = s.split(".")
    is_neg = rupees.startswith("-")
    if is_neg:
        rupees = rupees[1:]
    if len(rupees) <= 3:
        formatted = rupees
    else:
        last_three = rupees[-3:]
        rest = rupees[:-3]
        groups = []
        while rest:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        formatted = ",".join(groups) + "," + last_three
    result = f"Rs {formatted}.{paise}"
    return f"-{result}" if is_neg else result


def calculate_tax(taxable_income):
    breakdown = []
    total_tax = 0
    prev = 0
    remaining = taxable_income
    for i, (limit, rate) in enumerate(TAX_SLABS):
        if remaining <= 0:
            break
        slab_size = remaining if limit is None else min(remaining, limit - prev)
        tax_here = slab_size * rate
        total_tax += tax_here
        if slab_size > 0:
            breakdown.append((SLAB_LABELS[i], slab_size, rate * 100, tax_here))
        remaining -= slab_size
        if limit is not None:
            prev = limit
    return breakdown, total_tax


def main():
    print("")
    print("=" * 55)
    print("   INCOME TAX CALCULATOR - New Regime FY 2024-25")
    print("=" * 55)
    while True:
        try:
            gross = float(input("Annual Gross Income (Rs): "))
            if gross < 0:
                print("  Income cannot be negative.")
                continue
            break
        except ValueError:
            print("  Enter a valid number.")
    taxable = max(0, gross - STANDARD_DEDUCTION)
    print("")
    print("  Gross Income       : " + format_inr(gross))
    print("  Standard Deduction : " + format_inr(STANDARD_DEDUCTION))
    print("  Taxable Income     : " + format_inr(taxable))
    breakdown, total_tax = calculate_tax(taxable)
    print("")
    print("-" * 55)
    print("  {:<14} {:>15} {:>6} {:>13}".format("Slab", "Income in Slab", "Rate", "Tax"))
    print("-" * 55)
    for label, income, rate, tax in breakdown:
        print("  {:<14} {:>15} {:>5.0f}% {:>13}".format(label, format_inr(income), rate, format_inr(tax)))
    print("-" * 55)
    print("  Total Tax          : " + format_inr(total_tax))
    if gross > 0:
        eff = (total_tax / gross) * 100
        print("  Effective Rate     : " + "{:.2f}%".format(eff))
    if taxable <= 700000:
        print("")
        print("  Rebate u/s 87A: No tax if taxable income <= Rs 7L")
    print("=" * 55)


if __name__ == "__main__":
    main()
