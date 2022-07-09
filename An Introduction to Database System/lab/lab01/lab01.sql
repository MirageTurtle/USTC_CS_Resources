use library;
-- create the basic tables
create table Book(
    ID char(8),
    name varchar(10) NOT NULL,
    author varchar(10),
    price float,
    status int DEFAULT 0,
    Constraint PK_Book Primary Key(ID)
);
create table Reader(
    ID char(8),
    name varchar(10),
    age int,
    address varchar(20),
    Constraint PK_Reader Primary Key(ID)
);
create table Borrow(
    book_ID char(8),
    Reader_ID char(8),
    Borrow_Date date,
    Return_Date date,
    Constraint PK_Borrow Primary Key(book_ID, Reader_ID),
    Constraint FK_Borrow_Book Foreign Key(book_ID) References Book(ID),
    Constraint FK_Borrow_Reader Foreign Key(Reader_ID) References Reader(ID)
);
-- insert some data for test
-- 插入书籍
insert into Book value('b1', '数据库系统实现', 'Ullman', 59.0, 0);
insert into Book value('b2', '数据库系统概念', 'Abraham', 59.0, 1);
insert into Book value('b3', 'C++ Primer', 'Stanley', 78.6, 0);
insert into Book value('b4', 'Redis设计与实现', '黄建宏', 79.0, 1);
insert into Book value('b5', '人类简史', 'Yuval', 68.00, 0);
insert into Book value('b6', '史记(公版)', '司马迁', 220.2, 1);
insert into Book value('b7', 'Oracle编程艺术', 'Thomas', 43.1, 1);
insert into Book value('b8', '分布式系统及其应用', '邵佩英', 30.0, 0);
insert into Book value('b9', 'Oracle管理', '张立杰', 51.9, 1);
insert into Book value('b10', '数理逻辑', '汪芳庭', 22.0, 0);
insert into Book value('b11', '三体', '刘慈欣', 23.0, 0);
insert into Book value('b12', 'Fun python', 'Luciano', 354.2, 1);
insert into Book value('b13', 'Learn SQL', 'Seyed', 23.0, 1);
insert into Book value('b14', 'Perl&MySQL', '徐泽平', 23.0, 1);

-- 插入读者
insert into Reader value('r1', '李林', 18, '中国科学技术大学东校区');
insert into Reader value('r2', 'Rose', 22, '中国科学技术大学北校区');
insert into Reader value('r3', '罗永平', 23, '中国科学技术大学西校区');
insert into Reader value('r4', 'Nora', 26, '中国科学技术大学北校区');
insert into Reader value('r5', '汤晨', 22, '先进科学技术研究院');
insert into Reader value('r6', '李小一', 18, '中国科学技术大学东校区');
insert into Reader value('r7', '王二', 22, '中国科学技术大学北校区');
insert into Reader value('r8', '赵三', 23, '中国科学技术大学西校区');
insert into Reader value('r9', '魏四', 26, '中国科学技术大学北校区');
insert into Reader value('r10', '汤大晨', 22, '先进科学技术研究院');
insert into Reader value('r11', '李平', 18, '中国科学技术大学东校区');
insert into Reader value('r12', 'Lee', 22, '中国科学技术大学北校区');
insert into Reader value('r13', 'Jack', 23, '中国科学技术大学西校区');
insert into Reader value('r14', 'Bob', 26, '中国科学技术大学北校区');
insert into Reader value('r15', '李晓', 22, '先进科学技术研究院');
insert into Reader value('r16', '王林', 18, '中国科学技术大学东校区');
insert into Reader value('r17', 'Mike', 22, '中国科学技术大学北校区');
insert into Reader value('r18', '范维', 23, '中国科学技术大学西校区');
insert into Reader value('r19', 'David', 26, '中国科学技术大学北校区');
insert into Reader value('r20', 'Vipin', 22, '先进科学技术研究院');
insert into Reader value('r21', '林立', 18, '中国科学技术大学东校区');
insert into Reader value('r22', '张悟', 22, '中国科学技术大学北校区');
insert into Reader value('r23', '袁平', 23, '中国科学技术大学西校区');

