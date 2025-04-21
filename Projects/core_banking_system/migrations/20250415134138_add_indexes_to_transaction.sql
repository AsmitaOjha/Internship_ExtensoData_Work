--DROP INDEX idx_sender_account ON transactions;
CREATE INDEX idx_sender_account ON transactions(sender_account_id);
--DROP INDEX idx_receiver_account ON transactions;

CREATE INDEX idx_receiver_account ON transactions(receiver_account_id);
--DROP INDEX idx_transaction_time ON transactions;

CREATE INDEX idx_transaction_time ON transactions(transaction_time);

