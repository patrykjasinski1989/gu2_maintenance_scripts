set serveroutput on;
declare
    imei_wrong varchar2(15) := '';
    imei_correct varchar2(15) := '';
    msisdn number(9) := 555555555;
    order_id number(8) := 44444444;
    v_imei varchar2(15);
    v_model_difference number(1);
begin
    select zpmp.param_value into v_imei 
    from rsw.rsw_zam_poz_materialne_param zpmp
    join rsw.rsw_zamowienia_lojalki zl on zl.id_lojalki = zpmp.id_zamowienia_lojalki 
    join rsw.rsw_zamowienia z on z.id_zamowienia = zl.id_zamowienia
    where zl.id_zamowienia = order_id and z.dn_num = msisdn 
    and zpmp.param_id = 'RSW_IMEI';
    if v_imei != imei_wrong then
        dbms_output.put_line('niezgodny istniejacy numer imei');
    else
        select count(1) into v_model_difference from (
        select mai.id_model_apr_ifs from rsw.rsw_model_apr_ifs mai
        join rsw.rsw_zestawy_imei zi on zi.id_model_apr_ifs = mai.id_model_apr_ifs
        where zi.imei = substr(imei_correct,1,6)
        minus
        select mai.id_model_apr_ifs from rsw.rsw_model_apr_ifs mai
        join rsw.rsw_zestawy_imei zi on zi.id_model_apr_ifs = mai.id_model_apr_ifs
        where zi.imei = substr(imei_wrong,1,6)
        );
        if v_model_difference > 0 then
            dbms_output.put_line('potencjalna niezgodnosc modeli');
        else
            update rsw.rsw_zam_poz_materialne_param
            set param_value = imei_correct
            where param_value = imei_wrong;
            if sql%rowcount = 1 then
                dbms_output.put_line('zrealizowano');
                commit;
            else 
                dbms_output.put_line('cos poszlo nie tak');
                rollback;
            end if;
        end if;
    end if;
end;
/