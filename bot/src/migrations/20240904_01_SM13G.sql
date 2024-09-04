CREATE TABLE IF NOT EXISTS companies (
  	sheet_id VARCHAR(20) NOT NULL PRIMARY KEY,
  	title VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS company_data (
	id SERIAL NOT NULL PRIMARY KEY,
	company_id VARCHAR(20) NOT NULL,
	month VARCHAR(20) NOT NULL,
	income FLOAT,
	expences FLOAT,
	profit FLOAT,
	KPN FLOAT,

	UNIQUE (company_id, month),

	CONSTRAINT fk_data_company
      FOREIGN KEY(company_id)
	  REFERENCES companies(sheet_id)
	  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chats (
  	user_id VARCHAR(20) NOT NULL PRIMARY KEY,
  	graphic_message_id VARCHAR(20),
	selected_company_id VARCHAR(20),
	selected_company_option VARCHAR(20),


	CONSTRAINT fk_chat_company
      FOREIGN KEY(selected_company_id)
	  REFERENCES companies(sheet_id)
	  ON DELETE SET NULL
);


