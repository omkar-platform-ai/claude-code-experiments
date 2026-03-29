# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Setup**: `npm run setup` (installs deps, generates Prisma client, runs migrations)
- **Dev server**: `npm run dev` (Next.js with Turbopack, requires `node-compat.cjs` shim)
- **Build**: `npm run build`
- **Lint**: `npm run lint`
- **Tests**: `npm test` (vitest, runs in watch mode)
- **Single test**: `npx vitest run src/path/to/test.test.ts`
- **DB reset**: `npm run db:reset`
- **Prisma generate** (after schema changes): `npx prisma generate && npx prisma migrate dev`

## Architecture

UIGen is an AI-powered React component generator with live in-browser preview. Users describe components in a chat, and the AI generates/edits files in a virtual file system that renders live in an iframe.

### Core Flow

1. **Chat API** (`src/app/api/chat/route.ts`) — Receives messages + serialized virtual file system, streams AI responses using Vercel AI SDK (`streamText`). The AI has two tools: `str_replace_editor` (create/edit files) and `file_manager` (rename/delete).
2. **Tool calls land on both sides** — Server-side tools modify the `VirtualFileSystem` instance for persistence. Client-side `onToolCall` in `ChatProvider` mirrors changes into the React-managed file system context for live updates.
3. **Preview** (`src/components/preview/PreviewFrame.tsx`) — Transforms all virtual files with Babel (`@babel/standalone`), creates blob URLs, builds an import map, and renders in a sandboxed iframe. Third-party imports resolve via `esm.sh`. Entry point is `/App.jsx` by default.

### Key Abstractions

- **`VirtualFileSystem`** (`src/lib/file-system.ts`) — In-memory tree-based file system. No disk I/O. Supports CRUD, rename, serialize/deserialize, and text editor operations (str_replace, insert). Serialized as JSON to persist in the database.
- **`FileSystemContext`** (`src/lib/contexts/file-system-context.tsx`) — React context wrapping `VirtualFileSystem` with a `refreshTrigger` pattern to force re-renders on mutations.
- **`ChatContext`** (`src/lib/contexts/chat-context.tsx`) — Wraps Vercel AI SDK's `useChat`, wires up tool call handling, and tracks anonymous work.
- **JSX Transformer** (`src/lib/transform/jsx-transformer.ts`) — Babel-based transform that builds import maps with blob URLs, resolves `@/` aliases, handles CSS imports, and creates placeholder modules for missing imports.

### Mock Provider

When `ANTHROPIC_API_KEY` is not set, `src/lib/provider.ts` uses a `MockLanguageModel` that returns static component code (counter/form/card) without calling any API. The model used when the key is present is `claude-haiku-4-5`.

### Data Model

SQLite via Prisma. The database schema is defined in `prisma/schema.prisma`. Two models: `User` (email/password auth with bcrypt + JWT via `jose`) and `Project` (stores serialized messages and file system data as JSON strings). Prisma client outputs to `src/generated/prisma`. The database file is `prisma/dev.db`.

### Layout

The app is a two-panel layout (`src/app/main-content.tsx`): chat on the left, preview/code on the right with tab switching. The code view has a nested resizable split with file tree + Monaco editor. UI components use shadcn/ui (new-york style).

### Routing

- `/` — Anonymous users see the main UI; authenticated users redirect to their latest project
- `/[projectId]` — Project-specific page (authenticated only)
- Auth uses cookie-based JWT sessions (`src/lib/auth.ts`, `src/middleware.ts`)

### Path Alias

`@/*` maps to `./src/*` (configured in tsconfig.json and used throughout).