-- 插入借书
insert into Borrow value('b5','r1',  '2021-03-12', '2021-04-07');
insert into Borrow value('b6','r1',  '2021-03-08', '2021-03-19');
insert into Borrow value('b11','r1',  '2021-01-12', '2021-05-19');

insert into Borrow value('b3', 'r2', '2021-02-22', '2021-03-10');
insert into Borrow value('b9', 'r2', '2021-02-22', '2021-04-10');
insert into Borrow value('b7', 'r2', '2021-04-11', NULL);

insert into Borrow value('b1', 'r3', '2021-04-02', '2021-07-19');
insert into Borrow value('b2', 'r3', '2021-04-02', '2021-07-19');
insert into Borrow value('b4', 'r3', '2021-04-02', '2021-04-09');
insert into Borrow value('b7', 'r3', '2021-04-02', '2021-04-09');

insert into Borrow value('b6', 'r4', '2021-03-31', NULL);
insert into Borrow value('b12', 'r4', '2021-03-31', '2021-07-19');

insert into Borrow value('b4', 'r5', '2021-04-10', NULL);
insert into Borrow value('b11','r5',  '2021-08-12', '2021-09-19');

insert into Borrow value('b3', 'r6', '2021-04-10', '2022-01-01');

insert into Borrow value('b1', 'r7', '2021-08-10', '2021-12-19');

insert into Borrow value('b1', 'r8', '2022-01-10', '2022-02-19');
insert into Borrow value('b5','r8',  '2021-07-12', '2021-10-07');

insert into Borrow value('b1', 'r9', '2022-03-10', '2022-03-19');
insert into Borrow value('b2', 'r9', '2022-03-10', '2021-03-19');

insert into Borrow value('b2', 'r10', '2022-03-20', NULL);
insert into Borrow value('b5','r10',  '2021-05-12', '2021-06-07');
insert into Borrow value('b11','r10',  '2021-10-12', '2021-11-19');

insert into Borrow value('b3', 'r12', '2021-04-10', '2021-08-19');

insert into Borrow value('b3', 'r13', '2021-09-10', '2021-12-19');

insert into Borrow value('b3', 'r14', '2022-01-10', NULL);

insert into Borrow value('b9', 'r15', '2021-04-19', '2021-08-19');

insert into Borrow value('b9', 'r16', '2021-10-10', '2021-12-19');

insert into Borrow value('b9', 'r17', '2022-01-10', NULL);
insert into Borrow value('b11','r17',  '2021-12-12', '2022-01-19');

insert into Borrow value('b12', 'r18', '2021-10-10', '2021-12-19');
insert into Borrow value('b13', 'r18', '2021-10-10', '2021-12-19');

insert into Borrow value('b13', 'r19', '2022-01-10', NULL);
insert into Borrow value('b5','r19',  '2022-01-12', '2022-03-07');


insert into Borrow value('b8', 'r20', '2022-01-10', '2022-02-19');

insert into Borrow value('b14', 'r22', '2021-10-10', '2021-12-19');

insert into Borrow value('b14', 'r23', '2022-01-10', NULL);

-- ! 复习时备注：很多地方其实应该用id而非name，因为id是主键，name可能重名

