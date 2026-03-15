import os
import re
from config import TEMPLATE_DIR


def render_template(template_name, context=None):
    """
    Simple template engine:
    - {{variable}} -> replaced with context value
    - {%include filename%} -> includes another template file
    """
    if context is None:
        context = {}

    template_path = os.path.join(TEMPLATE_DIR, template_name)
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Handle includes: {%include partials/navbar.html%}
    def replace_include(match):
        include_file = match.group(1).strip()
        include_path = os.path.join(TEMPLATE_DIR, include_file)
        if os.path.exists(include_path):
            with open(include_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ''

    html = re.sub(r'\{%\s*include\s+(.+?)\s*%\}', replace_include, html)

    # Build nav auth links based on is_authenticated
    if context.get('is_authenticated'):
        context['nav_auth_links'] = f'''
        <li class="nav-item"><a class="nav-link" href="/accounts/dashboard">
          <i class="fas fa-user"></i> Welcome {context.get("first_name", context.get("username", ""))}</a></li>
        <li class="nav-item"><a class="nav-link" href="/accounts/logout">
          <i class="fas fa-sign-out-alt"></i> Logout</a></li>'''
    else:
        context['nav_auth_links'] = '''
        <li class="nav-item"><a class="nav-link" href="/accounts/register">
          <i class="fas fa-user-plus"></i> Register</a></li>
        <li class="nav-item"><a class="nav-link" href="/accounts/login">
          <i class="fas fa-sign-in-alt"></i> Login</a></li>'''

    # Replace variables: {{variable}}
    def replace_var(match):
        var_name = match.group(1).strip()
        value = context.get(var_name, '')
        if value is None:
            return ''
        return str(value)

    html = re.sub(r'\{\{(.+?)\}\}', replace_var, html)

    return html


def format_price(price):
    """Format price with commas: 1500000 -> 15,00,000 (Indian) or 1,500,000"""
    try:
        return f"{int(price):,}"
    except (ValueError, TypeError):
        return str(price)


def build_options_html(options, selected=''):
    """Build HTML <option> tags from a list."""
    html = ''
    for opt in options:
        sel = ' selected' if str(opt) == str(selected) else ''
        html += f'<option value="{opt}"{sel}>{opt}</option>\n'
    return html


def build_pagination_html(current_page, total_pages, base_url):
    """Build pagination HTML."""
    if total_pages <= 1:
        return ''

    html = '<nav><ul class="pagination">'

    # Previous
    if current_page > 1:
        html += f'<li class="page-item"><a class="page-link" href="{base_url}?page={current_page - 1}">&laquo;</a></li>'
    else:
        html += '<li class="page-item disabled"><span class="page-link">&laquo;</span></li>'

    # Page numbers
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += f'<li class="page-item active"><span class="page-link">{i}</span></li>'
        else:
            html += f'<li class="page-item"><a class="page-link" href="{base_url}?page={i}">{i}</a></li>'

    # Next
    if current_page < total_pages:
        html += f'<li class="page-item"><a class="page-link" href="{base_url}?page={current_page + 1}">&raquo;</a></li>'
    else:
        html += '<li class="page-item disabled"><span class="page-link">&raquo;</span></li>'

    html += '</ul></nav>'
    return html
