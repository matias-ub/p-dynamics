-- 001_initial_schema.sql
-- Initial database schema for P Dynamics - 4 Perspectivas para Parejas

-- Enable UUID extension (usually enabled by default in Supabase)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 1. Profiles (extension of auth.users)
-- Supabase creates auth.users automatically
-- =============================================================================
CREATE TABLE public.profiles (
  id          uuid PRIMARY KEY REFERENCES auth.users ON DELETE CASCADE,
  name        text,                     -- visible name (can come from Google)
  avatar_url  text,                     -- profile picture
  email       text UNIQUE,              -- optional, but useful for email invites
  created_at  timestamptz DEFAULT now(),
  updated_at  timestamptz DEFAULT now()
);

-- Trigger for updated_at (optional but recommended)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- 2. Couples (1:1, but allows null in user2 until invite is accepted)
-- =============================================================================
CREATE TABLE public.couples (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user1_id    uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  user2_id    uuid REFERENCES profiles(id) ON DELETE SET NULL,  -- can be null temporarily
  invite_code text UNIQUE NOT NULL DEFAULT substring(md5(random()::text), 1, 8),  -- short code to share
  status      text DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'inactive')),  -- improves UX
  created_at  timestamptz DEFAULT now(),
  updated_at  timestamptz DEFAULT now()
);

-- Index for fast lookups by invite_code
CREATE INDEX idx_couples_invite_code ON public.couples(invite_code);

-- Trigger updated_at
CREATE TRIGGER couples_updated_at
  BEFORE UPDATE ON public.couples
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- 3. Scenario Packs (for versioning: cotidiano-v1, intimidad-v2, etc.)
-- =============================================================================
CREATE TABLE public.scenario_packs (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        text UNIQUE NOT NULL,     -- 'cotidiano-v1', 'intimidad-2026', etc.
  title       text NOT NULL,
  description text,
  is_active   boolean DEFAULT true,
  created_at  timestamptz DEFAULT now()
);

-- =============================================================================
-- 4. Individual Scenarios (within a pack)
-- =============================================================================
CREATE TABLE public.scenarios (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  pack_id     uuid NOT NULL REFERENCES scenario_packs(id) ON DELETE CASCADE,
  key         text NOT NULL UNIQUE,     -- 'platos-sucios', 'tiempo-libre-viernes', etc.
  title       text NOT NULL,
  description text NOT NULL,             -- full situation text
  order_num   integer DEFAULT 0,         -- for display ordering
  created_at  timestamptz DEFAULT now()
);

CREATE INDEX idx_scenarios_pack_key ON public.scenarios(pack_id, key);

-- =============================================================================
-- 5. Response Options per Scenario
-- =============================================================================
CREATE TABLE public.scenario_options (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  scenario_id uuid NOT NULL REFERENCES scenarios(id) ON DELETE CASCADE,
  key         text NOT NULL,             -- 'A', 'B', 'C'...
  text        text NOT NULL,             -- what the user sees
  tags        jsonb,                     -- {"generosidad": 9, "colaboracion": 8, "equidad": 5, ...}
  is_positive boolean DEFAULT true,      -- to filter "negative" options if needed
  order_num   integer DEFAULT 0,
  created_at  timestamptz DEFAULT now(),

  UNIQUE (scenario_id, key)              -- unique key per scenario
);

-- =============================================================================
-- 6. Tests (instances taken by a couple)
-- =============================================================================
CREATE TABLE public.tests (
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  couple_id   uuid NOT NULL REFERENCES couples(id) ON DELETE CASCADE,
  pack_id     uuid NOT NULL REFERENCES scenario_packs(id),
  status      text DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'aborted')),
  created_at  timestamptz DEFAULT now(),
  completed_at timestamptz
);

-- =============================================================================
-- 7. Responses (user answers)
-- =============================================================================
CREATE TABLE public.responses (
  id             uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  test_id        uuid NOT NULL REFERENCES tests(id) ON DELETE CASCADE,
  user_id        uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  scenario_id    uuid NOT NULL REFERENCES scenarios(id) ON DELETE RESTRICT,  -- better to reference id than key
  option_key     text NOT NULL,             -- 'A', 'B'...
  free_text      text,
  perspective    smallint NOT NULL CHECK (perspective BETWEEN 1 AND 4),
  created_at     timestamptz DEFAULT now(),

  UNIQUE (test_id, user_id, scenario_id, perspective)  -- prevents duplicates per user/perspective
);

-- Index for fast queries of a complete test
CREATE INDEX idx_responses_test_user_scenario ON public.responses(test_id, user_id, scenario_id);
