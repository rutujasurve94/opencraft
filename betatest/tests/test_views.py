# -*- coding: utf-8 -*-
#
# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015 OpenCraft <xavier@opencraft.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Tests for the betatest views
"""

# Imports #####################################################################

from collections import defaultdict
import json
import re

from bs4 import BeautifulSoup
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from betatest.models import BetaTestApplication
from instance.tests.models.factories.instance import SingleVMOpenEdXInstanceFactory
from simple_email_confirmation.models import EmailAddress


# Tests #######################################################################

class BetaTestApplicationViewTestMixin:
    """
    Tests for beta test applications.
    """
    maxDiff = None

    def setUp(self): #pylint: disable=invalid-name
        """
        Initialize the test case with some valid data.
        """
        self.form_data = {
            'subdomain': 'hogwarts',
            'instance_name': 'Hogwarts',
            'full_name': 'Albus Dumbledore',
            'username': 'albus',
            'email': 'albus.dumbledore@hogwarts.edu',
            'public_contact_email': 'support@hogwarts.edu',
            'password': 'gryffindor',
            'password_confirmation': 'gryffindor',
            'project_description': 'Online courses in Witchcraft and Wizardry',
            'accept_terms': 'on',
        }

    def register(self, form_data):
        """
        Register with the given application form data, and return the response
        content as a string.
        """
        getter = getattr(self.client, self.request_method)
        response = getter(self.url, form_data, follow=True)
        return response.content.decode('utf-8')

    def assert_registration_succeeds(self, form_data):
        """
        Assert that the given application form data creates new user, profile
        and registration instances, sends email verification messages, and
        displays a success message.
        """
        response = self.register(form_data)
        self.assertIn('Thank you for registering', response)

        # An application, user and profile should have been created
        application = BetaTestApplication.objects.get()
        user = application.user
        profile = user.profile

        # Check the application fields
        for application_field in ('subdomain',
                                  'instance_name',
                                  'public_contact_email',
                                  'project_description'):
            self.assertEqual(getattr(application, application_field),
                             self.form_data[application_field])
        self.assertEqual(application.subscribe_to_updates,
                         bool(self.form_data.get('subscribe_to_updates')))

        # Check the user fields
        for user_field in ('username', 'email'):
            self.assertEqual(getattr(user, user_field),
                             self.form_data[user_field])
        self.assertTrue(user.check_password(self.form_data['password']))

        # Check the profile fields
        self.assertEqual(profile.full_name, self.form_data['full_name'])

        # Test email verification flow
        self.assertEqual(EmailAddress.objects.count(), 2) #pylint: disable=no-member
        for email_address in (user.email, application.public_contact_email):
            email = EmailAddress.objects.get(email=email_address) #pylint: disable=no-member
            self.assertEqual(email.is_confirmed, False)
        self.assertEqual(len(mail.outbox), 2)  # fix flaky pylint: disable=no-member,useless-suppression
        for verification_email in mail.outbox:  # fix flaky pylint: disable=no-member,useless-suppression
            verify_url = re.search(r'https?://[^\s]+',
                                   verification_email.body).group(0)
            self.client.get(verify_url)
        for email_address in (user.email, application.public_contact_email):
            email = EmailAddress.objects.get(email=email_address) #pylint: disable=no-member
            self.assertEqual(email.is_confirmed, True)

    def assert_registration_fails(self, form_data, expected_errors=None):
        """
        Assert that the given application form data does not create new user,
        profile and registration instances, or send email verification
        messages.
        """
        original_count = BetaTestApplication.objects.count()
        response = self.register(form_data)
        if expected_errors:
            self.assertEqual(self.get_error_messages(response),
                             expected_errors)
        self.assertEqual(BetaTestApplication.objects.count(), original_count)
        self.assertEqual(len(mail.outbox), 0)  # fix flaky pylint: disable=no-member,useless-suppression

    def test_valid_application(self):
        """
        Test a valid beta test application.
        """
        self.assert_registration_succeeds(self.form_data)

    def test_invalid_subdomain(self):
        """
        Invalid characters in the subdomain.
        """
        self.form_data['subdomain'] = 'hogwarts?'
        self.assert_registration_fails(self.form_data, expected_errors={
            'subdomain': ["Please include only letters, numbers, '_', '-' "
                          "and '.'"],
        })

    def test_existing_subdomain(self):
        """
        Subdomain already taken.
        """
        BetaTestApplication.objects.create(
            subdomain=self.form_data['subdomain'],
            instance_name='I got here first',
            public_contact_email='test@example.com',
            project_description='test',
            user=User.objects.create(username='test'), #pylint: disable=no-member
        )
        self.assert_registration_fails(self.form_data, expected_errors={
            'subdomain': ['This domain is already taken.'],
        })

    def test_instance_subdomain(self):
        """
        Subdomain used by an existing instance.
        """
        SingleVMOpenEdXInstanceFactory.create(
            sub_domain=self.form_data['subdomain'],
        )
        self.assert_registration_fails(self.form_data, expected_errors={
            'subdomain': ['This domain is already taken.'],
        })

    def test_subdomain_with_base_domain(self):
        """
        Subdomain that includes the base domain.
        """
        form_data = self.form_data.copy()
        form_data['subdomain'] += '.' + BetaTestApplication.BASE_DOMAIN
        self.assert_registration_succeeds(form_data)

    def test_invalid_username(self):
        """
        Invalid characters in the username.
        """
        self.form_data['username'] = 'albus@dumbledore'
        self.assert_registration_fails(self.form_data, expected_errors={
            'username': ['Usernames may contain only letters, numbers, and '
                         './+/-/_ characters.'],
        })

    def test_existing_username(self):
        """
        Username already taken.
        """
        BetaTestApplication.objects.create(
            subdomain='test',
            instance_name='That username is mine',
            public_contact_email='test@example.com',
            project_description='test',
            user=User.objects.create(username=self.form_data['username']), #pylint: disable=no-member
        )
        self.assert_registration_fails(self.form_data, expected_errors={
            'username': ['This username is already taken.'],
        })

    def test_invalid_email(self):
        """
        Invalid email address.
        """
        self.form_data['email'] = 'albus'
        self.assert_registration_fails(self.form_data, expected_errors={
            'email': ['Enter a valid email address.'],
        })

    def test_existing_email(self):
        """
        Email address already taken.
        """
        BetaTestApplication.objects.create(
            subdomain='test',
            instance_name='That email address is mine',
            public_contact_email='test@example.com',
            project_description='test',
            user=User.objects.create(username='test', #pylint: disable=no-member
                                     email=self.form_data['email']),
        )
        self.assert_registration_fails(self.form_data, expected_errors={
            'email': ['This email address is already registered.'],
        })

    def test_invalid_public_contact_email(self):
        """
        Invalid public contact email address.
        """
        self.form_data['public_contact_email'] = 'hogwarts'
        self.assert_registration_fails(self.form_data, expected_errors={
            'public_contact_email': ['Enter a valid email address.'],
        })

    def test_weak_password(self):
        """
        Password not strong enough.
        """
        for password in ('password', 'qwerty', 'Hogwarts'):
            self.form_data['password'] = password
            self.form_data['password_confirmation'] = password
            self.assert_registration_fails(self.form_data, expected_errors={
                'password': ['Please use a stronger password: avoid common '
                             'patterns and make it long enough to be '
                             'difficult to crack.'],
            })

    def test_password_mismatch(self):
        """
        Password confirmation does not match password.
        """
        self.form_data['password_confirmation'] = 'slytherin'
        self.assert_registration_fails(self.form_data, expected_errors={
            'password_confirmation': ["The two password fields didn't match."],
        })


class BetaTestApplicationViewTestCase(BetaTestApplicationViewTestMixin,
                                      TestCase):
    """
    Tests for beta test applications.
    """
    url = reverse('beta:register')
    request_method = 'post'

    @staticmethod
    def get_error_messages(response):
        """
        Extract the error messages from the response body.
        """
        soup = BeautifulSoup(response, 'html.parser')
        attrs = {'class': 'djng-field-errors'}
        error_lists = [ul for ul in soup.find_all('ul', attrs=attrs)
                       if ul.get('ng-show').endswith('$pristine')]
        errors = defaultdict(list)
        for error_list in error_lists:
            pattern = r"(?:form\.(\w+)|form\['(\w+)'\])"
            match = re.match(pattern, error_list.get('ng-show'))
            name = next(group for group in match.groups() if group)
            for error in error_list.find_all('li'):
                if error.text:
                    errors[name].append(error.text)
        return errors


class BetaTestAjaxValidationTestCase(BetaTestApplicationViewTestMixin,
                                     TestCase):
    """
    Tests the ajax validation view for the beta registration form.
    """
    url = reverse('api:register-list')
    request_method = 'get'

    def assert_registration_succeeds(self, form_data):
        """
        Check that validating a valid application does not return any errors.
        """
        response = self.register(form_data)
        self.assertJSONEqual(response, '{}')

    @staticmethod
    def get_error_messages(response):
        """
        Extract error messages from the response JSON.
        """
        return json.loads(response)
