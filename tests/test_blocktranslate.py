# coding: utf-8
from __future__ import unicode_literals

import os
import sys
from threading import local

from django.template import Context
from django.template import Template
from django.template import TemplateSyntaxError
from django.test import SimpleTestCase
from django.test import override_settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import trans_real

from .base import MultipleLocaleActivationTestCase
from .base import extended_locale_paths
from .base import here
from .base import setup


def switch_on_version(py3, py2):
    return py3 if sys.version_info > (3, 0) else py2


class I18nBlockTranslateTagTests(SimpleTestCase):
    libraries = {"i18n": "django.templatetags.i18n"}

    @setup({"i18n03": "{% load i18n %}{% blocktranslate %}{{ anton }}{% endblocktranslate %}"})
    def test_i18n03(self):
        """simple translation of a variable"""
        output = self.engine.render_to_string("i18n03", {"anton": "Å"})
        self.assertEqual(output, "Å")

    @setup(
        {
            "i18n04": "{% load i18n %}{% blocktranslate with berta=anton|lower %}{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_i18n04(self):
        """simple translation of a variable and filter"""
        output = self.engine.render_to_string("i18n04", {"anton": "Å"})
        self.assertEqual(output, "å")

    @setup(
        {
            "legacyi18n04": "{% load i18n %}"
            "{% blocktranslate with anton|lower as berta %}{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_legacyi18n04(self):
        """simple translation of a variable and filter"""
        output = self.engine.render_to_string("legacyi18n04", {"anton": "Å"})
        self.assertEqual(output, "å")

    @setup(
        {
            "i18n05": "{% load i18n %}{% blocktranslate %}xxx{{ anton }}xxx{% endblocktranslate %}"
        }
    )
    def test_i18n05(self):
        """simple translation of a string with interpolation"""
        output = self.engine.render_to_string("i18n05", {"anton": "yyy"})
        self.assertEqual(output, "xxxyyyxxx")

    @setup(
        {
            "i18n07": "{% load i18n %}"
            "{% blocktranslate count counter=number %}singular{% plural %}"
            "{{ counter }} plural{% endblocktranslate %}"
        }
    )
    def test_i18n07(self):
        """translation of singular form"""
        output = self.engine.render_to_string("i18n07", {"number": 1})
        self.assertEqual(output, "singular")

    @setup(
        {
            "legacyi18n07": "{% load i18n %}"
            "{% blocktranslate count number as counter %}singular{% plural %}"
            "{{ counter }} plural{% endblocktranslate %}"
        }
    )
    def test_legacyi18n07(self):
        """translation of singular form"""
        output = self.engine.render_to_string("legacyi18n07", {"number": 1})
        self.assertEqual(output, "singular")

    @setup(
        {
            "i18n08": "{% load i18n %}"
            "{% blocktranslate count number as counter %}singular{% plural %}"
            "{{ counter }} plural{% endblocktranslate %}"
        }
    )
    def test_i18n08(self):
        """translation of plural form"""
        output = self.engine.render_to_string("i18n08", {"number": 2})
        self.assertEqual(output, "2 plural")

    @setup(
        {
            "legacyi18n08": "{% load i18n %}"
            "{% blocktranslate count counter=number %}singular{% plural %}"
            "{{ counter }} plural{% endblocktranslate %}"
        }
    )
    def test_legacyi18n08(self):
        """translation of plural form"""
        output = self.engine.render_to_string("legacyi18n08", {"number": 2})
        self.assertEqual(output, "2 plural")

    @setup(
        {
            "i18n17": "{% load i18n %}"
            "{% blocktranslate with berta=anton|escape %}{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_i18n17(self):
        """
        Escaping inside blocktranslate and trans works as if it was directly in the
        template.
        """
        output = self.engine.render_to_string("i18n17", {"anton": "α & β"})
        self.assertEqual(output, "α &amp; β")

    @setup(
        {
            "i18n18": "{% load i18n %}"
            "{% blocktranslate with berta=anton|force_escape %}{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_i18n18(self):
        output = self.engine.render_to_string("i18n18", {"anton": "α & β"})
        self.assertEqual(output, "α &amp; β")

    @setup({"i18n19": "{% load i18n %}{% blocktranslate %}{{ andrew }}{% endblocktranslate %}"})
    def test_i18n19(self):
        output = self.engine.render_to_string("i18n19", {"andrew": "a & b"})
        self.assertEqual(output, "a &amp; b")

    @setup({"i18n21": "{% load i18n %}{% blocktranslate %}{{ andrew }}{% endblocktranslate %}"})
    def test_i18n21(self):
        output = self.engine.render_to_string("i18n21", {"andrew": mark_safe("a & b")})
        self.assertEqual(output, "a & b")

    @setup(
        {
            "legacyi18n17": "{% load i18n %}"
            "{% blocktranslate with anton|escape as berta %}{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_legacyi18n17(self):
        output = self.engine.render_to_string("legacyi18n17", {"anton": "α & β"})
        self.assertEqual(output, "α &amp; β")

    @setup(
        {
            "legacyi18n18": "{% load i18n %}"
            "{% blocktranslate with anton|force_escape as berta %}"
            "{{ berta }}{% endblocktranslate %}"
        }
    )
    def test_legacyi18n18(self):
        output = self.engine.render_to_string("legacyi18n18", {"anton": "α & β"})
        self.assertEqual(output, "α &amp; β")

    @setup(
        {
            "i18n26": "{% load i18n %}"
            "{% blocktranslate with extra_field=myextra_field count counter=number %}"
            "singular {{ extra_field }}{% plural %}plural{% endblocktranslate %}"
        }
    )
    def test_i18n26(self):
        """
        translation of plural form with extra field in singular form (#13568)
        """
        output = self.engine.render_to_string(
            "i18n26", {"myextra_field": "test", "number": 1}
        )
        self.assertEqual(output, "singular test")

    @setup(
        {
            "legacyi18n26": "{% load i18n %}"
            "{% blocktranslate with myextra_field as extra_field count number as counter %}"
            "singular {{ extra_field }}{% plural %}plural{% endblocktranslate %}"
        }
    )
    def test_legacyi18n26(self):
        output = self.engine.render_to_string(
            "legacyi18n26", {"myextra_field": "test", "number": 1}
        )
        self.assertEqual(output, "singular test")

    @setup(
        {
            "i18n27": "{% load i18n %}{% blocktranslate count counter=number %}"
            "{{ counter }} result{% plural %}{{ counter }} results"
            "{% endblocktranslate %}"
        }
    )
    def test_i18n27(self):
        """translation of singular form in Russian (#14126)"""
        with translation.override("ru"):
            output = self.engine.render_to_string("i18n27", {"number": 1})
        self.assertEqual(
            output, "1 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442"
        )

    @setup(
        {
            "legacyi18n27": "{% load i18n %}"
            "{% blocktranslate count number as counter %}{{ counter }} result"
            "{% plural %}{{ counter }} results{% endblocktranslate %}"
        }
    )
    def test_legacyi18n27(self):
        with translation.override("ru"):
            output = self.engine.render_to_string("legacyi18n27", {"number": 1})
        self.assertEqual(
            output, "1 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442"
        )

    @setup(
        {
            "i18n28": "{% load i18n %}"
            "{% blocktranslate with a=anton b=berta %}{{ a }} + {{ b }}{% endblocktranslate %}"
        }
    )
    def test_i18n28(self):
        """simple translation of multiple variables"""
        output = self.engine.render_to_string("i18n28", {"anton": "α", "berta": "β"})
        self.assertEqual(output, "α + β")

    @setup(
        {
            "legacyi18n28": "{% load i18n %}"
            "{% blocktranslate with anton as a and berta as b %}"
            "{{ a }} + {{ b }}{% endblocktranslate %}"
        }
    )
    def test_legacyi18n28(self):
        output = self.engine.render_to_string(
            "legacyi18n28", {"anton": "α", "berta": "β"}
        )
        self.assertEqual(output, "α + β")

    # blocktranslate handling of variables which are not in the context.
    # this should work as if blocktranslate was not there (#19915)
    @setup(
        {"i18n34": "{% load i18n %}{% blocktranslate %}{{ missing }}{% endblocktranslate %}"}
    )
    def test_i18n34(self):
        output = self.engine.render_to_string("i18n34")
        if self.engine.string_if_invalid:
            self.assertEqual(output, "INVALID")
        else:
            self.assertEqual(output, "")

    @setup(
        {
            "i18n34_2": "{% load i18n %}{% blocktranslate with a='α' %}{{ missing }}{% endblocktranslate %}"
        }
    )
    def test_i18n34_2(self):
        output = self.engine.render_to_string("i18n34_2")
        if self.engine.string_if_invalid:
            self.assertEqual(output, "INVALID")
        else:
            self.assertEqual(output, "")

    @setup(
        {
            "i18n34_3": "{% load i18n %}{% blocktranslate with a=anton %}{{ missing }}{% endblocktranslate %}"
        }
    )
    def test_i18n34_3(self):
        output = self.engine.render_to_string("i18n34_3", {"anton": "\xce\xb1"})
        if self.engine.string_if_invalid:
            self.assertEqual(output, "INVALID")
        else:
            self.assertEqual(output, "")

    @setup(
        {
            "i18n37": "{% load i18n %}"
            '{% trans "Page not found" as page_not_found %}'
            "{% blocktranslate %}Error: {{ page_not_found }}{% endblocktranslate %}"
        }
    )
    def test_i18n37(self):
        with translation.override("de"):
            output = self.engine.render_to_string("i18n37")
        self.assertEqual(output, "Error: Seite nicht gefunden")

    # blocktranslate tag with asvar
    @setup(
        {
            "i18n39": "{% load i18n %}"
            "{% blocktranslate asvar page_not_found %}Page not found{% endblocktranslate %}"
            ">{{ page_not_found }}<"
        }
    )
    def test_i18n39(self):
        with translation.override("de"):
            output = self.engine.render_to_string("i18n39")
        self.assertEqual(output, ">Seite nicht gefunden<")

    @setup(
        {
            "i18n40": "{% load i18n %}"
            '{% trans "Page not found" as pg_404 %}'
            "{% blocktranslate with page_not_found=pg_404 asvar output %}"
            "Error: {{ page_not_found }}"
            "{% endblocktranslate %}"
        }
    )
    def test_i18n40(self):
        output = self.engine.render_to_string("i18n40")
        self.assertEqual(output, "")

    @setup(
        {
            "i18n41": "{% load i18n %}"
            '{% trans "Page not found" as pg_404 %}'
            "{% blocktranslate with page_not_found=pg_404 asvar output %}"
            "Error: {{ page_not_found }}"
            "{% endblocktranslate %}"
            ">{{ output }}<"
        }
    )
    def test_i18n41(self):
        with translation.override("de"):
            output = self.engine.render_to_string("i18n41")
        self.assertEqual(output, ">Error: Seite nicht gefunden<")

    @setup({"template": "{% load i18n %}{% blocktranslate asvar %}Yes{% endblocktranslate %}"})
    def test_blocktrans_syntax_error_missing_assignment(self):
        msg = "No argument provided to the 'blocktranslate' tag for the asvar option."
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template")

    @setup({"template": "{% load i18n %}{% blocktranslate %}%s{% endblocktranslate %}"})
    def test_blocktrans_tag_using_a_string_that_looks_like_str_fmt(self):
        output = self.engine.render_to_string("template")
        self.assertEqual(output, "%s")

    @setup(
        {
            "template": "{% load i18n %}{% blocktranslate %}{% block b %} {% endblock %}{% endblocktranslate %}"
        }
    )
    def test_with_block(self):
        msg = switch_on_version(
            "'blocktranslate' doesn't allow other block tags (seen 'block b') inside it",
            "'blocktranslate' doesn't allow other block tags (seen u'block b') inside it"
        )
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template")

    @setup(
        {
            "template": "{% load i18n %}{% blocktranslate %}{% for b in [1, 2, 3] %} {% endfor %}{% endblocktranslate %}"
        }
    )
    def test_with_for(self):
        msg = switch_on_version(
            "'blocktranslate' doesn't allow other block tags (seen 'for b in [1, 2, 3]') inside it",
            "'blocktranslate' doesn't allow other block tags (seen u'for b in [1, 2, 3]') inside it"
        )
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template")

    @setup(
        {
            "template": "{% load i18n %}{% blocktranslate with foo=bar with %}{{ foo }}{% endblocktranslate %}"
        }
    )
    def test_variable_twice(self):
        msg = switch_on_version(
            "The 'with' option was specified more than once",
            "The u'with' option was specified more than once",
        )
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template", {"foo": "bar"})

    @setup({"template": "{% load i18n %}{% blocktranslate with %}{% endblocktranslate %}"})
    def test_no_args_with(self):
        msg = switch_on_version(
            "\"with\" in 'blocktranslate' tag needs at least one keyword argument.",
            "\"with\" in u'blocktranslate' tag needs at least one keyword argument.",
        )
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template")

    @setup({"template": "{% load i18n %}{% blocktranslate count a %}{% endblocktranslate %}"})
    def test_count(self):
        msg = switch_on_version(
            "\"count\" in 'blocktranslate' tag expected exactly one keyword argument.",
            "\"count\" in u'blocktranslate' tag expected exactly one keyword argument.",
        )
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template", {"a": [1, 2, 3]})

    @setup(
        {
            "template": (
                "{% load i18n %}{% blocktranslate count count=var|length %}"
                "There is {{ count }} object. {% block a %} {% endblock %}"
                "{% endblocktranslate %}"
            )
        }
    )
    def test_plural_bad_syntax(self):
        msg = "'blocktranslate' doesn't allow other block tags inside it"
        with self.assertRaisesMessage(TemplateSyntaxError, msg):
            self.engine.render_to_string("template", {"var": [1, 2, 3]})


class TranslationBlockTranslateTagTests(SimpleTestCase):
    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_template_tags_pgettext(self):
        """{% blocktranslate %} takes message contexts into account (#14806)."""
        trans_real._active = local()
        trans_real._translations = {}
        with translation.override("de"):
            # Nonexistent context
            t = Template(
                '{% load i18n %}{% blocktranslate context "nonexistent" %}May{% endblocktranslate %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "May")

            # Existing context...  using a literal
            t = Template(
                '{% load i18n %}{% blocktranslate context "month name" %}May{% endblocktranslate %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "Mai")
            t = Template(
                '{% load i18n %}{% blocktranslate context "verb" %}May{% endblocktranslate %}'
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "Kann")

            # Using a variable
            t = Template(
                "{% load i18n %}{% blocktranslate context message_context %}May{% endblocktranslate %}"
            )
            rendered = t.render(Context({"message_context": "month name"}))
            self.assertEqual(rendered, "Mai")
            t = Template(
                "{% load i18n %}{% blocktranslate context message_context %}May{% endblocktranslate %}"
            )
            rendered = t.render(Context({"message_context": "verb"}))
            self.assertEqual(rendered, "Kann")

            # Using a filter
            t = Template(
                "{% load i18n %}{% blocktranslate context message_context|lower %}May{% endblocktranslate %}"
            )
            rendered = t.render(Context({"message_context": "MONTH NAME"}))
            self.assertEqual(rendered, "Mai")
            t = Template(
                "{% load i18n %}{% blocktranslate context message_context|lower %}May{% endblocktranslate %}"
            )
            rendered = t.render(Context({"message_context": "VERB"}))
            self.assertEqual(rendered, "Kann")

            # Using 'count'
            t = Template(
                '{% load i18n %}{% blocktranslate count number=1 context "super search" %}'
                "{{ number }} super result{% plural %}{{ number }} super results{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "1 Super-Ergebnis")
            t = Template(
                '{% load i18n %}{% blocktranslate count number=2 context "super search" %}{{ number }}'
                " super result{% plural %}{{ number }} super results{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "2 Super-Ergebnisse")
            t = Template(
                '{% load i18n %}{% blocktranslate context "other super search" count number=1 %}'
                "{{ number }} super result{% plural %}{{ number }} super results{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "1 anderen Super-Ergebnis")
            t = Template(
                '{% load i18n %}{% blocktranslate context "other super search" count number=2 %}'
                "{{ number }} super result{% plural %}{{ number }} super results{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "2 andere Super-Ergebnisse")

            # Using 'with'
            t = Template(
                '{% load i18n %}{% blocktranslate with num_comments=5 context "comment count" %}'
                "There are {{ num_comments }} comments{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "Es gibt 5 Kommentare")
            t = Template(
                '{% load i18n %}{% blocktranslate with num_comments=5 context "other comment count" %}'
                "There are {{ num_comments }} comments{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "Andere: Es gibt 5 Kommentare")

            # Using trimmed
            t = Template(
                "{% load i18n %}{% blocktranslate trimmed %}\n\nThere\n\t are 5  "
                "\n\n   comments\n{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "There are 5 comments")
            t = Template(
                '{% load i18n %}{% blocktranslate with num_comments=5 context "comment count" trimmed %}\n\n'
                "There are  \t\n  \t {{ num_comments }} comments\n\n{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "Es gibt 5 Kommentare")
            t = Template(
                '{% load i18n %}{% blocktranslate context "other super search" count number=2 trimmed %}\n'
                "{{ number }} super \n result{% plural %}{{ number }} super results{% endblocktranslate %}"
            )
            rendered = t.render(Context())
            self.assertEqual(rendered, "2 andere Super-Ergebnisse")

            # Misuses
            msg = switch_on_version(
                "Unknown argument for 'blocktranslate' tag: %r.",
                "Unknown argument for u'blocktranslate' tag: %r.",
            )
            with self.assertRaisesMessage(TemplateSyntaxError, msg % 'month="May"'):
                Template(
                    '{% load i18n %}{% blocktranslate context with month="May" %}{{ month }}{% endblocktranslate %}'
                )
            msg = '"context" in %r tag expected exactly one argument.' % "blocktranslate"
            with self.assertRaisesMessage(TemplateSyntaxError, msg):
                Template("{% load i18n %}{% blocktranslate context %}{% endblocktranslate %}")
            with self.assertRaisesMessage(TemplateSyntaxError, msg):
                Template(
                    "{% load i18n %}{% blocktranslate count number=2 context %}"
                    "{{ number }} super result{% plural %}{{ number }}"
                    " super results{% endblocktranslate %}"
                )

    @override_settings(LOCALE_PATHS=[os.path.join(here, "other", "locale")])
    def test_bad_placeholder_1(self):
        """
        Error in translation file should not crash template rendering (#16516).
        (%(person)s is translated as %(personne)s in fr.po).
        """
        with translation.override("fr"):
            t = Template(
                "{% load i18n %}{% blocktranslate %}My name is {{ person }}.{% endblocktranslate %}"
            )
            rendered = t.render(Context({"person": "James"}))
            self.assertEqual(rendered, "My name is James.")

    @override_settings(LOCALE_PATHS=[os.path.join(here, "other", "locale")])
    def test_bad_placeholder_2(self):
        """
        Error in translation file should not crash template rendering (#18393).
        (%(person) misses a 's' in fr.po, causing the string formatting to fail)
        .
        """
        with translation.override("fr"):
            t = Template(
                "{% load i18n %}{% blocktranslate %}My other name is {{ person }}.{% endblocktranslate %}"
            )
            rendered = t.render(Context({"person": "James"}))
            self.assertEqual(rendered, "My other name is James.")


class MultipleLocaleActivationBlockTransTests(MultipleLocaleActivationTestCase):
    def test_single_locale_activation(self):
        """
        Simple baseline behavior with one locale for all the supported i18n
        constructs.
        """
        with translation.override("fr"):
            self.assertEqual(
                Template(
                    "{% load i18n %}{% blocktranslate %}Yes{% endblocktranslate %}"
                ).render(Context({})),
                "Oui",
            )

    def test_multiple_locale_btrans(self):
        with translation.override("de"):
            t = Template("{% load i18n %}{% blocktranslate %}No{% endblocktranslate %}")
        with translation.override(self._old_language), translation.override("nl"):
            self.assertEqual(t.render(Context({})), "Nee")

    def test_multiple_locale_deactivate_btrans(self):
        with translation.override("de", deactivate=True):
            t = Template("{% load i18n %}{% blocktranslate %}No{% endblocktranslate %}")
        with translation.override("nl"):
            self.assertEqual(t.render(Context({})), "Nee")

    def test_multiple_locale_direct_switch_btrans(self):
        with translation.override("de"):
            t = Template("{% load i18n %}{% blocktranslate %}No{% endblocktranslate %}")
        with translation.override("nl"):
            self.assertEqual(t.render(Context({})), "Nee")


class MiscTests(SimpleTestCase):
    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_percent_in_translatable_block(self):
        t_sing = Template(
            "{% load i18n %}{% blocktranslate %}The result was {{ percent }}%{% endblocktranslate %}"
        )
        t_plur = Template(
            "{% load i18n %}{% blocktranslate count num as number %}"
            "{{ percent }}% represents {{ num }} object{% plural %}"
            "{{ percent }}% represents {{ num }} objects{% endblocktranslate %}"
        )
        with translation.override("de"):
            self.assertEqual(
                t_sing.render(Context({"percent": 42})), "Das Ergebnis war 42%"
            )
            self.assertEqual(
                t_plur.render(Context({"percent": 42, "num": 1})),
                "42% stellt 1 Objekt dar",
            )
            self.assertEqual(
                t_plur.render(Context({"percent": 42, "num": 4})),
                "42% stellt 4 Objekte dar",
            )

    @override_settings(LOCALE_PATHS=extended_locale_paths)
    def test_percent_formatting_in_blocktrans(self):
        """
        Python's %-formatting is properly escaped in blocktrans, singular, or
        plural.
        """
        t_sing = Template(
            "{% load i18n %}{% blocktranslate %}There are %(num_comments)s comments{% endblocktranslate %}"
        )
        t_plur = Template(
            "{% load i18n %}{% blocktranslate count num as number %}"
            "%(percent)s% represents {{ num }} object{% plural %}"
            "%(percent)s% represents {{ num }} objects{% endblocktranslate %}"
        )
        with translation.override("de"):
            # Strings won't get translated as they don't match after escaping %
            self.assertEqual(
                t_sing.render(Context({"num_comments": 42})),
                "There are %(num_comments)s comments",
            )
            self.assertEqual(
                t_plur.render(Context({"percent": 42, "num": 1})),
                "%(percent)s% represents 1 object",
            )
            self.assertEqual(
                t_plur.render(Context({"percent": 42, "num": 4})),
                "%(percent)s% represents 4 objects",
            )
