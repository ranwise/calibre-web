# -*- coding: utf-8 -*-

#  This file is part of the Calibre-Web (https://github.com/janeczku/calibre-web)
#    Copyright (C) 2018-2020 OzzieIsaacs
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from flask import render_template, g, abort, request
from flask_babel import gettext as _
from werkzeug.local import LocalProxy
from flask_login import current_user

from . import config, constants, logger
from .ub import User

log = logger.create()


def get_sidebar_config(kwargs=None):
    kwargs = kwargs or []
    simple = bool(
        [
            e
            for e in ["kindle", "tolino", "kobo", "bookeen"]
            if (e in request.headers.get("User-Agent", "").lower())
        ]
    )
    if "content" in kwargs:
        content = kwargs["content"]
        content = (
            isinstance(content, (User, LocalProxy)) and not content.role_anonymous()
        )
    else:
        content = "conf" in kwargs
    sidebar = []
    sidebar.append(
        {
            "glyph": "bi-book",
            "text": _("Books"),
            "link": "web.index",
            "id": "new",
            "visibility": constants.SIDEBAR_RECENT,
            "public": True,
            "page": "root",
            "show_text": _("Show recent books"),
            "config_show": False,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-fire",
            "text": _("Hot Books"),
            "link": "web.books_list",
            "id": "hot",
            "visibility": constants.SIDEBAR_HOT,
            "public": True,
            "page": "hot",
            "show_text": _("Show Hot Books"),
            "config_show": True,
        }
    )
    if current_user.role_admin():
        sidebar.append(
            {
                "glyph": "bi-download",
                "text": _("Downloaded Books"),
                "link": "web.download_list",
                "id": "download",
                "visibility": constants.SIDEBAR_DOWNLOAD,
                "public": (not g.user.is_anonymous),
                "page": "download",
                "show_text": _("Show Downloaded Books"),
                "config_show": content,
            }
        )
    else:
        sidebar.append(
            {
                "glyph": "bi-download",
                "text": _("Downloaded Books"),
                "link": "web.books_list",
                "id": "download",
                "visibility": constants.SIDEBAR_DOWNLOAD,
                "public": (not g.user.is_anonymous),
                "page": "download",
                "show_text": _("Show Downloaded Books"),
                "config_show": content,
            }
        )
    sidebar.append(
        {
            "glyph": "bi-star-fill",
            "text": _("Top Rated Books"),
            "link": "web.books_list",
            "id": "rated",
            "visibility": constants.SIDEBAR_BEST_RATED,
            "public": True,
            "page": "rated",
            "show_text": _("Show Top Rated Books"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-eye-fill",
            "text": _("Read Books"),
            "link": "web.books_list",
            "id": "read",
            "visibility": constants.SIDEBAR_READ_AND_UNREAD,
            "public": (not g.user.is_anonymous),
            "page": "read",
            "show_text": _("Show read and unread"),
            "config_show": content,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-eye-slash-fill",
            "text": _("Unread Books"),
            "link": "web.books_list",
            "id": "unread",
            "visibility": constants.SIDEBAR_READ_AND_UNREAD,
            "public": (not g.user.is_anonymous),
            "page": "unread",
            "show_text": _("Show unread"),
            "config_show": False,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-shuffle",
            "text": _("Discover"),
            "link": "web.books_list",
            "id": "rand",
            "visibility": constants.SIDEBAR_RANDOM,
            "public": True,
            "page": "discover",
            "show_text": _("Show Random Books"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-inbox-fill",
            "text": _("Categories"),
            "link": "web.category_list",
            "id": "cat",
            "visibility": constants.SIDEBAR_CATEGORY,
            "public": True,
            "page": "category",
            "show_text": _("Show category selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-bookmark-fill",
            "text": _("Series"),
            "link": "web.series_list",
            "id": "serie",
            "visibility": constants.SIDEBAR_SERIES,
            "public": True,
            "page": "series",
            "show_text": _("Show series selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-person-fill",
            "text": _("Authors"),
            "link": "web.author_list",
            "id": "author",
            "visibility": constants.SIDEBAR_AUTHOR,
            "public": True,
            "page": "author",
            "show_text": _("Show author selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-newspaper",
            "text": _("Publishers"),
            "link": "web.publisher_list",
            "id": "publisher",
            "visibility": constants.SIDEBAR_PUBLISHER,
            "public": True,
            "page": "publisher",
            "show_text": _("Show publisher selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-translate",
            "text": _("Languages"),
            "link": "web.language_overview",
            "id": "lang",
            "visibility": constants.SIDEBAR_LANGUAGE,
            "public": (g.user.filter_language() == "all"),
            "page": "language",
            "show_text": _("Show language selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-star",
            "text": _("Ratings"),
            "link": "web.ratings_list",
            "id": "rate",
            "visibility": constants.SIDEBAR_RATING,
            "public": True,
            "page": "rating",
            "show_text": _("Show ratings selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-file-earmark-fill",
            "text": _("File formats"),
            "link": "web.formats_list",
            "id": "format",
            "visibility": constants.SIDEBAR_FORMAT,
            "public": True,
            "page": "format",
            "show_text": _("Show file formats selection"),
            "config_show": True,
        }
    )
    sidebar.append(
        {
            "glyph": "bi-archive-fill",
            "text": _("Archived Books"),
            "link": "web.books_list",
            "id": "archived",
            "visibility": constants.SIDEBAR_ARCHIVED,
            "public": (not g.user.is_anonymous),
            "page": "archived",
            "show_text": _("Show archived books"),
            "config_show": content,
        }
    )
    if not simple:
        sidebar.append(
            {
                "glyph": "bi-list-ul",
                "text": _("Books List"),
                "link": "web.books_table",
                "id": "list",
                "visibility": constants.SIDEBAR_LIST,
                "public": (not g.user.is_anonymous),
                "page": "list",
                "show_text": _("Show Books List"),
                "config_show": content,
            }
        )
    return sidebar, simple


# Returns the template for rendering and includes the instance name
def render_title_template(*args, **kwargs):
    sidebar, simple = get_sidebar_config(kwargs)
    try:
        return render_template(
            instance=config.config_calibre_web_title,
            sidebar=sidebar,
            simple=simple,
            accept=constants.EXTENSIONS_UPLOAD,
            *args,
            **kwargs
        )
    except PermissionError:
        log.error("No permission to access {} file.".format(args[0]))
        abort(403)
