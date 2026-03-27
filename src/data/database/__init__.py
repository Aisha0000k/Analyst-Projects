"""
Database module for data persistence and retrieval.
"""

from .supabase import SupabaseClient, create_supabase_client

__all__ = ["SupabaseClient", "create_supabase_client"]
