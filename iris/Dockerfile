ARG IRIS_IMAGE=containers.intersystems.com/intersystems/irishealth-community:latest-cd
FROM ${IRIS_IMAGE}

USER root
RUN mkdir -p /opt/repro && chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/repro
USER ${ISC_PACKAGE_MGRUSER}

WORKDIR /opt/repro
COPY --chown=${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} src/ /opt/repro/src/
COPY --chown=${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} iris.script merge.cpf /opt/repro/

# Build-time setup: namespace, code load, credentials. No runtime docker exec needed.
RUN iris start IRIS && \
    iris merge IRIS /opt/repro/merge.cpf && \
    iris session IRIS < /opt/repro/iris.script && \
    iris stop IRIS quietly
