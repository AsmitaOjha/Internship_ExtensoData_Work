ALTER TABLE transactions
MODIFY COLUMN remark ENUM(
    'travel & ticketing',
    'food',
    'clz/school fee',
    'recharge',
    'rent',
    'cloth and accessories',
    'clothes',
    'other'
) NOT NULL;
