# ui/Dockerfile  (English comments)
FROM node:20-alpine

# Make the dev server bind to all interfaces and be deterministic in CI
ENV NODE_ENV=development \
    HOST=0.0.0.0 \
    PORT=3000 \
    NEXT_TELEMETRY_DISABLED=1

# App working directory
WORKDIR /app

# Install deps first (use lockfile if present)
COPY package*.json ./
RUN npm ci --omit=optional || npm install --no-audit --no-fund

# Copy the rest of the app
COPY . .

# Expose Next dev port
EXPOSE 3000

# Start Next.js dev server listening on all interfaces
CMD ["sh","-lc","npm run dev -- -H $HOST -p $PORT"]
