# Database Schema Documentation

This document describes the Supabase database structure used in Claude Computer.

## 🗄️ Database Overview

Claude Computer uses Supabase (PostgreSQL) for:
- Real-time audience message streaming
- Activity logging and search
- Behavior tracking and analytics
- Chat session management
- Memory system for persistent learning
- System health monitoring

**Project ID**: `fcxkkpjgwyiopvlewjtl`  
**Database Version**: PostgreSQL 17.4.1

## 📊 Tables

### `audience_messages`
Stores AI-generated commentary and reactions from Claude.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `message` | TEXT | The message content |
| `message_type` | TEXT | Type: `commentary`, `reaction`, `discovery`, `question`, `reflection`, `spontaneous` |
| `timestamp` | TIMESTAMPTZ | When the message was created |
| `context` | TEXT | Optional context about what Claude was doing |
| `activity_id` | UUID | Foreign key to activities table |
| `emotion` | TEXT | Emotional tone: `excitement`, `frustration`, `surprise`, `satisfaction`, `confusion`, `neutral` |
| `created_at` | TIMESTAMPTZ | Database insertion time |

**Indexes**: `timestamp`, `message_type`, `emotion`
**Foreign Keys**: `activity_id` → `activities.id`

### `activities`
Logs all actions performed by Claude.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `activity_id` | VARCHAR | Unique activity identifier (indexed) |
| `activity_type` | VARCHAR | Type: `system`, `user`, `assistant`, `tool`, `behavior` |
| `action` | VARCHAR | The action performed |
| `data` | JSONB | Activity details and metadata |
| `duration_ms` | INTEGER | Execution time in milliseconds |
| `parent_id` | UUID | Links to parent activity (self-referencing) |
| `timestamp` | TIMESTAMPTZ | When the activity occurred |
| `created_at` | TIMESTAMPTZ | Database insertion time |

**Indexes**: `activity_id` (unique), `activity_type`, `timestamp`
**Foreign Keys**: `parent_id` → `activities.id` (self-referencing)

**JSONB data structure**:
```json
{
  "action": "string",
  "details": "string",
  "result": "string",
  "duration_ms": 1234,
  "tool_name": "string",
  "parameters": {}
}
```

### `behaviors`
Tracks autonomous behavior execution.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `behavior_type` | TEXT | The behavior that was executed |
| `parameters` | JSONB | Behavior configuration parameters |
| `status` | VARCHAR | Status: `pending`, `active`, `completed`, `stopped`, `error` |
| `result` | JSONB | Behavior execution results |
| `started_at` | TIMESTAMPTZ | When behavior started |
| `completed_at` | TIMESTAMPTZ | When behavior completed (nullable) |
| `duration_minutes` | INTEGER | Total duration in minutes |
| `error_message` | TEXT | Error details if failed (nullable) |
| `created_at` | TIMESTAMPTZ | Database insertion time |

**Indexes**: `behavior_type`, `status`, `started_at`
**Row Count**: ~280 behaviors tracked

### `screenshots` (Optional)
Metadata for captured screenshots.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `timestamp` | TIMESTAMPTZ | When screenshot was taken |
| `filename` | VARCHAR | Screenshot filename |
| `resolution` | VARCHAR | Image resolution (e.g., "1024x768") |
| `file_size` | INTEGER | File size in bytes |
| `activity_id` | UUID | Foreign key to activities table |
| `created_at` | TIMESTAMPTZ | Database insertion time |

### `chat_sessions`
Manages chat conversation sessions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `title` | TEXT | Session title |
| `status` | TEXT | Status: `active`, `archived` |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

### `chat_messages`
Stores individual chat messages.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `session_id` | UUID | Foreign key to chat_sessions |
| `message` | TEXT | Message content |
| `role` | TEXT | Role: `user`, `assistant` |
| `metadata` | JSONB | Additional message metadata |
| `created_at` | TIMESTAMPTZ | Message timestamp |

### `memories`
Claude's long-term memory storage.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `type` | VARCHAR | Type: `skill`, `knowledge`, `experience`, `preference`, `website` |
| `category` | VARCHAR | Memory category |
| `title` | VARCHAR | Memory title |
| `content` | TEXT | Memory content |
| `context` | JSONB | Contextual information |
| `relevance_score` | FLOAT | Relevance scoring (0-1) |
| `access_count` | INTEGER | Times accessed |
| `tags` | TEXT[] | Array of tags |
| `source_activity_id` | UUID | Link to originating activity |
| `created_at` | TIMESTAMPTZ | Creation time |
| `last_accessed` | TIMESTAMPTZ | Last access time |

### `memory_associations`
Relationships between memories.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `memory_id_1` | UUID | First memory reference |
| `memory_id_2` | UUID | Second memory reference |
| `association_type` | VARCHAR | Type: `similar`, `prerequisite`, `opposite`, `related` |
| `strength` | FLOAT | Association strength (0-1) |
| `created_at` | TIMESTAMPTZ | Creation time |

