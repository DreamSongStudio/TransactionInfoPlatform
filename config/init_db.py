

create_table_announcement_info = """
CREATE TABLE IF NOT EXISTS announcement_info(
    id INTEGER PRIMARY KEY,
    project_no VARCHAR(30),
    title VARCHAR(100),
    release_date DATETIME,
    release_timestamp  INTEGER,
    url VARCHAR(100),
    have_supplementary TINYINT
)
"""

create_table_announcement_detail = """
CREATE TABLE IF NOT EXISTS announcement_detail(
    id INTEGER PRIMARY KEY,
    info_id INTEGER,
    
    audit_type VARCHAR(10),
    project_region VARCHAR(10),
    bid_registration_time_start DATETIME,
    bid_registration_time_end DATETIME,
    bid_registration_type  VARCHAR(10),
    allow_combination_registration VARCHAR(5),
    earnest_money DECIMAL(10,5),
    bid_amount_max DECIMAL(10,5),
    bid_start_time_start DATETIME,
    bid_start_time_end DATETIME,
    bid_start_address VARCHAR(100),
    bid_file_submit_time_start DATETIME,
    bid_file_submit_time_end DATETIME,
    bid_company VARCHAR(100),
    bid_representative VARCHAR(100),
    bid_company_contact VARCHAR(100),
    bid_proxy_company VARCHAR(100),
    bid_proxy_representative VARCHAR(100),
    bid_proxy_representative_contact VARCHAR(100),
    bid_monitor_org VARCHAR(100),
    bid_monitor_org_contact VARCHAR(100)
    
)
"""