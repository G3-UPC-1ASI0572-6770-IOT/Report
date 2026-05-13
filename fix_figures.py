import re

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

# Pass 1: find all figure definitions.
# The definitions look like: **Figura \d+(?:\.\d+)***
# Let's extract them.
defs = re.findall(r"\*\*Figura\s+([0-9.]+)\*\*", text, flags=re.IGNORECASE)

# We want to assign them new sequential IDs in order. But what if one is defined twice? 
# Usually they appear once in the exact order.
mapping = {}
counter = 1
for old_num in defs:
    if old_num not in mapping:
        mapping[old_num] = str(counter)
        counter += 1

# Pass 2: Replace both definitions and references
# We must replace them carefully so we don't do partial replacements (e.g., replacing "1" in "10")
# We'll use a regex replacement with word boundary

def replacer(match):
    prefix = match.group(1)
    old_num = match.group(2)
    suffix = match.group(3)
    
    if old_num in mapping:
        return f"{prefix}{mapping[old_num]}{suffix}"
    return match.group(0)

# Replace instances of: Figura <number> 
# And handle optional bolding around it like **Figura 1**
new_text = re.sub(r"(?i)(Figura\s+)([0-9.]+)(\b|\*)", replacer, text)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_text)

print(f"Mapped {len(mapping)} unique figures. Rewrote README.md")
