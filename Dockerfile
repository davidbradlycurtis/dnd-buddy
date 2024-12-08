# ****************************************************************************
# Docker Container Build File
# ****************************************************************************
FROM python:3.9.14

ENV QUIET_MODE="True"

COPY [ "dnd-buddy", "/srv/dnd-buddy" ]
RUN [ "pip", "install", "-r", "/srv/dnd-buddy/requirements.txt" ]

WORKDIR "/srv"

ENTRYPOINT [ "/bin/bash" ]
