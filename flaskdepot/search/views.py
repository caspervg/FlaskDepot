from flask import Blueprint, redirect, flash, current_app, render_template, request
from flaskdepot.file.models import File, BroadCategory, NarrowCategory
from flaskdepot.search.controllers import SearchForm
from flaskdepot.user.models import User, Usergroup
from flaskdepot.utils.helper import likeable, url_for

search = Blueprint("search", __name__)


@search.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    form.next.data = url_for('.index')
    form.author.choices = [(str(u.id), u.username) for u in
                            User.query
                                .join(Usergroup)
                                .filter(Usergroup.is_uploader)
                                .filter(User.group_id == Usergroup.id)
                                .all()]
    form.author.choices.insert(0, ('', 'Select'))
    form.broad_category.choices = [(str(c.id), c.name) for c in BroadCategory.query.all()]
    form.broad_category.choices.insert(0, ('', 'Select'))
    form.narrow_category.choices = [(str(c.id), c.name) for c in NarrowCategory.query.all()]
    form.narrow_category.choices.insert(0, ('', 'Select'))

    if form.validate_on_submit():
        _params = {
            'exclude_locked': form.exclude_locked.data
        }

        if len(form.keyword.data) > 0:
            _params['keyword'] = form.keyword.data
        if len(form.author.data) > 0:
            _params['author'] = form.author.data
        if len(form.broad_category.data) > 0:
            _params['broad_category'] = form.broad_category.data
        if len(form.narrow_category.data) > 0:
            _params['narrow_category'] = form.narrow_category.data

        return redirect(url_for('.result', _params=_params))

    return render_template('search/index.html', form=form, title="Search files")


@search.route('/result', methods=['GET'])
@search.route('/result/page-<int:page>', methods=['GET'])
def result(page=1):
    _keyword = request.form.get('keyword')
    _authors = request.form.get('authors')
    _broad_cats = request.form.get('broad_cats')
    _narrow_cats = request.form.get('narrow_cats')
    _exclude_locked = request.form.get('exclude_locked')

    files = File.query

    if _keyword and len(_keyword) > 0:
        _likeword = likeable(_keyword)
        files = files.filter((File.name.ilike(_likeword)) | (File.description.ilike(_likeword)))
    if _authors and len(_authors) > 0:
        files = files.filter(File.author_id.in_(_authors))
    if _broad_cats and len(_broad_cats) > 0:
        files = files.filter(File.broad_category_id.in_(_broad_cats))
    if _narrow_cats and len(_narrow_cats) > 0:
        files = files.filter(File.narrow_category_id.in_(_narrow_cats))
    if _exclude_locked:
        files = files.filter(not File.is_locked)

    if len(files.all()) == 0:
        flash('No results were found. Please adjust your parameters and try again')
        return redirect(url_for('.index'))
    else:
        files = files.paginate(page, current_app.config['RESULTS_PER_PAGE'], False)
        return render_template('search/search_result.html', results=files, title="Search results")
