import docker
import pytest

testinfra_hosts = ['test_container']

@pytest.fixture(scope="module", autouse=True)
def container(client, image):
    container = client.containers.run(
        image.id,
        name="test_container",
        detach=True,
        environment=[
            'MYSQL_USER=test_user',
            'MYSQL_DATABASE=test_db',
            'MYSQL_PASSWORD=test_password',
            'BACKUP_TIME=1 2 3 4 5',
            'CLEANUP_OLDER_THAN=100'
        ]
    )
    yield container
    container.remove(force=True)

def test_environment(Command):
    env = Command.check_output("env")
    assert "MYSQL_USER=test_user" in env
    assert "MYSQL_DATABASE=test_db" in env
    assert "MYSQL_PASSWORD=test_password" in env
    assert "BACKUP_TIME=1 2 3 4 5" in env
    assert "CLEANUP_OLDER_THAN=100" in env

def test_crontab(Command):
    assert Command.check_output("crontab -l") == """MYSQL_USER=test_user
MYSQL_DATABASE=test_db
MYSQL_PASSWORD=test_password
CLEANUP_OLDER_THAN=100
1 2 3 4 5 backup > /backup.log"""
