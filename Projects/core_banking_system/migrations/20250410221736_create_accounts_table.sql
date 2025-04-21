CREATE TABLE IF NOT EXISTS accounts (
    account_number VARCHAR(20) PRIMARY KEY,
    account_type ENUM('Saving', 'Current', 'Fixed Deposit') NOT NULL DEFAULT 'Saving',
    account_status ENUM('Active', 'Closed') NOT NULL,
    account_balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL,
    closed_at DATETIME,
    user_id BIGINT NOT NULL,
    transaction_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -- FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);