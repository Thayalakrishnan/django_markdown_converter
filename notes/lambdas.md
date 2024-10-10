lambda_extractor = lambda pat: lambda x: x[len(pat[0]):len(pat[1])*(-1)]
lambda_formatter = lambda pat: lambda x: f"{pat[0]}{x}{pat[1]}"

# pat: pattern <tuple>
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})" 
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>

# processing content
get_text_captured = lambda cur, content: content[cur[0]:cur[1]]
get_text_between = lambda pre, cur, content: content[pre[1]:cur[0]]
get_text_after = lambda cur, content: content[cur[1]::]
create_text_object = lambda content: {"type": "text", "data": content}
create_markup_object = lambda name, content, lookup: {"type": name, "data": lookup[name](content)}


#for _ in filter(lambda x: isinstance(x["data"], str), mybank):


## functions
self.extract = lambda x: x[len(left):len(right)*(-1)]
self.format = lambda x: f"{left}{x}{right}"
        
        
single_pattern = lambda pat: f"({re.escape(pat[0])}.+?{re.escape(pat[1])})" # pat: pattern <tuple>
join_patterns = lambda pats: "|".join(pats) # pats: patterns <list>
label_pattern = lambda label, pats: f"(?P<{label}>{pats})" # label: label <string>, pat: pattern <tuple>
generate_pattern = lambda label, pats: label_pattern(label, join_patterns(map(single_pattern, pats))) # label: label <string>, pats: patterns <list>
