from django_markdown_converter.patterns.inlines.parser import convert_inline, revert_inline


MD = "***Markdown Example** with* but we could keep going and going *till there is another one* italizczed. "


converted = convert_inline(MD)

print(converted)