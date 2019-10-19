insert into ptk_otsa_trans_address_type select address_code, 1 from (
select distinct ta1.address_code from ptk_otsa_trans_address ta1 where ta1.trans_code in (
select t1.trans_code from ptk_otsa_transaction t1 where t1.status = '3C' --and t1.trans_type = 'S'
and t1.ncs_error_desc like 'Blad przetwarzania procesu: .....CSC.59_')
and not exists (select 1 from ptk_otsa_trans_address_type tat1 
where tat1.address_type = 1 and tat1.address_code = ta1.address_code));

update ptk_otsa_transaction set status = '1B' where status = '3C' --and trans_type = 'S'
and ncs_error_desc like 'Blad przetwarzania procesu: .....CSC.59_';

commit;