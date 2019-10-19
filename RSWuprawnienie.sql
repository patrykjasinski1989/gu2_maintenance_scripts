declare
    v_msisdn rsw.rsw_zamowienia.dn_num%type := '555555555';
    v_id_oferty rsw.rsw_uprawnienia.id_oferty%type := '3624';
    v_co_id rsw.rsw_zamowienia.co_id%type;
    v_ins_prod_id rsw.rsw_zamowienia.ins_prod_id%type;
begin
    select max(co_id) into v_co_id from rsw.rsw_zamowienia where dn_num = v_msisdn;
    select max(ins_prod_id) into v_ins_prod_id from rsw.rsw_zamowienia where dn_num = v_msisdn;
    insert into rsw.rsw_uprawnienia (co_id, co_expir_date, data_upawnienia, data_waznosci, user_id, id_oferty, staz, ins_prod_id, msisdn, ignorowanie_warunkow_oferty)
    values (v_co_id, trunc(sysdate), trunc(sysdate), trunc(sysdate+365), 'patjasinski2', v_id_oferty, null, v_ins_prod_id, v_msisdn, 1);
end;
/