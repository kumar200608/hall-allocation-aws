# Stage 1: Build the React Application
FROM node:20-slim AS build

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source files
COPY . .

# Build application using local vite binary
RUN ./node_modules/.bin/vite build

# Stage 2: Production Nginx Server
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
