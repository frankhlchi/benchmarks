import time
import docker
client = docker.from_env()


class Dockering:
    def __init__(self, config):
        self.image = config['image']
        self.ports = config['ports']
        self.env = config.get('envs')
        self.volumes = config.get('volumes')
        if self.volumes:
            for key, val in self.volumes.items():
                self.volumes[key] = {'bind': val, 'mode': 'ro'}
        client.images.pull(self.image)

    def up(self):
        self.container = client.containers.create(
            self.image, auto_remove=True,
            volumes=self.volumes, ports=self.ports, name='server', environment=self.env)
        self.container.start()
        if not self.container.logs():
            print('    Waiting for container to come up...')
            time.sleep(1)
        # delay giving for services inside the container to come up
        time.sleep(3)

    def down(self):
        self.container.remove(v=True, force=True)

    def __enter__(self):
        self.up()

    def __exit__(self, type, value, traceback):
        self.down()


if __name__ == '__main__':
    d = Dockering('tensorwerk/raibenchmarks:flask-optim-cpu')
    d.up()
    d.down()
"""
docker run --read-only -v /home/hhsecond/mypro/benchmarks/assets:/root/data \
    --read-only -v /home/hhsecond/mypro/benchmarks/experiments/_tensorflow/_flask:/root \
    -p 8000:8000 --name server --rm tensorwerk/raibenchmarks:flask-optim-cpu
"""
