drop table Borrow;
create table Borrow(
    book_ID char(8),
    Reader_ID char(8),
    Borrow_Date date,
    Return_Date date,
    Constraint PK_Borrow Primary Key(book_ID, Reader_ID),
    Constraint FK_Borrow_Book Foreign Key(book_ID) References Book(ID),
    Constraint FK_Borrow_Reader Foreign Key(Reader_ID) References Reader(ID)
);
Delimiter //
create trigger borrow_book after insert on Borrow for each row
begin
    if new.Return_Date is NULL then
        update Book set status = 1 where Book.ID = new.book_ID;
    elseif new.Return_Date is NOT NULL then
        update Book set status = 0 where Book.ID = new.book_ID;
    end if;
end //
Delimiter ;
Delimiter //
create trigger return_book after update on Borrow for each row
begin
    if old.book_ID = new.book_ID and old.Return_Date is NULL and new.Return_Date is NOT NULL then
        update Book set status = 0 where Book.ID = new.book_ID;
    end if;
end //
Delimiter ;
insert into Borrow value('b5','r1',  '2021-03-12', '2021-04-07');
insert into Borrow value('b6','r1',  '2021-03-08', '2021-03-19');
insert into Borrow value('b11','r1',  '2021-01-12', '2021-05-19');

insert into Borrow value('b3', 'r2', '2021-02-22', '2021-03-10');
insert into Borrow value('b9', 'r2', '2021-02-22', '2021-04-10');
insert into Borrow value('b7', 'r2', '2021-04-11', NULL);

insert into Borrow value('b1', 'r3', '2021-04-02', '2021-07-19');
insert into Borrow value('b2', 'r3', '2021-04-02', '2021-07-19');
insert into Borrow value('b4', 'r3', '2021-04-02', '2021-04-09');
-- check_book_status error because of insert b7
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
call check_book_status(@num);
-- update Book set status = 1 where Book.ID = 'b3';
select @num;

select Book.ID, Book.status, Borrow.Return_Date from Book, Borrow where Book.ID=Borrow.book_ID and Book.ID='b14';
update Borrow set Return_Date='2022-04-15' where book_ID='b14';
select Book.ID, Book.status, Borrow.Return_Date from Book, Borrow where Book.ID=Borrow.book_ID and Book.ID='b14';
select @num;