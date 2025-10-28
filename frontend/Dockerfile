# Use a Node.js image as the base
FROM node:20-alpine AS development

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files and install
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy the rest of the application code
COPY . .

# Vite's default port
EXPOSE 5173 

# Command to start the development server
# --host 0.0.0.0 is crucial for Docker access (as discussed previously)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ----- Stage 2: Build Stage -----
# Render doesn't make env vars available at build
ARG VITE_API_URL_ARG="https://https://clickeat-backend.onrender.com/api/v0/" 
ENV VITE_API_URL=$VITE_API_URL_ARG
RUN echo "VITE_API_URL during build is: $VITE_API_URL"
# We'll re-use the "development" stage to build our final files
FROM development AS build
# This creates the optimized 'dist' folder
RUN npm run build

# ----- Stage 3: Production Stage -----
# This is the final stage, which Render will build by default
FROM nginx:1.25-alpine AS production
# Copy the built static files from Stage 2
COPY --from=build /app/dist /usr/share/nginx/html
# Copy the Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]