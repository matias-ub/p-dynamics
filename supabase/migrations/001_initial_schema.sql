-- =========================================================
-- BASE MIGRATION SQL
-- Versión final unificada (tu esquema + auth anónima nativa + rooms futuro-proof)
-- Fecha: 18 Feb 2026
-- =========================================================

-- =========================================================
-- EXTENSIONS
-- =========================================================
create extension if not exists "pgcrypto";

-- =========================================================
-- GENERIC TRIGGERS
-- =========================================================

-- Trigger for updated_at (optional but recommended)
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- =========================================================
-- PROFILES (funciona tanto para usuarios reales como anónimos)
-- =========================================================
create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    name text,
    avatar_url text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Users can read own profile"
    on public.profiles for select
    using (auth.uid() = id);

create policy "Users can update own profile"
    on public.profiles for update
    using (auth.uid() = id);

drop trigger if exists profiles_updated_at on public.profiles;
create trigger profiles_updated_at
  before update on public.profiles
  for each row execute function update_updated_at();

-- =========================================================
-- AUTO CREATE PROFILE ON SIGNUP (incluye anónimos)
-- =========================================================
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, name, avatar_url)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', 'Usuario'),
    new.raw_user_meta_data->>'avatar_url'
  );
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- =========================================================
-- QUESTIONS
-- =========================================================
create table if not exists public.questions (
    id uuid primary key default gen_random_uuid(),
    text text not null,
    intensity_level smallint not null check (intensity_level between 1 and 5),
    created_at timestamptz not null default now()
);

alter table public.questions enable row level security;
create policy "Public read questions"
    on public.questions for select using (true);

-- =========================================================
-- OPTIONS
-- =========================================================
create table if not exists public.options (
    id uuid primary key default gen_random_uuid(),
    question_id uuid not null references public.questions(id) on delete cascade,
    text text not null,
    position smallint not null,
    created_at timestamptz not null default now(),
    unique (question_id, position)
);

create index if not exists idx_options_question on public.options(question_id);

alter table public.options enable row level security;
create policy "Public read options"
    on public.options for select using (true);

-- =========================================================
-- DAILY QUESTIONS
-- =========================================================
create table if not exists public.daily_questions (
    id uuid primary key default gen_random_uuid(),
    question_id uuid not null references public.questions(id) on delete cascade,
    date date not null unique,
    created_at timestamptz not null default now()
);

alter table public.daily_questions enable row level security;
create policy "Public read daily questions"
    on public.daily_questions for select using (true);

-- =========================================================
-- ROOMS (futuro-proof: pareja + grupos)
-- =========================================================
create table if not exists public.rooms (
    id uuid primary key default gen_random_uuid(),
    token varchar(24) not null unique,
    max_participants smallint not null default 2 check (max_participants > 0),
    room_type text not null default 'couple' check (room_type in ('couple', 'group')),
    is_permanent boolean not null default false,
    streak_count int not null default 0,
    last_streak_date date,
    created_at timestamptz not null default now(),
    -- Constraint para parejas (siempre máximo 2)
    constraint chk_couple_max_participants check (room_type != 'couple' or max_participants = 2)
);

create index if not exists idx_rooms_token on public.rooms(token);

alter table public.rooms enable row level security;

-- Lectura pública por token (necesario para que cualquiera pueda unirse con el código)
create policy "Public read rooms for joining"
    on public.rooms for select using (true);

-- Solo service_role (backend) puede crear rooms
-- No hay policy de insert

-- =========================================================
-- RESPONSES (siempre con user_id real de auth.users - anónimo o permanente)
-- =========================================================
create table if not exists public.responses (
    id uuid primary key default gen_random_uuid(),
    room_id uuid not null references public.rooms(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    daily_question_id uuid not null references public.daily_questions(id) on delete cascade,
    self_option_id uuid not null references public.options(id),
    partner_prediction_option_id uuid not null references public.options(id),
    created_at timestamptz not null default now()
);

create index if not exists idx_responses_room_day 
    on public.responses(room_id, daily_question_id);

create index if not exists idx_responses_user_id
    on public.responses(user_id);

-- Un usuario responde solo una vez por room por día
create unique index if not exists uniq_response_per_user_day 
    on public.responses(room_id, daily_question_id, user_id);

alter table public.responses enable row level security;

-- =========================================================
-- RLS RESPONSES (más seguro que "public total")
-- =========================================================
create policy "Authenticated users can insert their own response"
    on public.responses for insert
    with check (auth.uid() = user_id);

create policy "Room participants can read responses"
    on public.responses for select
    using (
        exists (
            select 1 
            from public.responses r2 
            where r2.room_id = responses.room_id 
              and r2.user_id = auth.uid()
        )
    );

-- =========================================================
-- TRIGGER: CAPACITY CHECK (adaptado a user_id)
-- =========================================================
create or replace function public.check_room_capacity()
returns trigger as $$
declare
    participant_count integer;
    room_limit integer;
begin
    -- Lock del room
    select max_participants
    into room_limit
    from public.rooms
    where id = new.room_id
    for update;

    select count(distinct user_id)
    into participant_count
    from public.responses
    where room_id = new.room_id 
      and daily_question_id = new.daily_question_id;

    if participant_count >= room_limit then
        raise exception 'Room capacity exceeded for this day';
    end if;

    return new;
end;
$$ language plpgsql;

drop trigger if exists enforce_room_capacity on public.responses;
create trigger enforce_room_capacity
    before insert on public.responses
    for each row
    execute procedure public.check_room_capacity();

-- =========================================================
-- TRIGGER: VALIDACIÓN DE OPCIONES
-- =========================================================
create or replace function public.validate_response_options()
returns trigger as $$
declare
    correct_question uuid;
begin
    select q.id
    into correct_question
    from public.daily_questions dq
    join public.questions q on q.id = dq.question_id
    where dq.id = new.daily_question_id;

    if not exists (
        select 1 from public.options
        where id = new.self_option_id
          and question_id = correct_question
    ) then
        raise exception 'Invalid self option for this question';
    end if;

    if not exists (
        select 1 from public.options
        where id = new.partner_prediction_option_id
          and question_id = correct_question
    ) then
        raise exception 'Invalid partner prediction option';
    end if;

    return new;
end;
$$ language plpgsql;

drop trigger if exists validate_response_options_trigger on public.responses;
create trigger validate_response_options_trigger
    before insert on public.responses
    for each row
    execute procedure public.validate_response_options();

-- =========================================================
-- FIN DEL SCHEMA
-- =========================================================