# Architecture

This document describes a target design of an application.

## 1. Design requirements

### Functional requirements

- Users can register with a valid email and matching passwords (minimum 8 characters), log in, and retrieve their own profile.
- Authenticated users can browse flashcards, filter by word, meaning, part of speech, and their own rating, sort by word, and paginate results.
- Authenticated users can create or change their rating for a flashcard.
- Authenticated users can request a learning session of up to 10 flashcards, selected by rating priority: hard, medium, easy, then unrated.
- Authenticated users can learn with AI powered Tutor through chat view. 
- AI powered Tutor has knowledge about Flashcards ratings that user left and uses this data in chat.
- The AI-powered Tutor automatically creates flashcards from conversation when appropriate. AI-generated flashcards are shared in the flashcard catalog and marked as AI-generated.

### Non-functional requirements

- Reliability:
    * `GET /healthcheck` returns HTTP 503 when the database check fails.
- Security:
    * Protect user data and state-changing operations against unauthorized access and cross-site request forgery.
    * Restrict cross-origin browser access to explicitly trusted frontend origins.
    * Encrypt HTTP API and WebSocket traffic in deployed environments.
    * Include automated vulnerability checks in the delivery pipeline.
- Privacy:
    * Inform users about external AI-provider processing when they first enter tutor chat.
    * Minimize personal data sent to external services and define retention expectations.

## 2. Data model

### Users (`users`)

| Column | Database type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE |
| `password_hash` | VARCHAR(200) | NOT NULL |

### Flashcards (`flashcards`)

| Column | Database type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `word` | VARCHAR(120) | NOT NULL |
| `meaning` | VARCHAR(500) | NOT NULL |
| `part_of_speech` | ENUM `part_of_speech_enum` | NOT NULL |
| `example` | VARCHAR(500) | NULL |
| `is_ai_generated` | BOOLEAN | NOT NULL; default `false` |

Flashcards are shared catalog entries and are not owned by individual users. The server sets `is_ai_generated` to `true` when the tutor creates a card; clients cannot set or change this flag. User ratings remain separate and user-specific in `user_ratings`.

`part_of_speech_enum` values (database label → API value):

| Database enum value | API value |
|---|---|
| `NOUN` | `noun` |
| `VERB` | `verb` |
| `ADJECTIVE` | `adjective` |
| `ADVERB` | `adverb` |
| `PRONOUN` | `pronoun` |
| `PREPOSITION` | `preposition` |
| `CONJUNCTION` | `conjunction` |
| `INTERJECTION` | `interjection` |
| `NUMERAL` | `numeral` |
| `PROPER_NOUN` | `proper noun` |

### User ratings (`user_ratings`)

| Column | Database type | Constraints |
|---|---|---|
| `user_id` | UUID | PK, FK → `users.id` |
| `flashcard_id` | UUID | PK, FK → `flashcards.id` |
| `rating` | ENUM `rating_enum` | NOT NULL |

The composite primary key `(user_id, flashcard_id)` allows at most one rating per user for each flashcard.

`rating_enum` values (database enum label → API value):

| Database enum value | API value |
|---|---|
| `EASY` | `1` |
| `MEDIUM` | `2` |
| `HARD` | `3` |

The flashcard-list `rating` filter additionally accepts `0` to mean not rated; `0` is a filter option and is not stored in `user_ratings`.

### Conversations (`conversations`)

| Column | Database type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `user_id` | UUID | NOT NULL, FK → `users.id` |
| `title` | VARCHAR(200) | NULL |
| `created_at` | TIMESTAMPTZ | NOT NULL |
| `updated_at` | TIMESTAMPTZ | NOT NULL |

Each conversation belongs to one user.

### Messages (`messages`)

| Column | Database type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `conversation_id` | UUID | NOT NULL, FK → `conversations.id` |
| `sequence_no` | INTEGER | NOT NULL; unique with `conversation_id` |
| `role` | ENUM `message_role_enum` | NOT NULL |
| `content` | TEXT | NOT NULL |
| `created_at` | TIMESTAMPTZ | NOT NULL |

`message_role_enum` values:

| Enum value | Meaning |
|---|---|
| `USER` | Message written by the user |
| `ASSISTANT` | Response written by the AI tutor |

`sequence_no` provides deterministic message ordering within a conversation and has a unique constraint together with `conversation_id`. Deleting a conversation cascades to its messages.

### Relationships

The diagram shows the relationships between the data models. In particular, `user_ratings.user_id` and `conversations.user_id` reference `users.id`, and `messages.conversation_id` references `conversations.id`.

