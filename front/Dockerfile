# Use the official Node.js image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the React app code into the container
COPY . .

# Build the app
# RUN npm run build