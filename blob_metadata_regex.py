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

text = "Valid@Text—but—this—em—dash—is—not—allowed 😎"
cleaned = clean_metadata_value(text)
print(cleaned)
# Output: "Valid@Text but this em dash is not allowed  "
