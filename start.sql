-- Create habits table
create table habits (
    id bigint primary key generated always as identity,
    name text not null,
    is_good boolean not null default true,
    goal_streak integer,
    current_streak integer not null default 0,
    longest_streak integer not null default 0,
    user_id uuid not null references auth.users(id) on delete cascade,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now()
);

-- Create habit_logs table
create table habit_logs (
    id bigint primary key generated always as identity,
    habit_id bigint not null references habits(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    date date not null,
    completed boolean not null default false,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now()
);

-- Create indexes
create index habits_user_id_idx on habits(user_id);
create index habit_logs_habit_id_idx on habit_logs(habit_id);
create index habit_logs_user_id_idx on habit_logs(user_id);
create unique index habit_logs_habit_date_idx on habit_logs(habit_id, date);

-- Enable Row Level Security
alter table habits enable row level security;
alter table habit_logs enable row level security;

-- Create policies
create policy "Users can create their own habits"
    on habits for insert
    with check (auth.uid() = user_id);

create policy "Users can view their own habits"
    on habits for select
    using (auth.uid() = user_id);

create policy "Users can update their own habits"
    on habits for update
    using (auth.uid() = user_id);

create policy "Users can delete their own habits"
    on habits for delete
    using (auth.uid() = user_id);

create policy "Users can create their own habit logs"
    on habit_logs for insert
    with check (auth.uid() = user_id);

create policy "Users can view their own habit logs"
    on habit_logs for select
    using (auth.uid() = user_id);

create policy "Users can update their own habit logs"
    on habit_logs for update
    using (auth.uid() = user_id);

create policy "Users can delete their own habit logs"
    on habit_logs for delete
    using (auth.uid() = user_id);