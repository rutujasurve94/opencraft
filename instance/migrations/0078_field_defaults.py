# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-06 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto
import django_extensions.db.fields.json
import functools
import instance.models.load_balancer
import instance.models.mixins.database
import instance.models.mixins.rabbitmq
import instance.models.mixins.secret_keys
import instance.models.openedx_appserver
import instance.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0077_openedxappserver__is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadbalancingserver',
            name='fragment_name_postfix',
            field=models.CharField(blank=True, default=functools.partial(instance.models.load_balancer.generate_fragment_name, *(), **{'length': 8}), max_length=8),
        ),
        migrations.AlterField(
            model_name='openedxappserver',
            name='configuration_source_repo_url',
            field=models.URLField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_CONFIGURATION_REPO_URL',), **{}), max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxappserver',
            name='configuration_version',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_CONFIGURATION_VERSION',), **{}), max_length=50),
        ),
        migrations.AlterField(
            model_name='openedxappserver',
            name='edx_platform_repository_url',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_EDX_PLATFORM_REPO_URL',), **{}), help_text='URL to the edx-platform repository to use. Leave blank for default.', max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxappserver',
            name='github_admin_organizations',
            field=django_extensions.db.fields.json.JSONField(blank=True, default=[], help_text='A list of Github organizations; the members of the "Owners" team in these organizations be given SSH admin access to this instance\'s VMs.', max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxappserver',
            name='openedx_release',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_OPENEDX_RELEASE',), **{}), help_text='Set this to a release tag like "named-release/dogwood" to build a specific release of Open edX. This setting becomes the default value for edx_platform_version, forum_version, notifier_version, xqueue_version, and certs_version so it should be a git branch that exists in all of those repositories. Note: to build a specific branch of edx-platform, you should just override edx_platform_commit rather than changing this setting. Note 2: This value does not affect the default value of configuration_version.', max_length=128),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='configuration_source_repo_url',
            field=models.URLField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_CONFIGURATION_REPO_URL',), **{}), max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='configuration_version',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_CONFIGURATION_VERSION',), **{}), max_length=50),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='edx_platform_repository_url',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_EDX_PLATFORM_REPO_URL',), **{}), help_text='URL to the edx-platform repository to use. Leave blank for default.', max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='github_admin_organizations',
            field=django_extensions.db.fields.json.JSONField(blank=True, default=[], help_text='A list of Github organizations; the members of the "Owners" team in these organizations be given SSH admin access to this instance\'s VMs.', max_length=256),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mongo_pass',
            field=models.CharField(blank=True, default=functools.partial(django.utils.crypto.get_random_string, *(), **{'length': 32}), max_length=32),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mongo_user',
            field=models.CharField(blank=True, default=functools.partial(django.utils.crypto.get_random_string, *(), **{'allowed_chars': 'abcdefghijklmnopqrstuvwxyz', 'length': 16}), max_length=16),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mongodb_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='instance.MongoDBServer'),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mysql_pass',
            field=models.CharField(blank=True, default=functools.partial(django.utils.crypto.get_random_string, *(), **{'length': 32}), max_length=32),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mysql_server',
            field=models.ForeignKey(blank=True, default=instance.models.mixins.database.select_random_mysql_server, null=True, on_delete=django.db.models.deletion.PROTECT, to='instance.MySQLServer'),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='mysql_user',
            field=models.CharField(blank=True, default=functools.partial(django.utils.crypto.get_random_string, *(), **{'allowed_chars': 'abcdefghijklmnopqrstuvwxyz', 'length': 6}), max_length=16),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='openedx_release',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('DEFAULT_OPENEDX_RELEASE',), **{}), help_text='Set this to a release tag like "named-release/dogwood" to build a specific release of Open edX. This setting becomes the default value for edx_platform_version, forum_version, notifier_version, xqueue_version, and certs_version so it should be a git branch that exists in all of those repositories. Note: to build a specific branch of edx-platform, you should just override edx_platform_commit rather than changing this setting. Note 2: This value does not affect the default value of configuration_version.', max_length=128),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='openstack_region',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('OPENSTACK_REGION',), **{}), max_length=16),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='openstack_server_base_image',
            field=django_extensions.db.fields.json.JSONField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('OPENSTACK_SANDBOX_BASE_IMAGE',), **{}), help_text='JSON openstack base image selector, e.g. {"name": "ubuntu-12.04-ref-ul"} Defaults to settings.OPENSTACK_SANDBOX_BASE_IMAGE on server creation.', null=True),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='openstack_server_flavor',
            field=django_extensions.db.fields.json.JSONField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('OPENSTACK_SANDBOX_FLAVOR',), **{}), help_text='JSON openstack flavor selector, e.g. {"name": "vps-ssd-1"}. Defaults to settings.OPENSTACK_SANDBOX_FLAVOR on server creation.', null=True),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='openstack_server_ssh_keyname',
            field=models.CharField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('OPENSTACK_SANDBOX_SSH_KEYNAME',), **{}), help_text='SSH key name used when setting up access to the openstack project. Defaults to settings.OPENSTACK_SANDBOX_SSH_KEYNAME on server creation.', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='rabbitmq_consumer_user',
            field=models.ForeignKey(blank=True, default=instance.models.mixins.rabbitmq.new_rabbitmq_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consumer_instance', to='instance.RabbitMQUser'),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='rabbitmq_provider_user',
            field=models.ForeignKey(blank=True, default=instance.models.mixins.rabbitmq.new_rabbitmq_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider_instance', to='instance.RabbitMQUser'),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='rabbitmq_vhost',
            field=models.CharField(blank=True, default=instance.models.mixins.rabbitmq.generate_random_vhost, max_length=16),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='secret_key_b64encoded',
            field=models.CharField(blank=True, default=functools.partial(instance.models.mixins.secret_keys.generate_secret_key, *(48,), **{}), help_text='This field holds a base-64-encoded secret key that is generated when the instance is created, and is used to generate secret keys for individual services on each appserver.', max_length=48, verbose_name='Instance-specific base-64-encoded secret key'),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='swift_openstack_auth_url',
            field=models.URLField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('SWIFT_OPENSTACK_AUTH_URL',), **{})),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='swift_openstack_password',
            field=models.CharField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('SWIFT_OPENSTACK_PASSWORD',), **{}), max_length=64),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='swift_openstack_region',
            field=models.CharField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('SWIFT_OPENSTACK_REGION',), **{}), max_length=16),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='swift_openstack_tenant',
            field=models.CharField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('SWIFT_OPENSTACK_TENANT',), **{}), max_length=32),
        ),
        migrations.AlterField(
            model_name='openedxinstance',
            name='swift_openstack_user',
            field=models.CharField(blank=True, default=functools.partial(instance.models.utils._get_setting, *('SWIFT_OPENSTACK_USER',), **{}), max_length=32),
        ),
        migrations.AlterField(
            model_name='openstackserver',
            name='openstack_region',
            field=models.CharField(default=functools.partial(instance.models.utils._get_setting, *('OPENSTACK_REGION',), **{}), max_length=16),
        ),
    ]
