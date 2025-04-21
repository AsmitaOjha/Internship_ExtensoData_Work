USE laxmi_bank;

-- First, check if the foreign key already exists.
-- MySQL doesn’t allow "IF NOT EXISTS" for adding foreign keys,
-- so you must drop it manually if you run this twice.

-- Add the foreign key constraint
-- ALTER TABLE accounts
-- ADD CONSTRAINT fk_accounts_transaction
-- FOREIGN KEY (transaction_id) REFERENCES transactions(id)
-- ON DELETE CASCADE;


ALTER TABLE accounts
ADD COLUMN transaction_id BIGINT,
ADD CONSTRAINT fk_accounts_transaction
FOREIGN KEY (transaction_id) REFERENCES transactions(id)
ON DELETE CASCADE;
