CREATE DATABASE snapshop_auth;
USE snapshop_auth;
CREATE TABLE referralhistory (
 id INT(11) NOT NULL AUTO_INCREMENT,
 referrer_telegram VARCHAR(50) NOT NULL COLLATE 'utf8mb4_bin',
 referee_telegram VARCHAR(50) NOT NULL COLLATE 'utf8mb4_bin',
 created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

--######################################################
--//////////////////////////////////////////////////////
--######################################################
CREATE DATABASE snapshop_property;
USE snapshop_property;

CREATE TABLE coupons (
 id INT(11) NOT NULL AUTO_INCREMENT,
 code VARCHAR(64) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
 title VARCHAR(64) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
 description TEXT NULL COLLATE 'utf8mb4_bin',
 coupontype VARCHAR(24) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
 shopid INT(11) NULL DEFAULT NULL,
 imageurl TEXT NULL COLLATE 'utf8mb4_bin',
 teleimageurl TEXT NULL COLLATE 'utf8mb4_bin',
 expirefrom DATE NULL DEFAULT '1000-01-01',
 expireto DATE NULL DEFAULT '1000-01-01',
 createdate TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX code (code)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO coupons(id, code, title, description, shopid, teleimageurl, expirefrom, expireto) VALUES
(13, 'MD001', '1-for-1 McDDs', 'Sample coupon 1', 1, './assets/voucher_images/sample/sample0001.png', '2021-01-01', '2031-01-01'),
(14, 'MD002', '10% off McDDs', 'Sample coupon 2', 1, './assets/voucher_images/sample/sample0001.png', '2021-01-01', '2021-12-01'),
(15, 'KF001', '15% off Chicken', 'Sample coupon 3', 2, './assets/voucher_images/sample/sample0001.png', '2021-01-01', '2031-01-01'),
(16, 'BK001', '15% off Burgers', 'Sample coupon 4', 3, './assets/voucher_images/sample/sample0001.png', '2021-01-01', '2031-01-01');



CREATE TABLE dailycoupons (
 id INT(11) NOT NULL AUTO_INCREMENT,
 couponid INT(11) NULL DEFAULT '0',
 startdate DATE NULL DEFAULT '1000-01-01',
 enddate DATE NULL DEFAULT '1000-01-01',
 action VARCHAR(12) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
 gameid INT(11) NULL DEFAULT '0',
 winscore INT(11) NULL DEFAULT '0',
 totalamount INT(11) NULL DEFAULT '0',
 issueamount INT(11) NULL DEFAULT '0',
 isadver TINYINT(4) NULL DEFAULT '0',
 isdeleted TINYINT(4) NULL DEFAULT '0',
 createdate TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX couponid (couponid)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO dailycoupons(couponid, action, totalamount, isdeleted) VALUES
(13, 'new_user', 9999, 0),
(14, 'weekly_login', 9999, 0);



CREATE TABLE exchangecoupons (
 id INT(11) NOT NULL AUTO_INCREMENT,
 couponid INT(11) NULL DEFAULT '0',
 startdate DATE NULL DEFAULT '1000-01-01',
 enddate DATE NULL DEFAULT '1000-01-01',
 exchangefee INT(11) NULL DEFAULT '0',
 totalamount INT(11) NULL DEFAULT '0',
 issueamount INT(11) NULL DEFAULT '0',
 isdeleted TINYINT(4) NULL DEFAULT '0',
 createdate TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX couponid (couponid)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO exchangecoupons(couponid, startdate, enddate, exchangefee, totalamount, issueamount) VALUES
(15, '2021-03-01', '2021-12-01', 1000, 99999, 0),
(16, '2021-03-01', '2021-12-01', 2000, 99999, 0);



CREATE TABLE shops (
 id INT(11) NOT NULL AUTO_INCREMENT,
 code VARCHAR(16) NULL DEFAULT '' COLLATE 'utf8mb4_bin',
 name VARCHAR(64) NULL DEFAULT '' COLLATE 'utf8mb4_bin',
 logo TEXT NULL COLLATE 'utf8mb4_bin',
 phone VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
 businesshours TEXT NULL COLLATE 'utf8mb4_bin',
 location TEXT NULL COLLATE 'utf8mb4_bin',
 locationimage TEXT NULL COLLATE 'utf8mb4_bin',
 website TEXT NULL COLLATE 'utf8mb4_bin',
 createdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX code (code),
 INDEX name (name)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO shops(code, name, phone, businesshours, website) VALUES
('S001', 'McDonalds', '12345678', '0900 - 1800', 'https://www.google.com.sg'),
('S002', 'KFC', '12345678', '0900 - 1800', 'https://www.google.com.sg'),
('S003', 'Burger King', '12345678', '0900 - 1800', 'https://www.google.com.sg');



CREATE TABLE promocode (
 id INT(11) NOT NULL AUTO_INCREMENT,
 code VARCHAR(30) NOT NULL COLLATE 'utf8mb4_bin',
 amount_claimable INT(11) NOT NULL DEFAULT 0,
 claimed_amount INT(11) NOT NULL DEFAULT 0,
 is_deleted TINYINT(4) NOT NULL DEFAULT 0,
 start_date DATE NULL DEFAULT '1000-01-01',
 end_date DATE NULL DEFAULT '1000-01-01',
 created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 UNIQUE KEY code (code),
 INDEX (code)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO promocode(code, amount_claimable, claimed_amount, is_deleted, start_date, end_date) VALUES
('SAMPLE001', 9999, 0, 0, '2021-01-01', '2031-01-01'),
('SAMPLE002', 9999, 0, 0, '2019-01-01', '2020-01-01');



CREATE TABLE promocoupon (
 id INT(11) NOT NULL AUTO_INCREMENT,
 promo_code_id INT(11) NOT NULL,
 coupon_id INT(11) NOT NULL,
 created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO promocoupon(promo_code_id, coupon_id) VALUES
(1, 13),
(1, 14),
(1, 15),
(2, 15);


--######################################################
--//////////////////////////////////////////////////////
--######################################################
CREATE DATABASE snapshop_wallet;
USE snapshop_wallet;

CREATE TABLE transfer (
 id INT(11) NOT NULL AUTO_INCREMENT,
 telegram_id VARCHAR(50) NULL DEFAULT NULL,
 transfer_code VARCHAR(50) NULL DEFAULT NULL,
 used TINYINT(4) NULL DEFAULT '0',
 telegram_username VARCHAR(50) NULL DEFAULT NULL,
 email VARCHAR(160) NULL DEFAULT NULL,
 gender VARCHAR(10) NULL DEFAULT NULL,
 referralcode VARCHAR(50) NULL DEFAULT NULL,
 newuserbonustracker INT(11) NOT NULL DEFAULT '1',
 newuserlogindate DATE NOT NULL DEFAULT '1000-01-01',
 bonustype TINYINT(4) NOT NULL DEFAULT '0',
 created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX telegram_id (telegram_id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;


CREATE TABLE transfer_assets (
 id INT(11) NOT NULL AUTO_INCREMENT,
 telegram_id VARCHAR(50) NULL DEFAULT NULL,
 asset_type VARCHAR(50) NULL DEFAULT NULL,
 asset_id INT(11) NULL DEFAULT NULL,
 asset_value INT(11) NULL DEFAULT NULL,
 expiry_date DATE NULL DEFAULT NULL,
 created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id),
 INDEX telegram_id (telegram_id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;



CREATE TABLE weeklyloginhistory (
 id INT(11) NOT NULL AUTO_INCREMENT,
 telegram_id VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',
 date_claimed DATE NOT NULL,
 createdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;



CREATE TABLE usercouponhistory (
 id INT(11) NOT NULL AUTO_INCREMENT,
 telegram_id VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_bin',
 from_action VARCHAR(20) NULL DEFAULT '' COLLATE 'utf8mb4_bin',
 coupon_id INT(11) NULL DEFAULT '0',
 createdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;



--######################################################
--//////////////////////////////////////////////////////
--######################################################
CREATE DATABASE snapshop_quest;
USE snapshop_quest;

CREATE TABLE quests (
 id INT(11) NOT NULL AUTO_INCREMENT,
 quest_title TEXT NOT NULL COLLATE 'utf8mb4_bin',
 quest_description TEXT NOT NULL COLLATE 'utf8mb4_bin',
 start_date DATE DEFAULT '1000-01-01',
 end_date DATE DEFAULT '1000-01-01',
 createdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB;

INSERT INTO quests(quest_title, quest_description, start_date, end_date) VALUES
('QUEST 1', 'SAMPLE QUEST 1', '2021-01-01', '2021-12-01'),
('QUEST 2', 'SAMPLE QUEST 2', '2021-01-01', '2021-12-01');



--######################################################
--//////////////////////////////////////////////////////
--######################################################
CREATE USER 'demo'@'%' IDENTIFIED BY 'password';

GRANT SELECT, UPDATE, INSERT, DELETE on snapshop_auth.* to 'demo'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE on snapshop_property.* to 'demo'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE on snapshop_wallet.* to 'demo'@'%';
GRANT SELECT, UPDATE, INSERT, DELETE on snapshop_quest.* to 'demo'@'%';