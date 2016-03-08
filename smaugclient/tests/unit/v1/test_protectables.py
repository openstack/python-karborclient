#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from smaugclient.tests.unit import base
from smaugclient.tests.unit.v1 import fakes

cs = fakes.FakeClient()
mock_request_return = ({}, {'protectable_type': {}})
mock_instances_request_return = ({}, {'instances': {}})


class ProtectablesTest(base.TestCaseShell):

    @mock.patch('smaugclient.common.http.HTTPClient.json_request')
    def test_list_protectables(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.protectables.list()
        mock_request.assert_called_with(
            'GET',
            '/v1/{project_id}/protectables'.format(
                project_id=fakes.PROJECT_ID), headers={})

    @mock.patch('smaugclient.common.http.HTTPClient.json_request')
    def test_get_protectables(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.protectables.get('OS::Cinder::Volume')
        mock_request.assert_called_with(
            'GET',
            '/v1/{project_id}/protectables/OS::Cinder::Volume'.format(
                project_id=fakes.PROJECT_ID), headers={})

    @mock.patch('smaugclient.common.http.HTTPClient.json_request')
    def test_list_protectables_instances(self, mock_request):
        mock_request.return_value = mock_instances_request_return
        cs.protectables.list_instances('OS::Cinder::Volume')
        mock_request.assert_called_with(
            'GET',
            '/v1/{project_id}/protectables/OS::Cinder::Volume/'
            'instances'.format(project_id=fakes.PROJECT_ID), headers={})

    @mock.patch('smaugclient.common.http.HTTPClient.json_request')
    def test_list_protectables_instances_with_marker_limit(self, mock_request):
        mock_request.return_value = mock_instances_request_return
        cs.protectables.list_instances('OS::Cinder::Volume',
                                       marker=1234, limit=2)
        mock_request.assert_called_with(
            'GET',
            '/v1/{project_id}/protectables/OS::Cinder::Volume/'
            'instances?limit=2&marker=1234'.format(
                project_id=fakes.PROJECT_ID), headers={})

    @mock.patch('smaugclient.common.http.HTTPClient.json_request')
    def test_list_protectables_instances_with_sort_key_dir(self, mock_request):
        mock_request.return_value = mock_instances_request_return
        cs.protectables.list_instances('OS::Cinder::Volume',
                                       sort_key='id', sort_dir='asc')
        mock_request.assert_called_with(
            'GET',
            '/v1/{project_id}/protectables/OS::Cinder::Volume/'
            'instances?sort_dir=asc&sort_key=id'.format(
                project_id=fakes.PROJECT_ID), headers={})

    def test_list_protectables_instances_with_invalid_sort_key(self):
        self.assertRaises(ValueError,
                          cs.protectables.list_instances, 'OS::Cinder::Volume',
                          sort_key='invalid', sort_dir='asc')
