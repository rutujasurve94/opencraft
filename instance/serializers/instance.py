# -*- coding: utf-8 -*-
#
# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015-2016 OpenCraft <contact@opencraft.com>
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
Instance serializers (API representation)
"""

# Imports #####################################################################

from rest_framework import serializers

from instance.models.instance import SingleVMOpenEdXInstance
from instance.serializers.server import OpenStackServerSerializer
from instance.serializers.logentry import LogEntrySerializer


# Serializers #################################################################

class SingleVMOpenEdXInstanceListSerializer(serializers.ModelSerializer):
    """
    SingleVMOpenEdXInstance API Serializer (list view).
    """
    api_url = serializers.HyperlinkedIdentityField(view_name='api:singlevmopenedxinstance-detail')
    active_server_set = OpenStackServerSerializer(many=True, read_only=True)

    class Meta:
        model = SingleVMOpenEdXInstance
        fields = (
            'id',
            'api_url',
            'active_server_set',
            'ansible_settings',
            'base_domain',
            'branch_name',
            'commit_id',
            'created',
            'domain',
            'email',
            'github_base_url',
            'github_branch_url',
            'github_pr_number',
            'github_pr_url',
            'github_organization_name',
            'modified',
            'name',
            'protocol',
            'repository_url',
            'status',
            'studio_url',
            'sub_domain',
            'url',
            'updates_feed',
        )

    def to_representation(self, obj):
        output = super().to_representation(obj)
        # Convert the state values from objects to strings:
        output['status'] = obj.status.state_id
        # Add state name and description for display purposes:
        output['status_name'] = obj.status.name
        output['status_description'] = obj.status.description
        # Add info about relevant conditions related to instance status
        output['is_steady'] = obj.status.is_steady_state
        output['is_healthy'] = obj.status.is_healthy_state
        return output


class SingleVMOpenEdXInstanceDetailSerializer(SingleVMOpenEdXInstanceListSerializer):
    """
    SingleVMOpenEdXInstance API Serializer (detail view). Includes log entries.
    """
    log_entries = LogEntrySerializer(many=True, read_only=True)
    log_error_entries = LogEntrySerializer(many=True, read_only=True)

    class Meta(SingleVMOpenEdXInstanceListSerializer.Meta):
        fields = SingleVMOpenEdXInstanceListSerializer.Meta.fields + ('log_entries', 'log_error_entries')