### `session_memory`
Short-term memory for current session.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `session_id` | VARCHAR | Session identifier |
| `memory_type` | VARCHAR | Type: `goal`, `context`, `state`, `recent_action` |
| `content` | JSONB | Memory content |
| `expires_at` | TIMESTAMPTZ | Expiration time |
| `created_at` | TIMESTAMPTZ | Creation time |

### `shared_chat`
Public chat messages with RLS enabled.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `message` | TEXT | Message content |
| `sender` | TEXT | Sender: `user`, `assistant`, `system` |
| `timestamp` | TIMESTAMPTZ | Message timestamp |
| `metadata` | JSONB | Additional metadata |

**Note**: This table has Row Level Security (RLS) enabled.

## 🔄 Real-time Subscriptions

Supabase real-time is enabled for:
- `audience_messages` - Live commentary updates
- `activities` - Real-time activity feed

Example subscription:
```javascript
const subscription = supabase
  .channel('audience_messages')
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'audience_messages' },
    (payload) => {
      console.log('New message:', payload.new);
    }
  )
  .subscribe();
```

## 🔑 Row Level Security (RLS)

Currently, RLS is disabled for development. For production:
- Enable RLS on all tables
- Create policies for read/write access
- Use service role key for backend operations

## 🚀 Common Queries

### Get recent activities
```sql
SELECT * FROM activities 
WHERE activity_type IN ('user', 'assistant')
ORDER BY timestamp DESC 
LIMIT 50;
```

### Search activities by keyword
```sql
SELECT * FROM activities 
WHERE data->>'action' ILIKE '%search%'
OR data->>'details' ILIKE '%search%'
ORDER BY timestamp DESC;
```

### Get audience messages for an activity
```sql
SELECT * FROM audience_messages 
WHERE activity_id = 'some-activity-id'
ORDER BY timestamp ASC;
```

### Behavior analytics
```sql
SELECT 
  behavior_type,
  COUNT(*) as execution_count,
  AVG(duration_minutes) as avg_duration,
  SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count
FROM behaviors
GROUP BY behavior_type;
```

## 🛠️ Setup Instructions

1. **Create a Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and anon key

2. **Run Database Migrations**
   ```sql
   -- Create tables (run in Supabase SQL editor)
   
   -- audience_messages table
   CREATE TABLE audience_messages (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     message TEXT NOT NULL,
     message_type TEXT NOT NULL CHECK (message_type IN ('commentary', 'reaction', 'discovery', 'question', 'reflection', 'spontaneous')),
     timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
     context TEXT,
     activity_id TEXT,
     emotion TEXT CHECK (emotion IN ('excitement', 'frustration', 'surprise', 'satisfaction', 'confusion', 'neutral')),
     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   -- activities table
   CREATE TABLE activities (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     activity_id TEXT UNIQUE,
     activity_type TEXT NOT NULL CHECK (activity_type IN ('system', 'user', 'assistant', 'tool', 'behavior')),
     category TEXT NOT NULL,
     data JSONB,
     timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   -- behaviors table
   CREATE TABLE behaviors (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     behavior_type TEXT NOT NULL,
     parameters JSONB DEFAULT '{}',
     status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'stopped', 'error')),
     started_at TIMESTAMPTZ NOT NULL,
     completed_at TIMESTAMPTZ,
     duration_minutes INTEGER,
     error_message TEXT,
     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   -- Create indexes
   CREATE INDEX idx_audience_messages_timestamp ON audience_messages(timestamp);
   CREATE INDEX idx_audience_messages_type ON audience_messages(message_type);
   CREATE INDEX idx_activities_type ON activities(activity_type);
   CREATE INDEX idx_activities_timestamp ON activities(timestamp);
   CREATE INDEX idx_behaviors_type ON behaviors(behavior_type);
   CREATE INDEX idx_behaviors_status ON behaviors(status);
   ```

3. **Enable Realtime**
   - Go to Database → Replication
   - Enable replication for `audience_messages` and `activities` tables

4. **Configure Environment**
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   ```

## 📝 Contributing Database Changes

When modifying the database:

1. **Document your changes** in this file
2. **Create migration scripts** in `/database/migrations/`
3. **Update TypeScript types** in `/frontend/types/database.ts`
4. **Test with real data** before submitting PR
5. **Consider performance** - add indexes for frequently queried columns

## 🔍 Debugging Tips

- Use Supabase dashboard for real-time data inspection
- Enable query logging in development
- Monitor slow queries in Supabase dashboard
- Use EXPLAIN ANALYZE for query optimization

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL JSONB Guide](https://www.postgresql.org/docs/current/datatype-json.html)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)