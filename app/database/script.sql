CREATE DATABASE politics_chatbot;
GO
USE politics_chatbot;
GO
CREATE TABLE Articles
(
    id_art INT IDENTITY(1,1) PRIMARY KEY,   
    links TEXT NOT NULL                    
);
