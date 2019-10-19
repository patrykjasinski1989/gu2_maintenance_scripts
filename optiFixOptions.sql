declare
    cursor c1 is select * from ptk_otsa_transaction 
    where status = '3C' and 
    (ncs_error_desc like 'Jednoczesne wystapienie nagrod%' or
    ncs_error_desc like 'Wiele nagrod na jedna usluge%');
begin
    for loop_trans in c1
    loop
        delete from ptk_otsa_contr_option 
        where contract_code in (
            select contract_code from ptk_otsa_trans_contract 
            where trans_code = loop_trans.trans_code) 
        and option_code = 229080;
        update ptk_otsa_transaction set status = '1B'
        where trans_code = loop_trans.trans_code;
        commit;
    end loop loop_trans;
end;
/
