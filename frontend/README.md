# Frontend (React SPA)

This frontend is now structured as a React SPA that talks to Django on a separate
domain/service. Django business logic and data models stay unchanged.

## Folder structure

```text
src/
  app/        # app bootstrap + routing
  api/        # shared HTTP client + API config
  pages/      # route-level pages
  features/   # domain-specific modules (auth/farms/weather/etc.)
  shared/     # reusable layout/ui/components
```

## Local setup

1. Install dependencies:

```bash
npm install
```

2. Create env file:

```bash
cp .env.example .env
```

3. Update API URL in `.env` if needed:

```env
VITE_API_BASE_URL=http://localhost:8000
```

4. Start dev server:

```bash
npm run dev
```

## Migration approach

- Build each feature in `src/features/*`.
- Add page-level routes in `src/app/routes.jsx`.
- Replace legacy Django template workflows one module at a time:
  - auth
  - farms/fields
  - soil
  - weather
  - recommendations
