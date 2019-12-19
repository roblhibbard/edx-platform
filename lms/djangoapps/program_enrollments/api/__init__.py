"""
Python API exposed by the program_enrollments app to other in-process apps.

The functions are split into separate files for code organization, but they
are imported into here so they can be imported directly from
`lms.djangoapps.program_enrollments.api`.

When adding new functions to this API, add them to the appropriate module
within the /api/ folder, and then "expose" them here by importing them.

We use explicit imports here because (1) it hides internal variables in the
sub-modules and (2) it provides a nice catalog of functions for someone
using this API.
"""
from __future__ import absolute_import

from .grades import iter_program_course_grades
from .linking import link_program_enrollment_to_lms_user, link_program_enrollments
from .reading import (
    fetch_program_course_enrollments,
    fetch_program_course_enrollments_by_student,
    fetch_program_enrollments,
    fetch_program_enrollments_by_student,
    get_program_course_enrollment,
    get_program_enrollment,
    get_provider_slug,
    get_saml_provider_for_organization,
    get_saml_provider_for_program,
    get_users_by_external_keys
)
from .writing import (
    change_program_course_enrollment_status,
    change_program_enrollment_status,
    create_program_course_enrollment,
    create_program_enrollment,
    enroll_in_masters_track,
    write_program_course_enrollments,
    write_program_enrollments
)
