FROM node:22-alpine AS base-image

ARG DEV="false"

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* .npmrc* ./

# Install dependencies
RUN if [ "$DEV" = "true" ]; then \
        npm ci --include=dev; \
    else \
        npm ci --omit=dev; \
    fi

# Copy application code
COPY . .

# Create user
RUN addgroup -S app && \
    adduser -S app

FROM base-image AS local-image

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM base-image AS release-image

EXPOSE 5173

CMD ["npm", "run", "start"]