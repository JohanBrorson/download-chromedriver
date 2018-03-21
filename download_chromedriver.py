"""
Download ChromeDriver
"""

import logging
import logging.config
import os
import shutil
import sys
import urllib
import urllib2
import urlparse
import zipfile


DOWNLOAD_BASE_URL = 'https://chromedriver.storage.googleapis.com'
CHROMEDRIVER_PLATFORMS = ['linux64', 'mac64', 'win32']

logging.config.fileConfig(os.path.join(sys.path[0], 'logging.conf'))
LOGGER = logging.getLogger('console')


def main():
    """"Main function"""
    version = get_latest_release()
    for platform in CHROMEDRIVER_PLATFORMS:
        url = get_chromedriver_url(version, platform)
        zip_file = get_chromedriver_filename(platform)
        download_file(url, zip_file)
        target = get_target_directory(version, platform)
        unzip(zip_file, target)
        remove_file(zip_file)


def get_latest_release():
    """"Gets the lastest ChromeDriver version"""
    url = get_url("LATEST_RELEASE")
    request = open_url(url)
    version = request.read().rstrip()
    LOGGER.debug("Latest release: %s", version)
    return version


def get_chromedriver_url(version, platform):
    """Gets the ChromeDriver URL"""
    path = '{}/{}'.format(version, get_chromedriver_filename(platform))
    url = get_url(path)
    LOGGER.info(url)
    return url


def get_chromedriver_filename(platform):
    """Gets the filename of the remote ChromeDriver"""
    return 'chromedriver_{}.zip'.format(platform)


def get_url(path):
    """Gets the URL by joining the specified path with the base URL"""
    return urlparse.urljoin(DOWNLOAD_BASE_URL, path)


def open_url(source):
    """Opens the URL for reading"""
    try:
        LOGGER.debug("Open URL: %s", source)
        return urllib2.urlopen(source)
    except urllib2.URLError, error:
        LOGGER.error('Fail to download file, exception: %s', error.reason)
        sys.exit(1)


def download_file(source, destination):
    """Downloads file"""
    urllib.urlretrieve(source, destination)


def unzip(archive, target):
    """Extracts an archive to target destination"""
    LOGGER.debug('Unzip %s to %s', archive, target)
    remove_directory(target)
    create_directory(target)
    zip_ref = zipfile.ZipFile(archive, 'r')
    zip_ref.extractall(target)
    zip_ref.close()


def get_target_directory(version, platform):
    """Gets the path to the directory where ChromeDriver extracted to"""
    return os.path.realpath(os.path.join('chromedriver', version, platform))


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
