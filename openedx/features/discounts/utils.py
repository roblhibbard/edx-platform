"""
Utility functions for working with discounts and discounted pricing.
"""

from datetime import datetime

import six
from django.utils.translation import ugettext as _
import pytz

from course_modes.models import get_course_prices, format_course_price
from lms.djangoapps.courseware.date_summary import verified_upgrade_deadline_link
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from experiments.models import ExperimentData

from openedx.core.djangolib.markup import HTML
from web_fragments.fragment import Fragment
from openedx.features.discounts.applicability import (
    can_receive_discount,
    get_discount_expiration_date,
    discount_percentage
)

REV1008_EXPERIMENT_ID = 15


def offer_banner_wrapper(user, block, view, frag, context):  # pylint: disable=W0613
    """
    A wrapper that prepends the First Purchase Discount banner if
    the user hasn't upgraded yet.
    """
    if block.category != "vertical":
        return frag

    course = CourseOverview.get_from_id(block.course_id)
    offer_banner_fragment = get_first_purchase_offer_banner_fragment(user, course)

    if not offer_banner_fragment:
        return frag

    # Course content must be escaped to render correctly due to the way the
    # way the XBlock rendering works. Transforming the safe markup to unicode
    # escapes correctly.
    offer_banner_fragment.content = six.text_type(offer_banner_fragment.content)

    offer_banner_fragment.add_content(frag.content)
    offer_banner_fragment.add_fragment_resources(frag)

    return offer_banner_fragment


def format_strikeout_price(user, course, base_price=None, check_for_discount=True):
    """
    Return a formatted price, including a struck-out original price if a discount applies, and also
        whether a discount was applied, as the tuple (formatted_price, has_discount).
    """
    if base_price is None:
        base_price = get_course_prices(course, verified_only=True)[0]

    original_price = format_course_price(base_price)

    if not check_for_discount or can_receive_discount(user, course):
        discount_price = base_price * ((100.0 - discount_percentage(course)) / 100)
        if discount_price == int(discount_price):
            discount_price = format_course_price("{:0.0f}".format(discount_price))
        else:
            discount_price = format_course_price("{:0.2f}".format(discount_price))

        # Separate out this string because it has a lot of syntax but no actual information for
        # translators to translate
        formatted_discount_price = HTML(
            u"{s_dp}{discount_price}{e_p} {s_st}{s_op}{original_price}{e_p}{e_st}"
        ).format(
            original_price=original_price,
            discount_price=discount_price,
            s_op=HTML("<span class='price original'>"),
            s_dp=HTML("<span class='price discount'>"),
            s_st=HTML("<del aria-hidden='true'>"),
            e_p=HTML("</span>"),
            e_st=HTML("</del>"),
        )

        return (
            HTML(_(
                u"{s_sr}Original price: {s_op}{original_price}{e_p}, discount price: {e_sr}{formatted_discount_price}"
            )).format(
                original_price=original_price,
                formatted_discount_price=formatted_discount_price,
                s_sr=HTML("<span class='sr'>"),
                s_op=HTML("<span class='price original'>"),
                e_p=HTML("</span>"),
                e_sr=HTML("</span>"),
            ),
            True
        )
    else:
        return (HTML(u"<span class='price'>{}</span>").format(original_price), False)


def get_first_purchase_offer_banner_fragment(user, course):
    """
    Return an HTML Fragment with First Purcahse Discount message,
    which has the discount_expiration_date, price,
    discount percentage and a link to upgrade.
    """
    if user and not user.is_anonymous and course:
        now = datetime.now(tz=pytz.UTC).strftime(u"%Y-%m-%d %H:%M:%S%z")
        saw_banner = ExperimentData.objects.filter(
            user=user, experiment_id=REV1008_EXPERIMENT_ID, key=str(course)
        )
        if not saw_banner:
            ExperimentData.objects.create(
                user=user, experiment_id=REV1008_EXPERIMENT_ID, key=str(course), value=now
            )
        discount_expiration_date = get_discount_expiration_date(user, course)
        if (discount_expiration_date and
                can_receive_discount(user=user, course=course, discount_expiration_date=discount_expiration_date)):
            # Translator: xgettext:no-python-format
            offer_message = _(u'{banner_open} Upgrade by {discount_expiration_date} and save {percentage}% '
                              u'[{strikeout_price}]{span_close}{br}Discount will be automatically applied at checkout. '
                              u'{a_open}Upgrade Now{a_close}{div_close}')
            return Fragment(HTML(offer_message).format(
                a_open=HTML(u'<a href="{upgrade_link}">').format(
                    upgrade_link=verified_upgrade_deadline_link(user=user, course=course)
                ),
                a_close=HTML('</a>'),
                br=HTML('<br>'),
                banner_open=HTML(
                    '<div class="first-purchase-offer-banner" role="note">'
                    '<span class="first-purchase-offer-banner-bold">'
                ),
                discount_expiration_date=discount_expiration_date.strftime(u'%B %d'),
                percentage=discount_percentage(course),
                span_close=HTML('</span>'),
                div_close=HTML('</div>'),
                strikeout_price=HTML(format_strikeout_price(user, course, check_for_discount=False)[0])
            ))
    return None
