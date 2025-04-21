ALTER TABLE accounts DROP FOREIGN KEY fk_accounts_transaction;

-- Alter the column to allow NULLs
ALTER TABLE accounts MODIFY transaction_id BIGINT NULL;

-- Re-add the foreign key constraint (now allowing NULLs)
ALTER TABLE accounts
ADD CONSTRAINT fk_accounts_transaction
FOREIGN KEY (transaction_id) REFERENCES transactions(id)
ON DELETE CASCADE;