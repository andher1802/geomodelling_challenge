FROM jupyter/minimal-notebook:latest

RUN pip install dask-labextension

EXPOSE 8787
EXPOSE 8786
EXPOSE 8000
EXPOSE 8888

ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]

ARG conda_env=geo_pipeline
ARG py_ver=3.8

USER root
RUN sudo apt-get update

COPY ./sentinel_data ./sentinel_data
COPY ./main_pipeline  ./main_pipeline

COPY --chown=${NB_UID}:${NB_GID} environment.yml /home/$NB_USER/tmp/
RUN cd /home/$NB_USER/tmp/ && \
     conda env create -p $CONDA_DIR/envs/$conda_env -f environment.yml && \
     conda clean --all -f -y

RUN $CONDA_DIR/envs/${conda_env}/bin/python -m ipykernel install --user --name=${conda_env} && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

ENV PATH $CONDA_DIR/envs/${conda_env}/bin:$PATH
ENV CONDA_DEFAULT_ENV ${conda_env}
ENV STAC_API_URL "https://earth-search.aws.element84.com/v0"

COPY . .
