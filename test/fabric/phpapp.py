import re
from fabric.api import env, run, hide, task
from envassert import detect, file, group, package, port, process, service, \
    user
from hot.utils.test import get_artifacts, http_check


def apache2_is_responding():
    with hide('running', 'stdout'):
        wget_cmd = (
            "wget --quiet --output-document - --header='Host: example.com' "
            "http://localhost/"
        )
        homepage = run(wget_cmd)
        if re.search('Welcome to example.com', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists("/var/www/vhosts/application/index.php")

    assert port.is_listening(11211), "port 11211/memcached is not listening"
    assert port.is_listening(80), "port 80/memcached is not listening"
    assert port.is_listening(443), "port 443/memcached is not listening"

    assert user.exists("memcache"), "user memcache does not exist"

    assert group.is_exists("memcache"), "group memcache does not exist"

    assert process.is_up("apache2"), "apache2 process is not running"
    assert process.is_up("memcached"), "memcached process is not running"

    assert service.is_enabled("apache2"), "apache2 service is not enabled"
    assert service.is_enabled("memcached"), "memcached service is not enabled"

    assert apache2_is_responding(), \
        "php application did not respond as expected"


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
