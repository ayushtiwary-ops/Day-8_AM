# Day 8 AM — Conditionals and Control Flow

**IIT Gandhinagar | PG Diploma in AI-ML & Agentic AI Engineering**
Day 8 AM Take-Home Assignment | Due: 06/03/2026 07:15 PM

---

## Files

| File | Part | Description |
|---|---|---|
| `admission_system.py` | A | Student admission decision system |
| `tax_calculator.py` | B | Indian income tax calculator — New Regime FY 2024-25 |
| `pan_validator.py` | D | PAN card validator — AI-generated, critiqued & improved |
| `transaction_validator.py` | E | Smart transaction fraud detection rule engine |

Part C interview answers are in this README below.

---

## How to Run

```bash
python admission_system.py        # Part A
python tax_calculator.py          # Part B
python pan_validator.py           # Part D
python transaction_validator.py   # Part E
```

No external packages needed — standard library only.

---

## Part C — Interview Ready

### Q1: elif vs multiple if

The key difference is simple: `elif` is a chain — once one condition is true, Python skips everything else in that chain. Multiple `if` statements are completely independent — every single one gets evaluated regardless of what happened before.

Here's an example where they give different output:

```python
x = 10

# Multiple if — each condition is evaluated separately
if x > 5:
    x = x + 1      # runs → x becomes 11
if x > 10:
    x = x + 1      # ALSO runs because x is now 11 and 11 > 10
print(x)           # Output: 12

# elif — chain exits after first match
x = 10
if x > 5:
    x = x + 1      # runs → x becomes 11
elif x > 10:
    x = x + 1      # never reached — Python already entered the first branch
print(x)           # Output: 11
```

**Input:** `x = 10`
**Output with multiple if:** `12`
**Output with elif:** `11`

**Why the difference happens:** With multiple `if`, the second check (`x > 10`) is evaluated *after* `x` was already changed to 11 by the first block. So it passes. With `elif`, Python exits the entire chain once the first condition is true — the second condition is never even looked at.

The rule of thumb: use `elif` when choices are mutually exclusive (grading, categories, decision trees). Use separate `if` statements only when you genuinely want multiple independent checks to run on the same input.

---

### Q2: classify_triangle()

```python
def classify_triangle(a, b, c):
    """Classify a triangle given three side lengths.

    Returns:
        str: Classification or reason for invalidity.
    """
    # reject zero or negative sides first
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle (sides must be positive)"

    # triangle inequality — sum of any two sides must exceed the third
    if a >= b + c or b >= a + c or c >= a + b:
        return "Not a triangle (violates triangle inequality)"

    if a == b == c:
        return "Equilateral"
    elif a == b or b == c or a == c:
        return "Isosceles"
    else:
        return "Scalene"
```

Test cases:

```python
classify_triangle(0, 5, 5)    # "Not a triangle (sides must be positive)"
classify_triangle(-1, 3, 4)   # "Not a triangle (sides must be positive)"
classify_triangle(1, 2, 10)   # "Not a triangle (violates triangle inequality)"
classify_triangle(1, 2, 3)    # "Not a triangle (violates triangle inequality)" — 3 >= 1+2
classify_triangle(5, 5, 5)    # "Equilateral"
classify_triangle(5, 5, 8)    # "Isosceles"
classify_triangle(3, 4, 5)    # "Scalene"
```

Edge case worth noting: `(1, 2, 3)` is NOT a valid triangle even though it looks close — 3 ≥ 1 + 2, which means it's a degenerate triangle (a straight line).

---

### Q3: Debug — What is wrong with this grading code?

```python
# Buggy code
score = 85

if score >= 60:
    grade = 'D'
if score >= 70:
    grade = 'C'
if score >= 80:
    grade = 'B'
if score >= 90:
    grade = 'A'

print(grade)  # prints 'B' — should print 'B', but for score=95 it would print 'A' correctly
              # for score=85 specifically it prints 'B' which happens to be right
              # but the logic is still broken — for score=65 it would print 'C' not 'D'
```

**The bug:** Every `if` is independent. For `score = 85`:
- `85 >= 60` → True → `grade = 'D'`
- `85 >= 70` → True → `grade = 'C'` (overwrites D)
- `85 >= 80` → True → `grade = 'B'` (overwrites C)
- `85 >= 90` → False → grade stays 'B'

