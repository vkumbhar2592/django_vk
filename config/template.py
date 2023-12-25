# Template Settings
# ------------------------------------------------------------------------------


# Theme layout templates directory
# ! Don't change unless it's required
THEME_LAYOUT_DIR = "layout"

# Template config
# ? Easily change the template configuration from here
# ? Replace this object with template-config/demo-*.py file's TEMPLATE_CONFIG to change the template configuration as per our demos
TEMPLATE_CONFIG = {
    "layout": "vertical",             # Options[String]: vertical(default), horizontal
    "theme": "theme-default",         # Options[String]: theme-default(default), theme-bordered, theme-semi-dark
    "style": "light",                 # Options[String]: light(default), dark, system mode
    "rtl_support": False,              # options[Boolean]: True(default), False # To provide RTLSupport or not
    "rtl_mode": False,                # options[Boolean]: False(default), True # To set layout to RTL layout  (myRTLSupport must be True for rtl mode)
    "has_customizer": False,           # options[Boolean]: True(default), False # Display customizer or not THIS WILL REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WON'T WORK
    "display_customizer": False,       # options[Boolean]: True(default), False # Display customizer UI or not, THIS WON'T REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WILL WORK
    "content_layout": "wide",      # options[String]: 'compact', 'wide' (compact=container-xxl, wide=container-fluid)
    "navbar_type": "fixed",           # options[String]: 'fixed', 'static', 'hidden' (Only for vertical Layout)
    "header_type": "static",           # options[String]: 'static', 'fixed' (for horizontal layout only)
    "menu_fixed": True,               # options[Boolean]: True(default), False # Layout(menu) Fixed (Only for vertical Layout)
    "menu_collapsed": True,          # options[Boolean]: False(default), True # Show menu collapsed, Only for vertical Layout
    "footer_fixed": True,            # options[Boolean]: False(default), True # Footer Fixed
    "show_dropdown_onhover": True,    # True, False (for horizontal layout only)
    "customizer_controls": False,  # To show/hide customizer options
}

# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
THEME_VARIABLES = {
    "creator_name": "Yahoo HR Team",
    "creator_url": "https://www.yahoo.com",
    "template_name": "HR",
    "template_suffix": "Sheldon Agent Admin",
    "template_version": "1.0.0",
    "template_free": False,
    "template_description": "Our first release of what would be the ultimate HR AI assistant.",
    "template_keyword": "Yahoo, HR. AI, Assistant, Chatbot, Sheldon",
    "facebook_url": "https://www.facebook.com/ThemeSelections/",
    "twitter_url": "https://twitter.com/Theme_Selection",
    "github_url": "https://github.com/themeselection",
    "dribbble_url": "https://dribbble.com/themeselection",
    "instagram_url": "https://www.instagram.com/themeselection/",
    "license_url": "https://themeselection.com/license/",
    "live_preview": "https://demos.themeselection.com/sneat-bootstrap-html-django-admin-template/html/vertical-menu-template/",
    "product_page": "https://themeselection.com/item/sneat-bootstrap-django-admin-template/",
    "support": "https://themeselection.com/support/",
    "more_themes": "https://themeselection.com/",
    "documentation": "https://demos.themeselection.com/sneat-bootstrap-html-admin-template/documentation/django-introduction.html",
    "changelog": "https://demos.themeselection.com/sneat-bootstrap-html-django-admin-template/changelog.html",
    "git_repository": "https://github.com/themeselection/sneat-bootstrap-html-django-admin-template",
    "git_repo_access": "https://tools.themeselection.com/github/github-access",
}
