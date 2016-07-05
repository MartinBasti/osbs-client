"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""
import pytest

from osbs.build.spec import BuildIDParam, RegistryURIsParam, BuildSpec
from osbs.exceptions import OsbsValidationException
from tests.constants import TEST_USER


class TestBuildIDParam(object):
    def test_build_id_param_shorten_id(self):
        p = BuildIDParam()
        p.value = "x" * 63

        val = p.value

        assert len(val) == 63

    def test_build_id_param_raise_exc(self):
        p = BuildIDParam()
        with pytest.raises(OsbsValidationException):
            p.value = r"\\\\@@@@||||"


class TestRegistryURIsParam(object):
    @pytest.mark.parametrize('suffix', ['', '/'])
    def test_registry_uris_param_api_implicit(self, suffix):
        p = RegistryURIsParam()
        p.value = ['registry.example.com:5000{suffix}'.format(suffix=suffix)]

        assert p.value[0].uri == 'registry.example.com:5000'
        assert p.value[0].docker_uri == 'registry.example.com:5000'
        assert p.value[0].version == 'v1'

    def test_registry_uris_param_v2(self):
        p = RegistryURIsParam()
        p.value = ['registry.example.com:5000/v2']

        assert p.value[0].uri == 'registry.example.com:5000'
        assert p.value[0].docker_uri == 'registry.example.com:5000'
        assert p.value[0].version == 'v2'


class TestBuildSpec(object):

    def get_minimal_kwargs(self):
        return {
            # Params needed to avoid exceptions.
            'user': 'user',
            'base_image': 'base_image',
            'name_label': 'name_label',
            'source_registry_uri': 'source_registry_uri',
            'git_uri': 'https://github.com/user/reponame.git',
            'registry_uris': ['http://registry.example.com:5000/v2'],
        }

    def test_spec_name(self):
        kwargs = self.get_minimal_kwargs()
        kwargs.update({
            'git_uri': 'https://github.com/user/reponame.git',
            'git_branch': 'master',
        })

        spec = BuildSpec()
        spec.set_params(**kwargs)

        assert spec.name.value == 'reponame-master'
        registry = spec.registry_uris.value[0]
        assert registry.uri == 'http://registry.example.com:5000'
        assert registry.docker_uri == 'registry.example.com:5000'
        assert registry.version == 'v2'