-- 查询读者 Rose 的读者号和地址
select ID, address from Reader where name='Rose';
-- 查询读者 Rose 所借阅读书(包括已还和未还图书)的图书名和借期
select book_ID, Borrow_Date from Reader, Borrow where Reader.ID=Borrow.Reader_ID and Reader.name='Rose';
-- 查询未借阅图书的读者姓名;
select name from Reader where NOT EXISTS (Select * from Borrow where Reader.ID=Borrow.Reader_ID);
-- 查询 Ullman 所写的书的书名和单价
select name, price from Book where author='Ullman';
-- 查询读者“李林”借阅未还的图书的图书号和书名
select Book.ID, Book.name from Book, Reader, Borrow where Book.ID=Borrow.book_ID and Reader.ID=Borrow.Reader_ID and Reader.name='李林' and Borrow.Return_Date is NULL;
-- 查询借阅图书数目超过 3 本的读者姓名
select name from Reader, Borrow where Reader.ID=Borrow.Reader_ID group by Reader.name having count(Borrow.book_ID) > 3;
-- 查询没有借阅读者“李林”所借的任何一本书的读者姓名和读者号
-- 对于一个给定的读者，不存在一本书是李林借过的
-- TODO: 感觉实现不是很优雅
select name, ID from Reader where NOT EXISTS (select * from Book, Borrow where Book.ID=Borrow.book_ID and Reader.ID=Borrow.Reader_ID and Book.name IN (select Book.name from Book, Reader, Borrow where Book.ID=Borrow.book_ID and Reader.ID=Borrow.Reader_ID and Reader.name='李林'));
-- 查询书名中包含“MySQL”的图书书名及图书号
select name, ID from Book where name LIKE '%MySQL%';
-- 查询 2021 年借阅图书数目排名前 20 名的读者号、姓名、年龄以及借阅图书数
select name from Reader, Borrow where Reader.ID=Borrow.Reader_ID group by Reader.name order by count(Borrow.book_ID) DESC limit 20;
-- 创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名和借期
create view borrow_view (Reader_ID, Reader_name, Book_ID, Book_name, Borrow_date) as select Reader.ID, Reader.name, Book.ID, Book.name, Borrow.Borrow_Date from Book, Reader, Borrow where Reader.ID=Borrow.Reader_ID and Book.ID=Borrow.Book_ID;
-- 并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数
select Reader_ID, count(*) from borrow_view where DATEDIFF(NOW(), borrow_view.Borrow_date) <=365 group by Reader_ID;

-- 设计一个存储过程，实现对 Book 表的 ID 的修改(本题要求不得使用外键定义时的 on update cascade 选项，因为该选项不是所有 DBMS 都支持)。
Delimiter //
create procedure update_book_id(in old_id varchar(8), in new_id varchar(8), out state int)
begin
    declare s int DEFAULT 0;
    declare num int;
    declare continue handler for NOT FOUND set s = 1;
    declare continue handler for SQLEXCEPTION set s = 2;
    alter table Borrow drop constraint FK_Borrow_Book;
    select count(*) from book where ID=old_id into num;
    if num = 0 then
        set s = 3;
    end if;
    update Book set ID=new_id where ID=old_id;
    update Borrow set book_ID=new_id where book_ID=old_id;
    alter table Borrow add constraint FK_Borrow_Book Foreign Key(book_ID) References Book(ID);
    set state = s;
    if s = 0 then
        commit;
    else
        rollback;
    end if;
end //
Delimiter;
-- 设计一个存储过程，检查每本图书 status 是否正确，并返回 status 不正确的图书数。
Delimiter //
create procedure check_book_status(out wrong_num int)
begin
    declare num int DEFAULT 0;
    declare s int DEFAULT 0;
    declare continue handler for NOT FOUND set s = 1;

    select count(*) from Book where EXISTS (select * from Borrow where Book.ID = Borrow.book_ID and Borrow.Return_Date is NULL) and status != 1 into num;
    set wrong_num = num;
    select count(*) from Book where NOT EXISTS (select * from Borrow where Book.ID = Borrow.book_ID and Borrow.Return_Date is NULL) and status != 0 into num;
    set wrong_num = wrong_num + num;
end //
Delimiter;
-- 设计触发器，实现:当一本书被借出时，自动将 Book 表中相应图书的 status 修改为 1;当某本书被归还时，自动将 status 改为 0。
Delimiter //
create trigger borrow_book after insert on Borrow for each row
begin
    if new.Return_Date is NULL then
        update Book set status = 1 where Book.ID = new.book_ID;
    end if;
end //
Delimiter;
Delimiter //
create trigger return_book after update on Borrow for each row
begin
    if old.book_ID = new.book_ID and old.Return_Date is NULL and new.Return_Date is NOT NULL then
        update Book set status = 0 where Book.ID = new.book_ID;
    end if;
end //
Delimiter;