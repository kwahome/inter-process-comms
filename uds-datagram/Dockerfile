ARG IMAGE_VERSION
FROM python:${IMAGE_VERSION}
ARG INSTALL_ASYNC

COPY . /usr/src/app
WORKDIR /usr/src/app


RUN echo "INSTALL_ASYNC is" 
RUN echo "$INSTALL_ASYNC"
RUN if [ "$INSTALL_ASYNC" = "yes" ] ; then pip install aiohttp cchardet aiodns ; else echo "not python3 so wont install aiohttp" ; fi
RUN pip install -r requirements.txt