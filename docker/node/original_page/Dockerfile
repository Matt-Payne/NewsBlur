FROM node:14.4.0
WORKDIR /usr/src/app
COPY ./node /usr/src/app/
RUN npm install
ENV NODE_ENV=development
CMD ["node", "original_page.js" ]