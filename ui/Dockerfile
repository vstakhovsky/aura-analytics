# ui/Dockerfile

# Use Node 20 on Alpine for a small footprint
FROM node:20-alpine

# App working directory inside the container
WORKDIR /app

# 1) Copy only dependency manifests first to leverage Docker layer cache
#    This will not copy the rest of the source yet.
COPY package*.json ./

# 2) Install dependencies
#    - Prefer npm ci when a lockfile exists (reproducible & faster)
#    - Fallback to npm install when there is no lockfile
RUN if [ -f package-lock.json ]; then \
      npm ci --omit=optional; \
    else \
      npm install --no-audit --no-fund; \
    fi

# 3) Copy the rest of the app sources
COPY . /app

# 4) Ensure Next.js listens on all interfaces inside container
ENV HOST=0.0.0.0

# 5) Expose dev server port
EXPOSE 3000

# 6) Start Next.js dev server and bind to 0.0.0.0 for Docker port mapping
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
