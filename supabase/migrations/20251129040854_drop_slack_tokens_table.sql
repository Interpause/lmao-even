/*
  # Drop slack_tokens table

  1. Changes
    - Drop the slack_tokens table as we're using the proper secrets manager instead
  
  2. Notes
    - This removes the table and all its data
    - Slack tokens are now managed via environment variables/secrets
*/

DROP TABLE IF EXISTS slack_tokens;
