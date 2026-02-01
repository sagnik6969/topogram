# Build stage
FROM node:22-alpine AS builder

WORKDIR /app

# Copy configuration files
COPY package.json package-lock.json .npmrc ./

# Install dependencies
RUN npm ci

# Copy source code
COPY tsconfig.json ./
COPY src ./src

# Build the application
RUN npm run build

# Production stage
FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

# Copy configuration files
COPY package.json package-lock.json .npmrc ./

# Install only production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Start server
CMD ["npm", "start"]