```mermaid
erDiagram
    USERS ||--o{ USER_RATINGS : gives
    FLASHCARDS ||--o{ USER_RATINGS : receives
    USERS ||--o{ CONVERSATIONS : owns
    CONVERSATIONS ||--o{ MESSAGES : contains

    USERS {
        UUID id PK
        VARCHAR_120 email UK
        VARCHAR_200 password_hash
    }
    FLASHCARDS {
        UUID id PK
        VARCHAR_120 word
        VARCHAR_500 meaning
        part_of_speech_enum part_of_speech
        VARCHAR_500 example "nullable"
        BOOLEAN is_ai_generated
    }
    USER_RATINGS {
        UUID user_id PK, FK
        UUID flashcard_id PK, FK
        rating_enum rating
    }
    CONVERSATIONS {
        UUID id PK
        UUID user_id FK
        VARCHAR_200 title
        TIMESTAMPTZ created_at
        TIMESTAMPTZ updated_at
    }
    MESSAGES {
        UUID id PK
        UUID conversation_id FK
        INTEGER sequence_no
        message_role_enum role
        TEXT content
        TIMESTAMPTZ created_at
    }
```

## 3. API design

HTTP paths below are relative to the API base URL configured by `VITE_API_URL`. HTTP request and response bodies use JSON unless stated otherwise. The chat message transport uses a WebSocket JSON event protocol described separately.

### Healthcheck Service

The healthcheck endpoint is public and verifies database connectivity.

| Method and path | Authentication | Request | Success response |
|---|---|---|---|
| `GET /healthcheck` | Public | None | `200`; `{"status":"healthy"}` |

If the database cannot be reached, it returns `503` with `{"detail":"Database unavailable"}`.

### Authentication Service

Registration and login are public HTTP endpoints. A successful login sets a signed access JWT with a 15-minute lifetime in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie scoped to `/`, with no `Domain` attribute and a matching cookie expiry; the token is not returned to frontend JavaScript. The same cookie authenticates protected HTTPS endpoints and WSS handshakes. For each protected HTTP request and WSS handshake, the API validates the JWT signature, allowed signing algorithm, issuer, audience, and expiry. The JWT `sub` claim contains the authenticated user's UUID; the API resolves it to a user record and rejects the credential if that user does not exist. Resource authorization compares the authenticated user's ID with the owner ID of the requested resource. Logout clears the browser cookie; an issued JWT remains valid until expiry, including on already-established WebSocket connections.

Unsafe HTTP requests require a valid CSRF token in the `X-CSRF-Token` header and a trusted `Origin`. Credentialed CORS requests are allowed only from explicitly configured frontend origins.

| Method and path | Authentication | Request | Success response |
|---|---|---|---|
| `GET /auth/csrf` | Public | None | `200`; `{"csrf_token":"<signed-csrf-token>"}` |
| `POST /auth/register` | Public; CSRF token required | JSON: `{"email":"learner@example.com","password_1":"...","password_2":"..."}` and `X-CSRF-Token` header | `201`; `{"id":"<uuid>","email":"learner@example.com"}` |
| `POST /auth/login` | Public; CSRF token required | Form URL-encoded OAuth2 fields `username` (email) and `password`, plus `X-CSRF-Token` header | `200`; `{"id":"<uuid>","email":"learner@example.com"}` and `Set-Cookie` for the access JWT |
| `POST /auth/logout` | Access JWT cookie; CSRF token required | `X-CSRF-Token` header | `204`; clears the cookie |
| `GET /auth/me` | Access JWT cookie required | None | `200`; `{"id":"<uuid>","email":"learner@example.com"}` |

Invalid input is rejected with `422`; missing, expired, or invalid JWTs produce `401`. Invalid/missing CSRF tokens or untrusted origins are rejected with `403`. Registration also returns `400` if the email already exists or the passwords do not match. `/auth/me` returns `404` if the JWT refers to a user that no longer exists.

`GET /auth/csrf` issues a cryptographically signed CSRF token for the frontend to retain in memory and send as `X-CSRF-Token`; the frontend never reads the JWT cookie. The backend validates the token and checks `Origin` for unsafe HTTP requests. Login and registration are also CSRF-protected to prevent login CSRF.

### Flashcards Service

All flashcard endpoints require the access JWT cookie. State-changing requests also require a valid CSRF token in `X-CSRF-Token`.

| Method and path | Request | Success response |
|---|---|---|
| `GET /flashcards/` | Query parameters below | `200`; paginated flashcard response below |
| `POST /flashcards/{flashcard_id}` | JSON: `{"rating":1}` (`1` easy, `2` medium, `3` hard) | `201`; `{"rating_changed":true}` or `{"rating_changed":false}` |
| `GET /flashcards/learning_session/` | None | `200`; array of flashcards, possibly empty |

#### Flashcard-list query parameters

