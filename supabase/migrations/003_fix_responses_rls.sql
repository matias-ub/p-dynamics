-- Fix recursive RLS policy on responses
-- This avoids infinite recursion by checking participation with row_security disabled.

-- Helper function to check room participation without RLS recursion
create or replace function public.is_room_participant(room_uuid uuid)
returns boolean
language sql
security definer
set search_path = public
set row_security = off
stable
as $$
  select exists (
    select 1
    from public.responses r
    where r.room_id = room_uuid
      and r.user_id = auth.uid()
  );
$$;

-- Replace the recursive select policy
drop policy if exists "Room participants can read responses" on public.responses;

create policy "Room participants can read responses"
  on public.responses for select
  using (
    public.is_room_participant(room_id)
  );
