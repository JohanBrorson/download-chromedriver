import pytest
from unittest import mock
from download_chromedriver import get_current_platform


@mock.patch('platform.system', mock.MagicMock(return_value="Linux"))
def test_get_current_platform_linux():
    current_platform = get_current_platform()
    assert current_platform == 'linux64'


@mock.patch('platform.system', mock.MagicMock(return_value="Windows"))
def test_get_current_platform_windows():
    current_platform = get_current_platform()
    assert current_platform == 'win32'


@mock.patch('platform.system', mock.MagicMock(return_value="Darwin"))
def test_get_current_platform_macos():
    current_platform = get_current_platform()
    assert current_platform == 'mac64'


@mock.patch('platform.system', mock.MagicMock(return_value="Unsupported"))
def test_get_current_platform_unsupported():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_current_platform()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
