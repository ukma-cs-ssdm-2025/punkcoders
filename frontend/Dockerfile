# Use a Node.js image as the base
FROM node:20-alpine 

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