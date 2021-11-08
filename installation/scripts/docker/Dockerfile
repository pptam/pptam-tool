FROM jupyter/datascience-notebook
        
USER root

RUN apt-get update 
RUN apt-get install -y libpq-dev
RUN echo 'install.packages(c("RSQLite"),repos="http://cran.us.r-project.org", dependencies=TRUE)' > /tmp/packages.R && Rscript /tmp/packages.R
