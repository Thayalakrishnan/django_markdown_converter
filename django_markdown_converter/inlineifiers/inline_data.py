
TEMPLATE_HTML_EL = lambda tag, content: f'<{tag}>{content}</{tag}>'
TEMPLATE_HTML_EL_SPACED = lambda tag, content: f'<{tag}>{content}</{tag}> '

TEMPLATE_BOUNDARY = lambda tag, content: f'{tag}{content}{tag}'

# everything inbetween
R_CONTENT = r'(?P<content>.*?)'

# everything inbetween except whitespace
R_CONTENT_NO_WSPACE = r'(?P<content>\S+)'

# inline image
R_INLINE_IMAGE = r'(?P<alt>.*?)\]\((?P<src>.*?)'

# inline LINK
R_LINK = r'(?P<label>.*?)\]\((?P<url>.*?)'

# inline LINK
R_EMAIL = r'(?P<email>\S+@\S+)'




CASES_LIST = [
    {
        "boundary": ("<", R_EMAIL, ">"), 
        "tag": "a", 
        "template": lambda tag, email: f'<{tag} href="mailto:{email}">{email}</{tag}>'
    },
    {
        "boundary": ("<https", R_CONTENT_NO_WSPACE, ">"), 
        "tag": "a", 
        "template": lambda tag, link: f'<{tag} href="{link}">{link}</{tag}>'
    },
    {
        "boundary": ("**", R_CONTENT, "**"), 
        "tag": "strong", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("__", R_CONTENT, "__"), 
        "tag": "strong", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("~~", R_CONTENT, "~~"), 
        "tag": "del", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("--", R_CONTENT, "--"), 
        "tag": "del", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("==", R_CONTENT, "=="), 
        "tag": "mark", 
        "template": TEMPLATE_HTML_EL
    }, # ensure taht we can math and code before this
    {
        "boundary": ("``", R_CONTENT, "``"), 
        "tag": "code", 
        "template": TEMPLATE_HTML_EL
    }, # no multiline or whitespace between
    #{
    #    "boundary": (":", R_CONTENT_NO_WSPACE, ":"), 
    #    "tag": "emoji", 
    #    "template": TEMPLATE_HTML_EL
    #}, # no whitespace between
    {
        "boundary": ("`", R_CONTENT, "`"), 
        "tag": "code", 
        "template": TEMPLATE_HTML_EL
    }, # no multiline or whitespace between
    {
        "boundary": ("*", R_CONTENT, "*"), 
        "tag": "em", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("_", R_CONTENT, "_"), 
        "tag": "em", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("![", R_INLINE_IMAGE, ")"), 
        "tag": "img", 
        "template": lambda tag, alt, src: f'<{tag} src="{src}" alt="{alt}"/>'
    },
    {
        "boundary": ("[^", R_CONTENT_NO_WSPACE, "]"), 
        "tag": "a", 
        "template": lambda tag, content: f'<sup id="fnref:footnote{content}"><{tag} class="footnote-ref" href="#fn:footnote{content}">{content}</{tag}></sup>'
    },
    {
        "boundary": ("[", R_LINK,")"), 
        "tag": "a", 
        "template": lambda tag, label, url: f'<{tag} href="{url}" title="external link to {label}">{label}</{tag}>'
    },
    {
        "boundary": ("^", R_CONTENT_NO_WSPACE, "^"), 
        "tag": "sup", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("~", R_CONTENT_NO_WSPACE, "~"), 
        "tag": "sub", 
        "template": TEMPLATE_HTML_EL
    },
    {
        "boundary": ("\<em>", R_CONTENT, "\</em>"), 
        "tag": "*", 
        "template": TEMPLATE_BOUNDARY
    },
    #{"boundary": ("$", R_CONTENT, "$"), "tag": "math", "swap": ("math", "math"), "whitespace": True, "html": True, "handler": False, "template": TEMPLATE_HTML_EL},
]