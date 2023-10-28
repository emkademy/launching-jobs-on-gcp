# Launching Jobs on GCP

This repository is created to make it easier to launch jobs on GCP using Instance Groups.

## Why instance groups?

- Flexibility for specifying VM specifications
- Being able to use SPOT machines (which is not possible to do on some GCP services)

## How to launch a job?

Before you can launch a job on GCP there are a few things you need to do:

### Prerequisites

- [docker](https://docs.docker.com/engine/install/) >= 24.0.6 (the repo might work with earlier versions as well, however they are not tested)
- [gsutils](https://cloud.google.com/storage/docs/gsutil_install)

### Building the docker image

Run:

```sh
make build
```

### Creating a config file

### Modifying the startup script

Modify [the startup script](./scripts/task_runner_startup_script.sh) based on your needs. This is the script that will be ran on every VM when you launch a job on GCP.

### Launching a job

Run:

```sh
make launch-job OVERRIDES='+configs/examples=simple-vm'
```

**NOTE:** In order to see available commands you can run `make` without any target.
