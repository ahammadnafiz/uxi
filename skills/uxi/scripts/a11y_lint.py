#!/usr/bin/env python3
"""Static accessibility lint for HTML. Stdlib only, no dependencies.

Usage: python a11y_lint.py page.html [more.html ...]

Catches the mechanical failures that show up in almost every audit:
missing alt, inputs without labels, click handlers on divs, custom widget
roles that cannot be focused, missing lang, skipped heading levels,
positive tabindex, unnamed buttons and links, placeholder-as-label,
zoom-blocking viewport meta, autoplay media, target=_blank without rel,
and outline removal in inline styles.

Of the ten common failures in references/accessibility.md this sees five:
focus removal (inline only; craft_lint.py covers stylesheets), div-with-
click-handler, placeholder-as-label, custom widgets without keyboard
support, and icon-only buttons with no accessible name. The other five
are not visible to a parser: colour as the only signal, sticky headers
covering focus, text baked into images, contrast that only fails in dark
mode, and auto-dismissing toasts. Those need the human passes.

A clean run means "no mechanical defects found", never "accessible".

Exit codes: 0 no errors (warnings allowed), 1 errors found, 2 usage error.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from typing import NamedTuple

from _common import CliError, read_text, run

INTERACTIVE_NATIVE = {"a", "button", "input", "select", "textarea",
                      "summary", "option", "label", "area", "audio", "video"}

# Elements that never have a closing tag, so they must never be pushed onto
# the open-element stack. Pushing them was a real bug: text after an <img>
# was attributed to the image, and icon-only buttons were reported as
# having no accessible name when their <img alt> was the name.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# Roles that promise a keyboard-operable widget. Carrying one without a
# tabindex on a non-interactive element means the promise is not kept.
WIDGET_ROLES = {"button", "link", "checkbox", "radio", "switch", "tab",
                "menuitem", "menuitemcheckbox", "menuitemradio", "option",
                "slider", "spinbutton", "combobox", "textbox", "treeitem"}

NAME_ATTRS = ("aria-label", "aria-labelledby", "title")


class Issue(NamedTuple):
    severity: str          # "error" or "warn"
    line: int
    message: str


class Frame:
    """One open element, and the name material collected inside it."""

    def __init__(self, tag: str, line: int, attrs: dict[str, str]) -> None:
        self.tag = tag
        self.line = line
        self.attrs = attrs
        self.name_len = 0


def _declares_no_outline(style: str) -> bool:
    """True when an inline style removes the outline.

    Checks the outline declaration itself rather than searching the whole
    attribute for "none", which used to flag `outline: 2px solid red;
    border: none` as focus removal: the exact opposite of the defect.
    """
    for declaration in style.split(";"):
        prop, _, value = declaration.partition(":")
        if prop.strip().lower() in ("outline", "outline-style",
                                    "outline-width"):
            first = value.strip().lower().split()[:1]
            if first and first[0] in ("none", "0", "0px"):
                return True
    return False


class Auditor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.issues: list[Issue] = []
        self.saw_html_lang = False
        self.html_line = 1
        self.saw_main = False
        self.h1_lines: list[int] = []
        self.last_heading = 0
        self.labeled_ids: set[str] = set()
        self.inputs: list[tuple[int, dict[str, str]]] = []
        self.stack: list[Frame] = []

    def issue(self, severity: str, message: str, line: int | None = None) -> None:
        self.issues.append(Issue(severity, line or self.getpos()[0],
                                 message))

    def _add_name_material(self, length: int) -> None:
        if length and self.stack:
            self.stack[-1].name_len += length

    def handle_starttag(self, tag: str,
                        attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: (v or "") for k, v in attrs_list}
        line = self.getpos()[0]

        if tag == "html":
            self.html_line = line
            if attrs.get("lang", "").strip():
                self.saw_html_lang = True
        if tag == "main" or attrs.get("role") == "main":
            self.saw_main = True

        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            content = attrs.get("content", "").replace(" ", "").lower()
            if "user-scalable=no" in content or "maximum-scale=1" in content:
                self.issue("error", "viewport blocks zoom; text scaling to "
                           "200 percent is a WCAG requirement, not a "
                           "preference.")

        if tag == "img":
            if "alt" not in attrs:
                self.issue("error", "<img> without an alt attribute. "
                           "Describe it, or alt=\"\" if decorative.")
            else:
                # An image's alt names the button or link that wraps it.
                self._add_name_material(len(attrs["alt"].strip()))

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            if tag == "h1":
                self.h1_lines.append(line)
            if self.last_heading and level > self.last_heading + 1:
                self.issue("error", f"heading jumps from h{self.last_heading} "
                           f"to h{level}; the outline has a hole.")
            self.last_heading = level

        if tag == "label" and attrs.get("for"):
            self.labeled_ids.add(attrs["for"])

        if tag == "input" and attrs.get("type") not in ("hidden", "submit",
                                                        "button", "image"):
            self.inputs.append((line, attrs))

        role = attrs.get("role", "").strip().lower()

        if tag not in INTERACTIVE_NATIVE and any(
                k in attrs for k in ("onclick", "onkeydown", "onmousedown")):
            if role not in WIDGET_ROLES:
                self.issue("error", f"<{tag}> has a click handler but no "
                           "interactive role. Use a real <button> or <a>, "
                           "or add role + tabindex + key handling.")

        if role in WIDGET_ROLES and tag not in INTERACTIVE_NATIVE \
                and "tabindex" not in attrs:
            self.issue("error", f"<{tag} role=\"{role}\"> is not focusable; "
                       "it needs tabindex=\"0\" and key handling, or it is a "
                       "widget only a mouse can reach.")

        if role == "dialog" and attrs.get("aria-modal") != "true":
            self.issue("warn", "role=\"dialog\" without aria-modal=\"true\"; "
                       "confirm focus is trapped and Escape closes it.")

        ti = attrs.get("tabindex", "")
        if ti and ti.lstrip("-").isdigit() and int(ti) > 0:
            self.issue("error", f"tabindex={ti} creates a custom tab order "
                       "that will fight the visual order. Use 0 or -1.")

        if tag == "a":
            if attrs.get("target") == "_blank" and "noopener" not in \
                    attrs.get("rel", ""):
                self.issue("warn", "target=_blank without rel=noopener.")
            if not attrs.get("href"):
                self.issue("warn", "<a> without href is not keyboard "
                           "reachable; if it acts, make it a button.")

        if tag in ("video", "audio") and "autoplay" in attrs and \
                "muted" not in attrs:
            self.issue("error", "autoplaying media with sound.")

        if _declares_no_outline(attrs.get("style", "")):
            self.issue("error", "inline outline removal; the keyboard focus "
                       "indicator dies here unless replaced.")

        # A labelled descendant contributes to its ancestor's name.
        if any(attrs.get(a) for a in NAME_ATTRS):
            self._add_name_material(1)

        if tag not in VOID:
            self.stack.append(Frame(tag, line, attrs))

    def handle_data(self, data: str) -> None:
        self._add_name_material(len(data.strip()))

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag:
                frame = self.stack.pop(i)
                break
        else:
            return

        # Name from content is recursive: what named the child names the
        # parent too, unless the child is hidden from the a11y tree.
        if frame.attrs.get("aria-hidden") != "true":
            self._add_name_material(frame.name_len)

        named = frame.name_len > 0 or any(frame.attrs.get(a)
                                          for a in NAME_ATTRS)
        if tag == "button" and not named:
            self.issues.append(Issue("error", frame.line,
                                     "button with no accessible name (no "
                                     "text, no image alt, no aria-label). "
                                     "Screen readers announce it as just "
                                     "'button'."))
        if tag == "a" and frame.attrs.get("href") and not named:
            self.issues.append(Issue("error", frame.line,
                                     "link with no accessible name."))

    def finish(self) -> None:
        if not self.saw_html_lang:
            self.issues.append(Issue("error", self.html_line,
                                     "no lang attribute on <html>."))
        if not self.h1_lines:
            self.issues.append(Issue("warn", 1, "no <h1> found."))
        elif len(self.h1_lines) > 1:
            self.issues.append(Issue("warn", self.h1_lines[1],
                                     f"{len(self.h1_lines)} <h1> elements; "
                                     "one per view is the convention."))
        if not self.saw_main:
            self.issues.append(Issue("warn", 1, "no <main> landmark."))
        for line, attrs in self.inputs:
            named = (attrs.get("id") in self.labeled_ids
                     or any(attrs.get(a) for a in NAME_ATTRS))
            if named:
                continue
            if attrs.get("placeholder"):
                self.issues.append(Issue("error", line, "input labeled only "
                                         "by placeholder text, which vanishes "
                                         "on focus and is skipped by some "
                                         "screen readers."))
            else:
                self.issues.append(Issue("error", line,
                                         "input with no label at all."))


def lint(path: str) -> int:
    auditor = Auditor()
    auditor.feed(read_text(path))
    auditor.finish()
    errors = [i for i in auditor.issues if i.severity == "error"]
    warns = [i for i in auditor.issues if i.severity == "warn"]
    print(f"\n{path}: {len(errors)} errors, {len(warns)} warnings")
    for issue in sorted(auditor.issues, key=lambda i: i.line):
        print(f"  [{issue.severity}] line {issue.line}: {issue.message}")
    if not auditor.issues:
        print("  no mechanical defects found. Now do the keyboard pass "
              "and a screen reader run; this tool cannot see those.")
    return len(errors)


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        raise CliError("usage: a11y_lint.py page.html [more.html ...]")
    return 1 if sum(lint(p) for p in argv) else 0


if __name__ == "__main__":
    run(main)
