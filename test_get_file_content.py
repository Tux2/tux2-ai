from config import MAX_CHARS
from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
length = len(result)
print(f"Lorem.txt length total: {len(result)}")
ends_with = result.endswith(f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]')
print(f"Lorem.txt is longer: {ends_with}")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))