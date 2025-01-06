-- 创建文档信息库file_info表
CREATE TABLE file_info (
    file_name VARCHAR(255), -- 根据实际文件名长度需求调整VARCHAR长度
    file_id INT PRIMARY KEY,
    remote_file VARCHAR(255) -- 根据实际文件地址长度需求调整VARCHAR长度
);
-- 创建识别结果库content_info表
CREATE TABLE content_info (
    id INT PRIMARY KEY,
    file_id INT,
    content TEXT, -- 识别内容可能较长，使用TEXT类型，可按需调整
    FOREIGN KEY (file_id) REFERENCES file_info(file_id)
);

-- 创建文档编辑库edit_info表
CREATE TABLE edit_info (
    id INT PRIMARY KEY,
    res_id INT,
    new_content TEXT, -- 新内容也可能较长，使用TEXT类型，可按需调整
    time DATETIME, -- 根据实际时间记录精度需求，也可使用TIMESTAMP等类型
    FOREIGN KEY (res_id) REFERENCES content_info(id)
);
-- 创建下载信息库download_info表
CREATE TABLE download_info (
    id INT PRIMARY KEY,
    file_id INT,
    file_name VARCHAR(255),
    file_address VARCHAR(255),
    FOREIGN KEY (file_id) REFERENCES file_info(file_id)
);
