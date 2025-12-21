-- Table, Trigger 등을 생성합니다. 초깃값이므로 최초 한 번만 실행합니다.
-- 전체 코드 백앤드팀 정유림님 작성(테이블, 트리거 작성 코드)
-- 1-1) 마약 종류 
CREATE TABLE tbl_Drug_Types ( 
    DrugID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    DrugCode VARCHAR(20) NOT NULL UNIQUE, 
    DrugWord VARCHAR(100), 
    DrugEffect TEXT 
); 

DELIMITER $$ 
CREATE TRIGGER trg_before_insert_drug_types 
BEFORE INSERT ON tbl_Drug_Types 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_Drug_Types'; 
    IF NEW.DrugID IS NULL THEN 
        SET NEW.DrugID = next_id; 
    END IF; 
    SET NEW.DrugCode = CONCAT('DC', LPAD(NEW.DrugID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 1-2) 마약 데이터 
CREATE TABLE tbl_Drug_Data_Raw ( 
    DrugDataID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    DrugDataCode VARCHAR(20) NOT NULL UNIQUE, 
    DrugText TEXT NOT NULL, 
    DrugWriting VARCHAR(50) NOT NULL, 
    UproadType VARCHAR(50) NOT NULL, 
    snsType VARCHAR(30) NOT NULL 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_drug_data_raw 
BEFORE INSERT ON tbl_Drug_Data_Raw 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_Drug_Data_Raw'; 
    IF NEW.DrugDataID IS NULL THEN 
        SET NEW.DrugDataID = next_id; 
    END IF; 
    SET NEW.DrugDataCode = CONCAT('DR', LPAD(NEW.DrugDataID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 3-1) 마약 데이터(사용자) 
CREATE TABLE tbl_User_Drug_Data ( 
    UserDrugID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    UserDrugCode VARCHAR(20) NOT NULL UNIQUE, 
    UserText TEXT NOT NULL, 
    InputSourceType VARCHAR(30) NOT NULL, 
    SNSType VARCHAR(30), 
    DetectionResult VARCHAR(50) 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_user_drug_data 
BEFORE INSERT ON tbl_User_Drug_Data 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_User_Drug_Data'; 
    IF NEW.UserDrugID IS NULL THEN 
        SET NEW.UserDrugID = next_id; 
    END IF; 
    SET NEW.UserDrugCode = CONCAT('UD', LPAD(NEW.UserDrugID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 1-3) 은어 사전 (1-1 연결) 
CREATE TABLE tbl_Slangs ( 
    SlangsID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    slangsCode VARCHAR(20) NOT NULL UNIQUE, 
    term VARCHAR(100) NOT NULL, 
    definition TEXT, 
    relatedTerm VARCHAR(255), 
    example TEXT, 
    catagory VARCHAR(50), 
    DrugType VARCHAR(20), 
    FOREIGN KEY (DrugType) REFERENCES tbl_Drug_Types(DrugCode) 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_slangs 
BEFORE INSERT ON tbl_Slangs 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_Slangs'; 
    IF NEW.SlangsID IS NULL THEN 
        SET NEW.SlangsID = next_id; 
    END IF; 
    SET NEW.slangsCode = CONCAT('SC', LPAD(NEW.SlangsID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 2-1) 은어 사용 횟수 (1-2, 1-3 연결) 
CREATE TABLE tbl_Slang_Usage_Count ( 
    UseID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    UseCode VARCHAR(20) NOT NULL UNIQUE, 
    articleID VARCHAR(20) NOT NULL, 
    SlangsID VARCHAR(20) NOT NULL, 
    count INT NOT NULL, 
    FOREIGN KEY (articleID) REFERENCES tbl_Drug_Data_Raw(DrugDataCode), 
    FOREIGN KEY (SlangsID) REFERENCES tbl_Slangs(slangsCode) 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_slang_usage_count 
BEFORE INSERT ON tbl_Slang_Usage_Count 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 
'tbl_Slang_Usage_Count'; 
    IF NEW.UseID IS NULL THEN 
        SET NEW.UseID = next_id; 
    END IF; 
    SET NEW.UseCode = CONCAT('UC', LPAD(NEW.UseID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 2-2) 마약 은어 탐지 (3-1, 2-3 연결) 
CREATE TABLE tbl_Slang_Detection ( 
    SlangDetectionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    SlangDetectionCode VARCHAR(20) NOT NULL UNIQUE, 
    InputText TEXT NOT NULL, 
    LLM_Reason TEXT, 
    DataType VARCHAR(30), 
    UserDrugCode VARCHAR(20),      
    FOREIGN KEY (UserDrugCode) REFERENCES tbl_User_Drug_Data(UserDrugCode) 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_slang_detection 
BEFORE INSERT ON tbl_Slang_Detection 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_Slang_Detection'; 
    IF NEW.SlangDetectionID IS NULL THEN 
        SET NEW.SlangDetectionID = next_id; 
    END IF; 
    SET NEW.SlangDetectionCode = CONCAT('SD', LPAD(NEW.SlangDetectionID, 6, '0')); 
END$$ 
DELIMITER ; 
 -- 3-2) 은어 사전 (사용자) 
CREATE TABLE tbl_User_Slangs ( 
    UserSlangsID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    UserSlangsCode VARCHAR(20) NOT NULL UNIQUE, 
    UserTerm VARCHAR(100) NOT NULL, 
    UserDefinition TEXT, 
    UserRelatedTerm VARCHAR(255), 
    UserCatagory VARCHAR(50), 
    DrugType VARCHAR(100), 
    FOREIGN KEY (DrugType) REFERENCES tbl_Drug_Types(DrugCode) 
 
); 
 
DELIMITER $$ 
CREATE TRIGGER trg_before_insert_user_slangs 
BEFORE INSERT ON tbl_User_Slangs 
FOR EACH ROW 
BEGIN 
    DECLARE next_id INT; 
    SELECT AUTO_INCREMENT INTO next_id 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tbl_User_Slangs'; 
    IF NEW.UserSlangsID IS NULL THEN 
        SET NEW.UserSlangsID = next_id; 
    END IF; 
    SET NEW.UserSlangsCode = CONCAT('US', LPAD(NEW.UserSlangsID, 6, '0')); 
END$$ 
DELIMITER ; 
 