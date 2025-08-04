// Database types generated from Supabase schema
// Project: fcxkkpjgwyiopvlewjtl

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      audience_messages: {
        Row: {
          id: string
          message: string
          message_type: 'commentary' | 'reaction' | 'discovery' | 'question' | 'reflection' | 'spontaneous'
          timestamp: string
          context: string | null
          activity_id: string | null
          emotion: 'excitement' | 'frustration' | 'surprise' | 'satisfaction' | 'confusion' | 'neutral' | null
          created_at: string
        }
        Insert: {
          id?: string
          message: string
          message_type?: 'commentary' | 'reaction' | 'discovery' | 'question' | 'reflection' | 'spontaneous'
          timestamp?: string
          context?: string | null
          activity_id?: string | null
          emotion?: 'excitement' | 'frustration' | 'surprise' | 'satisfaction' | 'confusion' | 'neutral' | null
          created_at?: string
        }
        Update: {
          id?: string
          message?: string
          message_type?: 'commentary' | 'reaction' | 'discovery' | 'question' | 'reflection' | 'spontaneous'
          timestamp?: string
          context?: string | null
          activity_id?: string | null
          emotion?: 'excitement' | 'frustration' | 'surprise' | 'satisfaction' | 'confusion' | 'neutral' | null
          created_at?: string
        }
      }
      activities: {
        Row: {
          id: string
          activity_id: string
          timestamp: string
          activity_type: 'system' | 'user' | 'assistant' | 'tool' | 'behavior'
          action: string
          data: Json
          duration_ms: number | null
          parent_id: string | null
          created_at: string
        }
        Insert: {
          id?: string
          activity_id: string
          timestamp: string
          activity_type: 'system' | 'user' | 'assistant' | 'tool' | 'behavior'
          action: string
          data?: Json
          duration_ms?: number | null
          parent_id?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          activity_id?: string
          timestamp?: string
          activity_type?: 'system' | 'user' | 'assistant' | 'tool' | 'behavior'
          action?: string
          data?: Json
          duration_ms?: number | null
          parent_id?: string | null
          created_at?: string
        }
      }
      behaviors: {
        Row: {
          id: string
          behavior_type: string
          status: 'pending' | 'active' | 'completed' | 'stopped' | 'error'
          parameters: Json | null
          started_at: string | null
          completed_at: string | null
          duration_minutes: number | null
          result: Json | null
          created_at: string
        }
        Insert: {
          id?: string
          behavior_type: string
          status?: 'pending' | 'active' | 'completed' | 'stopped' | 'error'
          parameters?: Json | null
          started_at?: string | null
          completed_at?: string | null
          duration_minutes?: number | null
          result?: Json | null
          created_at?: string
        }
        Update: {
          id?: string
          behavior_type?: string
          status?: 'pending' | 'active' | 'completed' | 'stopped' | 'error'
          parameters?: Json | null
          started_at?: string | null
          completed_at?: string | null
          duration_minutes?: number | null
          result?: Json | null
          created_at?: string
        }
      }
      screenshots: {
        Row: {
          id: string
          filename: string | null
          resolution: string | null
          file_size: number | null
          timestamp: string
          activity_id: string | null
          created_at: string
        }
        Insert: {
          id?: string
          filename?: string | null
          resolution?: string | null
          file_size?: number | null
          timestamp: string
          activity_id?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          filename?: string | null
          resolution?: string | null
          file_size?: number | null
          timestamp?: string
          activity_id?: string | null
          created_at?: string
        }
      }
      chat_sessions: {
        Row: {
          id: string
          created_at: string | null
          updated_at: string | null
          title: string | null
          status: 'active' | 'archived' | null
        }
        Insert: {
          id?: string
          created_at?: string | null
          updated_at?: string | null
          title?: string | null
          status?: 'active' | 'archived' | null
        }
        Update: {
          id?: string
          created_at?: string | null
          updated_at?: string | null
          title?: string | null
          status?: 'active' | 'archived' | null
        }
      }
      chat_messages: {
        Row: {
          id: string
          session_id: string | null
          message: string
          role: 'user' | 'assistant'
          created_at: string | null
          metadata: Json | null
        }
        Insert: {
          id?: string
          session_id?: string | null
          message: string
          role: 'user' | 'assistant'
          created_at?: string | null
          metadata?: Json | null
        }
        Update: {
          id?: string
          session_id?: string | null
          message?: string
          role?: 'user' | 'assistant'
          created_at?: string | null
          metadata?: Json | null
        }
      }
      memories: {
        Row: {
          id: string
          type: 'skill' | 'knowledge' | 'experience' | 'preference' | 'website'
          category: string | null
          title: string
          content: string
          context: Json | null
          relevance_score: number | null
          access_count: number | null
          created_at: string | null
          last_accessed: string | null
          tags: string[] | null
          source_activity_id: string | null
        }
        Insert: {
          id?: string
          type: 'skill' | 'knowledge' | 'experience' | 'preference' | 'website'
          category?: string | null
          title: string
          content: string
          context?: Json | null
          relevance_score?: number | null
          access_count?: number | null
          created_at?: string | null
          last_accessed?: string | null
          tags?: string[] | null
          source_activity_id?: string | null
        }
        Update: {
          id?: string
          type?: 'skill' | 'knowledge' | 'experience' | 'preference' | 'website'
          category?: string | null
          title?: string
          content?: string
          context?: Json | null
          relevance_score?: number | null
          access_count?: number | null
          created_at?: string | null
          last_accessed?: string | null
          tags?: string[] | null
          source_activity_id?: string | null
        }
      }
      memory_associations: {
        Row: {
          id: string
          memory_id_1: string | null
          memory_id_2: string | null
          association_type: 'similar' | 'prerequisite' | 'opposite' | 'related' | null
          strength: number | null
          created_at: string | null
        }
        Insert: {
          id?: string
          memory_id_1?: string | null
          memory_id_2?: string | null
          association_type?: 'similar' | 'prerequisite' | 'opposite' | 'related' | null
          strength?: number | null
          created_at?: string | null
        }
        Update: {
          id?: string
          memory_id_1?: string | null
          memory_id_2?: string | null
          association_type?: 'similar' | 'prerequisite' | 'opposite' | 'related' | null
          strength?: number | null
          created_at?: string | null
        }
      }
      session_memory: {
        Row: {
          id: string
          session_id: string
          memory_type: 'goal' | 'context' | 'state' | 'recent_action' | null
          content: Json
          expires_at: string
          created_at: string | null
        }
        Insert: {
          id?: string
          session_id: string
          memory_type?: 'goal' | 'context' | 'state' | 'recent_action' | null
          content: Json
          expires_at: string
          created_at?: string | null
        }
        Update: {
          id?: string
          session_id?: string
          memory_type?: 'goal' | 'context' | 'state' | 'recent_action' | null
          content?: Json
          expires_at?: string
          created_at?: string | null
        }
      }
      shared_chat: {
        Row: {
          id: string
          message: string
          sender: 'user' | 'assistant' | 'system'
          timestamp: string | null
          metadata: Json | null
        }
        Insert: {
          id?: string
          message: string
          sender: 'user' | 'assistant' | 'system'
          timestamp?: string | null
          metadata?: Json | null
        }
        Update: {
          id?: string
          message?: string
          sender?: 'user' | 'assistant' | 'system'
          timestamp?: string | null
          metadata?: Json | null
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}

// Helper types for easier usage
export type AudienceMessage = Database['public']['Tables']['audience_messages']['Row']
export type Activity = Database['public']['Tables']['activities']['Row']
export type Behavior = Database['public']['Tables']['behaviors']['Row']
export type Screenshot = Database['public']['Tables']['screenshots']['Row']
export type ChatSession = Database['public']['Tables']['chat_sessions']['Row']
export type ChatMessage = Database['public']['Tables']['chat_messages']['Row']
export type Memory = Database['public']['Tables']['memories']['Row']
export type MemoryAssociation = Database['public']['Tables']['memory_associations']['Row']
export type SessionMemory = Database['public']['Tables']['session_memory']['Row']
export type SharedChat = Database['public']['Tables']['shared_chat']['Row']

// Insert types
export type InsertAudienceMessage = Database['public']['Tables']['audience_messages']['Insert']
export type InsertActivity = Database['public']['Tables']['activities']['Insert']
export type InsertBehavior = Database['public']['Tables']['behaviors']['Insert']
export type InsertMemory = Database['public']['Tables']['memories']['Insert']