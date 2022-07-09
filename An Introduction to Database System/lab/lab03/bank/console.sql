drop table if exists Account;

drop table if exists Checking;

drop table if exists Pay;

drop table if exists Bank;

drop table if exists Cheque_Account;

drop table if exists Client;

drop table if exists Contact;

drop table if exists Department;

drop table if exists Employee;

drop table if exists Loan;

drop table if exists Own;

drop table if exists Saving_Account;

drop table if exists Service;

# 账户(账户号，支行名，余额，开户日期)
create table Account
(
   Account_ID varchar(50) not null,
   Bank_Name varchar(50) not null,
   Balance float(15),
   Opening_Date date,
   primary key (Account_ID)
);

# 支付(用户号，贷款号，支付号，支付金额，支付日期)
create table Pay
(
   Client_ID varchar(50) not null,
--    Loan_ID varchar(50) not null,
   Loan_ID varchar(50),
   Pay_ID varchar(50) not null,
   Pay_Amount float(15),
   Pay_Date date,
   primary key (Client_ID, Loan_ID, Pay_ID)
);

# 支行(支行，城市，资产)
create table Bank(
   Bank_Name varchar(50) not null,
   City varchar(50) not null,
   Assets float(15) not null,
   primary key (Bank_Name)
);

# 支票账户(账户号，透支额)
create table Cheque_Account
(
   Account_ID varchar(50) not null,
   Overdraft float(15),
   primary key (Account_ID)
);

# 客户(客户号，客户名，客户电话，客户地址)
create table Client
(
   Client_ID varchar(50) not null,
   Client_Name varchar(50) not null,
   Client_Tel varchar(50),
   Client_Address varchar(50),
   primary key (Client_ID)
);

# 联系人(客户号，联系人名，联系人邮箱，联系人电话，联系人和客户的关系)
create table Contact
(
   Client_ID varchar(50) not null,
   Contact_Name varchar(50) not null,
   Contact_Email varchar(50),
   Contact_Tel varchar(50),
   Relation varchar(50),
   primary key (Client_ID, Contact_Name)
);

-- create table Client
-- (
--       Client_ID varchar(50) not null,
--       Client_Name varchar(50) not null,
--       Client_Tel int,
--       Client_Address varchar(50),
--       Contact_Name varchar(50) not null,
--       Contact_Email varchar(50),
--       Contact_Tel int,
--       Relation varchar(50),
--       primary key (Client_ID)
-- )

# 部门(部门号，部门名，部门类型，经理身份证号)
create table Department
(
   Department_ID varchar(50) not null,
   Department_Name varchar(50) not null,
   Department_Type varchar(50),
   Manager_ID varchar(50),
   primary key (Department_ID)
);

# 员工(员工号，员工名，支行名，部门名，员工电话，员工地址，入职日期)
create table Employee
(
   Employee_ID varchar(50) not null,
   Employee_Name varchar(50) not null,
   Bank_Name varchar(50) not null,
   Department_ID varchar(50),
   Employee_Tel varchar(50),
   Employee_Address varchar(50),
   Work_Date date,
   primary key (Employee_ID)
);

# 贷款(贷款号，支行名，贷款总额，状态，已支付贷款)
create table Loan
(
   Loan_ID varchar(50) not null,
   Bank_Name varchar(50) not null,
   Loan_Amount float(15) not null,
   Loan_Status int default 0 not null,
   Pay_already float(15) not null,
   Opening_Date date,
   primary key (Loan_ID)
);

# 持有(客户号，最近访问日期，账户名)
create table Own
(
   Client_ID varchar(50) not null,
   Visited_Date date,
   Account_ID varchar(50),
   primary key (Client_ID, Account_ID)
);

# 开户约束(客户号，银行名，账户类型)
create table Checking
(
   Client_ID varchar(50) not null,
   Bank_Name varchar(50) not null,
   Account_Type int not null,
   primary key (Client_ID, Bank_Name, Account_Type)
);

# 储蓄账户(账户号，利率，货币类型)
create table Saving_Account
(
   Account_ID varchar(50) not null,
   Interest_Rate float(15),
   Currency_Type varchar(50),
   primary key (Account_ID)
);

# 服务(客户号，员工号，服务类型：该员工是此客户的贷款负责人或银行帐户负责人)
create table Service
(
   Client_ID varchar(50) not null,
   Employee_ID varchar(50) not null,
   Service_Type varchar(50),
   primary key (Client_ID, Employee_ID)
);


alter table Account add constraint FK_Open foreign key (Bank_Name)
      references Bank (Bank_Name) on delete restrict on update restrict;

alter table Pay add constraint FK_Apply foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

-- alter table Pay drop foreign key FK_Apply;

-- alter table Pay add constraint FK_Apply2 foreign key (Loan_ID)
--       references Loan (Loan_ID) on delete restrict on update restrict;
-- alter table Pay add constraint FK_Apply2 foreign key (Loan_ID)
--       references Loan (Loan_ID) on delete set null on update restrict;

alter table Pay drop foreign key FK_Apply2;

alter table Cheque_Account add constraint FK_Account_Type foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

alter table Contact add constraint FK_Have foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

-- alter table Contact drop foreign key FK_Have;

alter table Employee add constraint FK_Belong_To foreign key (Department_ID)
      references Department (Department_ID) on delete restrict on update restrict;

alter table Employee add constraint FK_Employ foreign key (Bank_Name)
      references Bank (Bank_Name) on delete restrict on update restrict;

alter table Loan add constraint FK_Make_Loan foreign key (Bank_Name)
      references Bank (Bank_Name) on delete restrict on update restrict;

alter table Own add constraint FK_Own1 foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

-- alter table Own drop foreign key FK_Own1;

alter table Own add constraint FK_Own2 foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

alter table Saving_Account add constraint FK_Account_Type2 foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

-- alter table Own drop foreign key FK_Own2;

-- alter table Saving_Account drop foreign key FK_Account_Type2;

alter table Service add constraint FK_Service foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

-- alter table Service drop foreign key FK_Service;

alter table Service add constraint FK_Service2 foreign key (Employee_ID)
      references Employee (Employee_ID) on delete restrict on update restrict;

alter table Checking add constraint FK_Checking1 foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

-- alter table Checking drop foreign key FK_Checking1;

alter table Checking add constraint FK_Checking2 foreign key (Bank_Name)
      references Bank (Bank_Name) on delete restrict on update restrict;