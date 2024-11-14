
import re

# Sample HTML content
html_content = '''
<html>
<body>
    <img src="image1.jpg" alt="First image">
    <p>Some text here.</p>
    <img src="image2.png" alt="Second image">
</body>
</html>
'''

# Regex pattern to find <img> tags with src attributes
pattern = r'(<img\s[^>]*src=)"[^"]*"'

# Replace with an empty src attribute
updated_html = re.sub(pattern, r'\1""', html_content)

print(updated_html)
