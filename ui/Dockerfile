# ui/Dockerfile
FROM node:20-alpine

# Use development env by default (tweak in compose if needed)
ENV NODE_ENV=development

# App working directory
WORKDIR /app

# 1) Install deps: prefer npm ci when lockfile exists, otherwise fallback to npm install
COPY package*.json ./
RUN npm ci --omit=optional || npm install --no-audit --no-fund

# 2) Copy the rest of the app
COPY . /app

# 3) Next.js must listen on all interfaces inside container
ENV HOST=0.0.0.0
EXPOSE 3000

# 4) Start dev server (bind to 0.0.0.0 so port mapping works)
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0", "-p", "3000"]
