"""
Download ChromeDriver
"""

import argparse
import logging
import logging.config
import os
import platform
import shutil
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import urllib.parse
import zipfile


DOWNLOAD_BASE_URL = 'https://chromedriver.storage.googleapis.com'
PLATFORM_WINDOWS = 'win32'
PLATFORM_LINUX = 'linux64'
PLATFORM_MACOS = 'mac64'

logging.config.fileConfig(os.path.join(sys.path[0], 'logging.conf'))
LOGGER = logging.getLogger('console')


def main():
    """"Main function"""
    parser = argparse.ArgumentParser(
        description=('Script for downloading and extracting ChromeDriver'))
    parser.add_argument('-a', '--all',
                        dest='should_download_all',
                        action='store_true',
                        required=False,
                        default=False,
                        help='download ChromeDriver for all platforms')

    args = parser.parse_args()
    if args.should_download_all:
        LOGGER.debug("Download ChromeDriver for all platforms")
        platforms = [PLATFORM_LINUX,
                     PLATFORM_MACOS,
                     PLATFORM_WINDOWS]
    else:
        LOGGER.debug("Download ChromeDriver for current platform")
        platforms = [get_current_platform()]

    version = get_latest_release()
    for platform_name in platforms:
        url = get_chromedriver_url(version, platform_name)
        zip_file = get_chromedriver_filename(platform_name)
        download_file(url, zip_file)
        target = get_target_directory(version, platform_name)
        unzip(zip_file, target)
        remove_file(zip_file)


def get_current_platform():
    """Gets this machines operating system"""
    if is_windows():
        return PLATFORM_WINDOWS
    elif is_linux():
        return PLATFORM_LINUX
    elif is_macos():
        return PLATFORM_MACOS
    else:
        LOGGER.error("Unsupported operating system")
        sys.exit(2)


def is_linux():
    """Checks if the operating system is Linux"""
    return 'linux' in str(platform.system()).lower()


def is_macos():
    """Checks if the operating system is macOS"""
    return 'darwin' in str(platform.system()).lower()


def is_windows():
    """Checks if the operating system is Windows"""
    return 'windows' in str(platform.system()).lower()


def get_latest_release():
    """"Gets the lastest ChromeDriver version"""
    url = get_url("LATEST_RELEASE")
    request = open_url(url)
    version = request.read().rstrip()
    LOGGER.debug("Latest release: %s", version)
    return version


def get_chromedriver_url(version, platform_name):
    """Gets the ChromeDriver URL"""
    path = '{}/{}'.format(version, get_chromedriver_filename(platform_name))
    url = get_url(path)
    LOGGER.info(url)
    return url


def get_chromedriver_filename(platform_name):
    """Gets the filename of the remote ChromeDriver"""
    return 'chromedriver_{}.zip'.format(platform_name)


def get_url(path):
    """Gets the URL by joining the specified path with the base URL"""
    return urllib.parse.urljoin(DOWNLOAD_BASE_URL, path)


def open_url(source):
    """Opens the URL for reading"""
    try:
        LOGGER.debug("Open URL: %s", source)
        return urllib.request.urlopen(source)
    except urllib.error.URLError as error:
        LOGGER.error('Fail to download file, exception: %s', error.reason)
        sys.exit(1)


def download_file(source, destination):
    """Downloads file"""
    urllib.request.urlretrieve(source, destination)


def unzip(archive, target):
    """Extracts an archive to target destination"""
    LOGGER.debug('Unzip %s to %s', archive, target)
    remove_directory(target)
    create_directory(target)
    zip_ref = zipfile.ZipFile(archive, 'r')
    zip_ref.extractall(target)
    zip_ref.close()


def get_target_directory(version, platform_name):
    """Gets the path to the directory where ChromeDriver extracted to"""
    return os.path.realpath(os.path.join(
        'chromedriver', version, platform_name))


def create_directory(directory):
    """Creates the specified directory, unless it already exists"""
    if not os.path.exists(directory):
        LOGGER.debug("Create directory: %s", directory)
        os.makedirs(directory)


def remove_directory(directory, ignore_errors=False):
    """Removes the specified directory"""
    if os.path.isdir(directory):
        LOGGER.debug("Delete directory: %s", directory)
        shutil.rmtree(directory, ignore_errors)


def remove_file(path):
    """Removes the specified file"""
    if os.path.isfile(path):
        LOGGER.debug("Remove %s", path)
        os.remove(path)


if __name__ == '__main__':
    main()