So for 85 the output *happens* to be 'B' — which looks correct — but the code is overwriting grade multiple times. For `score = 65`, it would set grade to 'D' then immediately overwrite it with 'C' (since 65 >= 70 is False but 65 >= 60 is True and then we fall through with grade = 'D' set... actually wait:

- `65 >= 60` → True → `grade = 'D'`
- `65 >= 70` → False → no change
- `65 >= 80` → False → no change
- `65 >= 90` → False → no change

So 65 gives 'D' which is... correct by accident. The real breakage is for `score = 75`:
- `75 >= 60` → True → `grade = 'D'`
- `75 >= 70` → True → `grade = 'C'` ← final answer is 'C', but should be 'C'... hmm.

Actually the most obvious breakage: for any score ≥ 90, it goes through D → C → B → A correctly. But the *bug* is semantic — the grades are assigned in overwriting order from lowest to highest, so it only works because the slabs are checked in ascending order. It will break the moment someone reorders them or adds a new slab in the middle.

**The correct fix:**

```python
score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(grade)  # 'B' — correct, and the logic is now clean and order-independent
```

With `elif`, once Python finds the right bracket, it stops. The code is now safe to reorder, extend, or maintain.

---

## Part D — AI-Augmented Task: PAN Validator

**Exact prompt used:**
> "Write a Python program that validates an Indian PAN card number format using if-else conditions. PAN format: 5 uppercase letters, 4 digits, 1 uppercase letter (e.g., ABCDE1234F). The 4th character indicates the type of taxpayer."

**What the AI got right:**
- Basic length check (10 characters)
- Positions 1–3 are letters, positions 6–9 are digits, position 10 is a letter
- Converted to uppercase before checking

**What the AI got wrong / missed:**
- Used regex instead of if-else (assignment explicitly asked for if-else)
- Did not validate the 4th character against the known set of taxpayer type codes (P, C, H, F, A, T, B, L, J, G)
- Generic error message — didn't tell you *which* position failed
- Didn't strip whitespace from input (common edge case)
- No loop for testing multiple PANs

**My improved version** (`pan_validator.py`) fixes all of this — character-by-character validation with position-specific error messages, validated taxpayer type lookup, whitespace handling, and an interactive loop.

---

## Part E — Smart Transaction Validator

See `transaction_validator.py`. Implements:
- BLOCK if amount > ₹50,000 or daily total would exceed ₹1,00,000
- FLAG for transactions before 6 AM or after 11 PM
- FLAG for category limit violations (food < ₹5,000, electronics < ₹30,000)
- VIP mode doubles all limits, implemented with ternary-style multiplier

---

### Q2: classify_triangle()

```python
def classify_triangle(a, b, c):
    """Classify a triangle given three side lengths.

    Returns:
        str: Type of triangle or reason it is invalid.
    """
    # reject non-positive sides before anything else
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle -- sides must be positive"

    # triangle inequality (strict) -- any side must be less than sum of other two
    if a >= b + c or b >= a + c or c >= a + b:
        return "Not a triangle -- violates triangle inequality"

    if a == b == c:
        return "Equilateral"
    elif a == b or b == c or a == c:
        return "Isosceles"
    else:
        return "Scalene"
```

Test cases:
- classify_triangle(5, 5, 5)  -> Equilateral
- classify_triangle(5, 5, 3)  -> Isosceles
- classify_triangle(3, 4, 5)  -> Scalene
- classify_triangle(1, 2, 3)  -> Not a triangle (1 + 2 = 3, fails strict inequality)
- classify_triangle(0, 4, 5)  -> Not a triangle -- sides must be positive
- classify_triangle(-1, 4, 5) -> Not a triangle -- sides must be positive

---

### Q3: Debug the grade code

```python
# BUGGY CODE
score = 85

if score >= 60:
    grade = 'D'
if score >= 70:
    grade = 'C'
if score >= 80:
    grade = 'B'
if score >= 90:
    grade = 'A'

print(grade)
```

**Bug:** All four are independent `if` statements, not an `elif` chain.

**Why it's wrong:** For score = 85, all three conditions (>= 60, >= 70, >= 80) are True,
so `grade` gets overwritten three times: D -> C -> B. The final value is B, which happens
to be correct for 85 -- but only by accident. The logic is fundamentally broken. For
score = 65, it would print C (overwritten from D by the >= 70 check... wait, 65 < 70,
so it prints D -- but you get the idea. Any score in a higher band would clobber lower ones).

The real problem shows up at score = 95: grade gets set D, C, B, A -- prints A.
Correct but for the wrong reason. The code has no concept of exclusive ranges.

**Correct fix:**

```python
score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(grade)  # B
```

Two things changed: (1) `elif` instead of `if`, and (2) order flipped to check highest
threshold first -- otherwise `>= 60` would always match before we got to A, B, or C.

---

## Part D -- AI Usage Notes

Prompt used:
> "Write a Python program that validates an Indian PAN card number format using if-else
> conditions. PAN format: 5 uppercase letters, 4 digits, 1 uppercase letter.
> The 4th character indicates the type of taxpayer."

What the AI got right: basic length check, letter/digit position validation, uppercase check.

What it missed or got wrong:
- Used regex, but the assignment specifically asks for if-else conditions
- Did not validate position 4 against known taxpayer type codes (P, C, H, F, A, T, etc.)
- Error messages were generic -- no indication of which position failed
- Did not strip whitespace before validating (easy edge case to miss)
- No loop for testing multiple inputs

The improved version in pan_validator.py addresses all of these -- position-specific
error messages, taxpayer type dictionary, whitespace handling, and a clean input loop.

---

## Git Commit

```bash
git add .
git commit -m "Day 8 AM: conditionals, admission system, tax calculator, fraud detection"
git push origin main
```
