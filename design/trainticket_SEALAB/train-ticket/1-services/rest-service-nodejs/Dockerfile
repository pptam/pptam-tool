FROM node


RUN mkdir -p /app
WORKDIR /app

ADD ./node_modules /app/node_modules
ADD ./package.json /app/
# RUN npm install

ADD ./rest-service-nodejs.js /app/
CMD [ "npm", "start" ]

EXPOSE 16100