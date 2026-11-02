CREATE DATABASE bms_ds;
USE BMS_DS;
SELECT DATABASE();
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('CUSTOMER', 'EMPLOYEE', 'MANAGER', 'ADMIN') NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE', 'BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE branches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    branch_code VARCHAR(20) NOT NULL UNIQUE,
    branch_name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    phone VARCHAR(20),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    mobile VARCHAR(20),
    email VARCHAR(150),
    date_of_birth DATE,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    employment_type VARCHAR(50),
    kyc_status ENUM('PENDING', 'VERIFIED', 'REJECTED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    mobile VARCHAR(20),
    designation VARCHAR(100),
    branch_id INT,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_user
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_employee_branch
        FOREIGN KEY (branch_id) REFERENCES branches(id)
);
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_number VARCHAR(30) NOT NULL UNIQUE,
    account_type ENUM('SAVINGS', 'CURRENT', 'SALARY', 'FIXED_DEPOSIT') NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    available_balance DECIMAL(15,2) DEFAULT 0.00,
    status ENUM('ACTIVE', 'INACTIVE', 'BLOCKED', 'CLOSED') DEFAULT 'ACTIVE',
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_account_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),

    CONSTRAINT fk_account_branch
        FOREIGN KEY (branch_id) REFERENCES branches(id)
);
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_reference VARCHAR(50) NOT NULL UNIQUE,
    account_id INT NOT NULL,
    transaction_type ENUM(
        'DEPOSIT',
        'WITHDRAWAL',
        'TRANSFER',
        'PAYMENT',
        'UPI',
        'NEFT',
        'RTGS',
        'IMPS'
    ) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    description VARCHAR(255),
    channel ENUM(
        'BRANCH',
        'ATM',
        'ONLINE',
        'MOBILE',
        'UPI'
    ) DEFAULT 'ONLINE',
    status ENUM(
        'PENDING',
        'SUCCESS',
        'FAILED',
        'REVERSED'
    ) DEFAULT 'PENDING',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transaction_account
        FOREIGN KEY (account_id) REFERENCES accounts(id)
);
CREATE TABLE beneficiaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    account_number VARCHAR(30) NOT NULL,
    bank_name VARCHAR(150),
    ifsc_code VARCHAR(20),
    nickname VARCHAR(100),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_beneficiary_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id)
);
CREATE TABLE cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_id INT NOT NULL,
    card_number VARCHAR(30) NOT NULL UNIQUE,
    card_type ENUM('DEBIT', 'CREDIT') NOT NULL,
    expiry_date DATE,
    status ENUM('ACTIVE', 'BLOCKED', 'EXPIRED', 'CANCELLED') DEFAULT 'ACTIVE',
    daily_limit DECIMAL(15,2) DEFAULT 50000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_card_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),

    CONSTRAINT fk_card_account
        FOREIGN KEY (account_id) REFERENCES accounts(id)
);
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    loan_number VARCHAR(50) NOT NULL UNIQUE,
    loan_type ENUM(
        'PERSONAL',
        'HOME',
        'EDUCATION',
        'VEHICLE',
        'BUSINESS'
    ) NOT NULL,
    principal_amount DECIMAL(15,2) NOT NULL,
    interest_rate DECIMAL(5,2) NOT NULL,
    tenure_months INT NOT NULL,
    outstanding_amount DECIMAL(15,2) NOT NULL,
    status ENUM(
        'APPLIED',
        'PENDING',
        'APPROVED',
        'ACTIVE',
        'REJECTED',
        'CLOSED'
    ) DEFAULT 'APPLIED',
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_date TIMESTAMP NULL,

    CONSTRAINT fk_loan_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id)
);
CREATE TABLE loan_payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    principal_component DECIMAL(15,2) DEFAULT 0.00,
    interest_component DECIMAL(15,2) DEFAULT 0.00,
    status ENUM('PENDING', 'SUCCESS', 'FAILED') DEFAULT 'PENDING',

    CONSTRAINT fk_loan_payment_loan
        FOREIGN KEY (loan_id) REFERENCES loans(id)
);
CREATE TABLE kyc_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    document_type ENUM(
        'AADHAAR',
        'PAN',
        'PASSPORT',
        'DRIVING_LICENSE',
        'VOTER_ID'
    ) NOT NULL,
    document_number VARCHAR(100) NOT NULL,
    verification_status ENUM(
        'PENDING',
        'VERIFIED',
        'REJECTED'
    ) DEFAULT 'PENDING',
    verified_by INT NULL,
    verified_at TIMESTAMP NULL,
    remarks VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_kyc_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),

    CONSTRAINT fk_kyc_verified_by
        FOREIGN KEY (verified_by) REFERENCES employees(id)
);
CREATE TABLE account_opening_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    application_number VARCHAR(50) NOT NULL UNIQUE,

    full_name VARCHAR(150) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    date_of_birth DATE NOT NULL,

    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,

    employment_type VARCHAR(100),
    account_type ENUM(
        'SAVINGS',
        'CURRENT',
        'SALARY',
        'FIXED_DEPOSIT'
    ) NOT NULL,

    branch_id INT NOT NULL,
    initial_deposit DECIMAL(15,2) DEFAULT 0.00,

    nominee_name VARCHAR(150),
    nominee_relation VARCHAR(100),

    status ENUM(
        'SUBMITTED',
        'UNDER_REVIEW',
        'KYC_PENDING',
        'PENDING_APPROVAL',
        'APPROVED',
        'REJECTED',
        'ACCOUNT_CREATED'
    ) DEFAULT 'SUBMITTED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_application_branch
        FOREIGN KEY (branch_id) REFERENCES branches(id)
);
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message VARCHAR(500) NOT NULL,
    notification_type ENUM(
        'INFO',
        'SUCCESS',
        'WARNING',
        'ALERT'
    ) DEFAULT 'INFO',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_notification_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE service_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    request_type VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    priority ENUM('LOW', 'MEDIUM', 'HIGH', 'URGENT') DEFAULT 'MEDIUM',
    status ENUM(
        'OPEN',
        'IN_PROGRESS',
        'RESOLVED',
        'CLOSED',
        'REJECTED'
    ) DEFAULT 'OPEN',
    assigned_to INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_service_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),

    CONSTRAINT fk_service_employee
        FOREIGN KEY (assigned_to) REFERENCES employees(id)
);
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'bms_ds'
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME;
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_KEY,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'bms_ds'
ORDER BY TABLE_NAME, ORDINAL_POSITION;