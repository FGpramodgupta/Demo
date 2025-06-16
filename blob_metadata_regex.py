"""

| Type               | Examples                                                                                                   |                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Letters**        | A–Z, a–z                                                                                                   |                                                          |
| **Digits**         | 0–9                                                                                                        |                                                          |
| **Spaces**         | `' '` (normal space)                                                                                       |                                                          |
| **Common Symbols** | `~`, `` ` ``, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `-`, `+`, `=`, `{`, `}`, `[`, `]`, \` | `, `\`, `:`, `;`, `"`, `'`, `<`, `>`, `,`, `.`, `?`, `/` |

Not allowed:

| Type                      | Examples                           | Reason              |
| ------------------------- | ---------------------------------- | ------------------- |
| **Long Hyphen**           | `—` (em dash, Unicode `\u2014`)    | Not in allowed list |
| **Other Unicode Dashes**  | `–`, `‒`, `−` etc.                 | Safer to exclude    |
| **Emojis & Icons**        | 😃, 🎉, 🧠, etc.                   | Non-ASCII Unicode   |
| **Language Symbols**      | `ç`, `ñ`, `ü`, `€`, `₹`, `©`, etc. | Not standard ASCII  |
| **Chinese/Japanese etc.** | 漢字, カタカナ, 한글                       | Not ASCII           |


"""


import re

def clean_metadata_value(value):
    # Regex to find all characters NOT in allowed set
    # Allowed: letters, digits, space, common ASCII special characters
    disallowed_chars = r"[^\w\s~`!@#$%^&*()_\-+={}\[\]|\\:;\"'<>,.?/]"
    
    # Replace each disallowed character with a space
    return re.sub(disallowed_chars, ' ', value)

import re

def clean_metadata_value(value):
    # Step 1: Replace all dash-like characters with a standard hyphen
    value = re.sub(r"[\u2012\u2013\u2014\u2015\u2212]", "-", value)

    # Step 2: Remove everything that's NOT in the allowed character set
    allowed_pattern = r"[^A-Za-z0-9\s~`!@#$%^&*()_\-+={}\[\]|\\:;\"'<>,.?/]"
    value = re.sub(allowed_pattern, '', value)

    return value


text = "Valid@Text—but—this—em—dash—is—not—allowed 😎"
cleaned = clean_metadata_value(text)
print(cleaned)
# Output: "Valid@Text but this em dash is not allowed  "
