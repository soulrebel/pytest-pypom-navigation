# -*- coding: utf-8 -*-

import pytest


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth(bar):
            assert bar == "europython2015"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--foo=europython2015',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'pypom-navigation:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])


def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_skin(skin):
    """ Skin fixture must return default value """
    assert skin == 'skin1'


def test_default_pages(default_pages, skin):
    """ Default pages fixture must return a valid mapping for default skin """
    assert default_pages[skin] == 'pypom_navigation.pages.BasePage'


def test_page_mappings(page_mappings):
    """ Empty page mappings by default """
    assert len(page_mappings.keys()) == 0


def test_default_page_class(default_page_class):
    """ Default page class """
    from pypom_navigation.pages import BasePage
    assert default_page_class is BasePage


def test_navigation_class(navigation_class):
    """ Default navigation class """
    from pypom_navigation.navigation import Navigation
    assert navigation_class is Navigation


@pytest.mark.parametrize('credentials_file', ['credentials.json',
                                              'credentials.yml'])
def test_credentials_mapping(testdir, credentials_file):
    """ Credentials available """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_generated_credentials(credentials_mapping, skin, variables):
            assert variables['skins'][skin]['credentials']\
                ['Administrator']['username'] == "admin1"
            assert variables['skins'][skin]['credentials']\
                ['Administrator']['password'] == "asdf1"
            assert credentials_mapping['Administrator']['username'] == "admin1"
            assert credentials_mapping['Administrator']['password'] == "asdf1"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_generated_credentials PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize('credentials_file', ['credentials.json',
                                              'credentials.yml'])
def test_skin_base_url(testdir, credentials_file):
    """ Skin base url """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_generated_skin_base_url_dummy(skin_base_url, skin, variables):
            assert variables['skins'][skin]\
                ['base_url'] == 'https://skin1-coolsite.com'
            assert skin_base_url == "https://skin1-coolsite.com"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_generated_skin_base_url_dummy PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
