# ****************************************************************************
# Docker Container Build File
# ****************************************************************************
FROM python:3.9.14

ENV DISCORD_TOKEN="MTA5NjUyNDI0MjkyMjc3NDYyMA.GM5YQb.TzXvS5UF0iRZisMi0Kvll_robV0S0io8a-CQDw"
ENV QUIET_MODE="True"

COPY [ "dnd-buddy", "/srv/dnd-buddy" ]
RUN [ "pip", "install", "-r", "/srv/dnd-buddy/requirements.txt" ]

WORKDIR "/srv"

ENTRYPOINT [ "/bin/bash" ]