| Parameter | Type and behavior |
|---|---|
| `page` | Integer, default `1`, minimum `1` |
| `page_size` | Integer, default `10`, range `1`–`50` |
| `order_by` | Optional `word` or `-word` (ascending or descending); defaults to `word`. Ties are ordered by flashcard ID. |
| `word`, `meaning` | Optional filters |
| `part_of_speech` | Optional `part_of_speech_enum` value |
| `rating` | Optional integer: `0` not rated, `1` easy, `2` medium, `3` hard |

`GET /flashcards/` paginated response:

```json
{
  "items": [
    {
      "id": "<uuid>",
      "word": "example",
      "meaning": "przykład",
      "part_of_speech": "noun",
      "example": "This is an example.",
      "rating": 1,
      "is_ai_generated": false
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1,
  "has_next": false,
  "has_previous": false
}
```

`example` and `rating` may be `null`; `rating` is the requesting user's rating. `is_ai_generated` indicates whether the card was created by the tutor. An empty result has an empty `items` array and zero `total`/`total_pages`.

Invalid input is rejected with `422`; missing or invalid credentials produce `401`. Other failure responses are not exhaustively specified here.

### Conversations Service

These endpoints manage conversations owned by the authenticated user. All endpoints require the access JWT cookie and only expose conversations belonging to that user. `POST`also requires a valid CSRF token in `X-CSRF-Token`.

| Method and path | Parameters / example request | Example success response |
|---|---|---|
| `GET /conversations` | Query: `page` (default `1`), `page_size` (default `20`, maximum `100`). Ordered by most recently updated first, with conversation ID as a tie-breaker. Example: `/conversations?page=1&page_size=20` | `200`; paginated conversation summaries (example below) |
| `POST /conversations` | JSON: `{"title":"English practice"}`; `title` may be omitted or `null` | `201`; created conversation (example below) |
| `GET /conversations/{conversation_id}` | Path: `conversation_id` UUID. Example: `/conversations/550e8400-e29b-41d4-a716-446655440000` | `200`; conversation object |

Paginated list response:

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "English practice",
      "created_at": "2026-10-24T08:30:00Z",
      "updated_at": "2026-10-24T08:35:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1,
  "has_next": false,
  "has_previous": false
}
```

Create and retrieve response:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "English practice",
  "created_at": "2026-10-24T08:30:00Z",
  "updated_at": "2026-10-24T08:30:00Z"
}
```

### Messages Service

Message history is fetched over HTTP using the JWT cookie. Sending a message and receiving the AI response use a WebSocket connection scoped to one conversation. The browser automatically sends the same JWT cookie during the handshake. The server validates the JWT and trusted `Origin` before accepting the connection; it then assigns `sequence_no`, `role`, and `created_at`. Clients cannot choose a role or write directly as the assistant. Logging out clears the browser cookie but does not invalidate an already-issued JWT. Established WebSocket connections are closed when their JWT expires.

Users cannot rename or delete conversations. Conversation and message records are retained indefinitely. Before the first tutor chat, the frontend displays information that messages and relevant user-rating data are sent to an external AI provider. The provider must not use submitted data to train models and may retain it only for limited service operation or abuse prevention. For each request, the backend sends only the relevant conversation context and the minimum rating information needed to answer; the provider does not receive the user's full rating set by default.

| Method and path | Parameters / example request | Example success response |
|---|---|---|
| `GET /conversations/{conversation_id}/messages` | Path: `conversation_id` UUID. Query: `page` (default `1`), `page_size` (default `50`, maximum `100`). Example: `/conversations/550e8400-e29b-41d4-a716-446655440000/messages?page=1&page_size=50`. Results ordered by `sequence_no` ascending. | `200`; paginated message list (example below) |

Paginated message-list response:

```json
{
  "items": [
    {
      "id": "7d444840-9dc0-11d1-b245-5ffdce74fad2",
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "sequence_no": 1,
      "role": "USER",
      "content": "Can you explain the past tense?",
      "created_at": "2026-10-24T08:35:00Z"
    },
    {
      "id": "7d444840-9dc0-11d1-b245-5ffdce74fad3",
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "sequence_no": 2,
      "role": "ASSISTANT",
      "content": "The past tense describes an action that happened before now.",
      "created_at": "2026-10-24T08:35:02Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 50,
  "total_pages": 1,
  "has_next": false,
  "has_previous": false
}
```

#### WebSocket message exchange

The client connects to the conversation over WSS. Before accepting the connection, the server authenticates the user, validates the trusted origin, and verifies conversation ownership. The same JWT cookie is used for HTTP and WebSocket authentication; it is not sent in the URL.

