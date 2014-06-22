from wtforms import TextField, BooleanField, SelectField
from flaskdepot.base.controllers import RedirectForm


class SearchForm(RedirectForm):
    keyword = TextField('Keyword')
    author = SelectField('File author', default=[])
    broad_category = SelectField('Broad category', default=[])
    narrow_category = SelectField('Narrow category', default=[])
    exclude_locked = BooleanField('Exclude locked files', default=True)
