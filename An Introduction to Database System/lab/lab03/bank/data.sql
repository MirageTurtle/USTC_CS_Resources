insert into bank(Bank_Name, City, Assets) values('ICBC', 'Beijing', 27000000);
insert into bank(Bank_Name, City, Assets) values('CCB', 'Beijing', 2720000);
insert into bank(Bank_Name, City, Assets) values('合肥支行', 'Anhui', 270000);

insert into Client(Client_ID, Client_Name, Client_Tel, Client_Address) values('0000', '张三', '12345678', '中科大西区');
insert into Contact(Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation) values('0000', '李四', 'lisi@email.com', '87654321', '同学');

insert into Department(Department_ID, Department_Name, Department_Type, Manager_ID) values('0000', 'Test', 'Test', '1000');
insert into Department(Department_ID, Department_Name, Department_Type, Manager_ID) values('0001', 'Sale', 'Sale', '1001');
insert into Department(Department_ID, Department_Name, Department_Type, Manager_ID) values('0002', 'Personnel', 'Personnel', '1002');

insert into Employee(Employee_ID, Employee_Name, Bank_Name, Department_ID, Employee_Tel, Employee_Address, Work_Date) values('1000', 'Test', '合肥支行', '0000', '10010001000', '安徽合肥中科大', '2022-05-26');