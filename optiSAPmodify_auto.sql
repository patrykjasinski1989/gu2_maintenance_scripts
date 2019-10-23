create table sap_order_notes_backup as select * from ptk_sap_order where trans_code in (
    select t.trans_code from ptk_otsa_transaction t where t.status='3C' 
    and (t.ncs_error_desc like 'SAP service SalesOrderModify returned an E status%'
        or t.ncs_error_desc = 'Blad przetwarzania procesu: .....SSOM.197'
        or t.ncs_error_desc = 'Blad przetwarzania procesu: Index: 0, Size: 0')
    );

update OTSA.PTK_SAP_ORDER so set so.NOTES = 'CANCELED' where so.TRANS_CODE in (
select trans_code from sap_order_notes_backup);
update OTSA.PTK_OTSA_TRANSACTION t set t.STATUS = '1B', t.NCS_ERROR_DESC = null where t.TRANS_CODE in (
select trans_code from sap_order_notes_backup);
commit;

exec dbms_lock.sleep(30);

begin
    for c1 in (select trans_code, notes from sap_order_notes_backup)
    loop
        update OTSA.PTK_SAP_ORDER so set so.NOTES = c1.notes
        where so.TRANS_CODE = c1.trans_code;
    end loop;
    commit;
end;
/

drop table sap_order_notes_backup;