The client sends chat messages over the connection. Only one turn may be active per conversation: the client disables message entry while waiting for a response, and the server enforces sequential processing. The server persists messages, provides the AI model with relevant conversation context and the minimum relevant rating data, and streams responses back to the client. The tutor may use restricted backend capabilities to read the authenticated user's ratings and create validated, shared AI-generated flashcards. Configurable connection, message, rate, and timeout controls protect availability and manage provider usage. Failures are surfaced to the client, and completed assistant responses are persisted. If generation fails or the client disconnects, the user message is retained and generation is cancelled; the user can retry the AI response.

For HTTP conversation and message-history endpoints, invalid input returns `422`, unauthenticated requests return `401`, a missing resource or a resource owned by another user returns `404`, and an invalid CSRF token or untrusted origin returns `403`. WebSocket authentication, origin, and ownership failures are rejected during the handshake; invalid events produce an error event and close the socket.

## 4. High-level system architecture

```mermaid
flowchart TD
    User[User]

    subgraph Client["Client"]
        Browser[Web browser<br/>React SPA]
    end

    subgraph App["Application tier: FastAPI"]
        Auth[Authentication service]
        Flashcards[Flashcards service]
        Conversations[Conversations service]
        Messages[Messages service]
        Health[Healthcheck service]
    end

    subgraph LLM["LLM tier"]
        Provider[External LLM provider API]
        Model[Hosted language model]
        Provider -->|runs inference with| Model
    end

    subgraph DB["Database tier"]
        Users[(users)]
        FlashcardRows[(flashcards)]
        Ratings[(user_ratings)]
        ConversationRows[(conversations)]
        MessageRows[(messages)]
    end

    User -->|uses| Browser
    Browser -->|registration, login, profile| Auth
    Browser -->|flashcard operations| Flashcards
    Browser -->|conversation operations| Conversations
    Browser -->|chat and message history| Messages
    Browser -->|health status| Health
    Auth -->|read/write account data| Users
    Flashcards -->|read/write cards| FlashcardRows
    Flashcards -->|read/write user ratings| Ratings
    Conversations -->|read/write conversations| ConversationRows
    Messages -->|read/write messages| MessageRows
    Messages -->|load conversation context| ConversationRows
    Messages -->|read ratings for tutor context| Ratings
    Health -->|check database connectivity| DB
    Messages -->|prompt and conversation context| Provider
    Provider -->|generated response| Messages
```

This diagram shows the application components and their data dependencies. HTTPS and WSS flows are detailed below.

### HTTPS request flow

```mermaid
sequenceDiagram
    actor User
    participant Browser as Web browser / React SPA
    participant API as FastAPI HTTP API
    participant Security as Request security
    participant Service as Feature service
    participant DB as PostgreSQL

    Browser->>API: GET /auth/csrf over HTTPS
    API-->>Browser: Signed CSRF token
    User->>Browser: Submit credentials
    Browser->>API: Submit login with CSRF header and Origin
    API->>Security: Validate request Origin and CSRF token
    Security-->>API: Request allowed
    API->>Service: Authenticate credentials
    Service->>DB: Find user and verify password hash
    DB-->>Service: User record
    Service-->>API: Authenticated user
    API-->>Browser: Return user profile and set secure HttpOnly JWT cookie
    Browser->>API: Send HTTPS request with cookie and Origin
    API->>Security: Apply CORS and validate cookie Origin and CSRF token
    Security-->>API: Request allowed
    API->>Service: Execute authorized operation
    Service->>DB: Access application data
    DB-->>Service: Query result
    Service-->>API: Response data
    API-->>Browser: JSON response
```

### WSS chat flow

```mermaid
sequenceDiagram
    actor User
    participant Browser as Web browser / React SPA
    participant WS as FastAPI WebSocket endpoint
    participant Auth as Authentication and authorization
    participant Messages as Messages service
    participant DB as PostgreSQL
    participant LLM as External LLM provider

    User->>Browser: Send chat message
    Browser->>WS: Open WSS with HttpOnly cookie and Origin
    WS->>Auth: Validate JWT cookie and trusted Origin
    Auth->>DB: Verify user owns conversation
    DB-->>Auth: Ownership confirmed
    Auth-->>WS: Authorize connection
    WS-->>Browser: WebSocket accepted
    Browser->>WS: Send message.create event
    WS->>Messages: Validate and handle message
    Messages->>DB: Save user message and load history and ratings
    DB-->>Messages: Context and assigned sequence number
    Messages->>Messages: Build prompt and select tools
    Messages->>LLM: Send prompt and conversation context
    LLM-->>Messages: Stream generated tokens
    Messages-->>WS: assistant.delta JSON events
    WS-->>Browser: Stream assistant.delta events
    Messages->>DB: Persist completed assistant message
    DB-->>Messages: Saved assistant message
    Messages-->>WS: assistant.completed event
    WS-->>Browser: Final message with ID and sequence number
```
