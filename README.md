# Beamr Args Converter for Hybrik Jobs

## Simplest usage, use Dockerhub image
Mac:
1) Install [Docker client](https://www.docker.com/products/docker-desktop)
2) pull the dockerhub image: `docker pull hybriksupport/beamr_args`
3) run
  ```
  docker run -v "`pwd`":"`pwd`" -w "`pwd`" beamr_args -c 422UF20.cfg beamr_job.json
  ```



## Requirements (either):
* Local install (harder):
  * Python 3.6+
  * [jsonpath-rw](https://github.com/kennknowles/python-jsonpath-rw) (from git source, not a package manager)
  * [jsonpath-rw-ext](https://pypi.org/project/jsonpath-rw-ext/) (from pip, 1.4.0+)
  * cloned this repository
  * access to a command line

* From Docker (easier):
  * [Docker client](https://www.docker.com/products/docker-desktop) installed
  * cloned this repository
  * access to a command line

## Installation
* Clone this repository from github (navigate your terminal to a save location)
  * `git clone git@github.com:dolby-hybrik-support/beamr_args.git`

### Additional steps for docker:
* Navigate to the cloned repository and build the image
  * `docker build -t beamr_args .`

## Running
* Locally
  * see "usage"

* Docker (mac)
  * Run: ```docker run -v "`pwd`":"`pwd`"" -w "`pwd`" beamr_args -c 422UF20.cfg beamr_job.json```

## Usage
### Example Included
```
beamr_args.py -c 422UF20.cfg beamr_job.json
```


### Full Usage
```
usage: beamr_args.py [-h] -c CONFIG [--verbose] job

Convert a beamr .cfg file into a Hybrik Job

positional arguments:
  job                   input job file

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        beamr.cfg file)
  --verbose             Verbose output
```
