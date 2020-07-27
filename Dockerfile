FROM python:3.6-alpine

# install git
RUN apk update && apk add git

# upgrade pip and install jsonpath-rw from git (implements .update()) then install jsonpath-rw-ext
RUN pip install --upgrade pip && pip install git+https://github.com/kennknowles/python-jsonpath-rw && pip install jsonpath-rw-ext

COPY beamr_args.py /usr/local/bin/

WORKDIR /beamr_args

ENTRYPOINT ["/usr/local/bin/python", "/usr/local/bin/beamr_args.py"]
