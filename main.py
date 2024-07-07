import time

import streamlit as st

from bot import main, message

st.set_page_config(page_title="Ponto SMS", page_icon=':tiger:')

st.subheader('Consulta ponto digital SMS')

form = st.form(key='Consulta do ponto eletrônico - SMS', clear_on_submit=True)

with form:
    cpf = st.text_input(key='cpf', label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')

    col_1, col_2 = st.columns(2)

    with col_1:
        date_start = st.date_input(key='date_start', label='Selecione a data inicial', format='DD/MM/YYYY', value=None)
    with col_2:
        date_end = st.date_input(key='date_end', label='Selecione a data final', format='DD/MM/YYYY', value=None)

    btn_submit: bool = st.form_submit_button('Gerar arquivo :thumbsup:')

if cpf and date_start and date_end:
    if (date_start > date_end):
        warning = st.warning('A data inicial deve ser MAIOR OU IGUAL a data final!', icon='⚠️')
        time.sleep(5)
        warning.empty()
        st.stop()

    if btn_submit:
        month_start: int | None = date_start.month
        year_start: int | None = date_start.year
        month_end: int | None = date_end.month
        year_end: int | None = date_end.year

        with st.spinner('Gerando arquivo. Aguarde...'):
            message = main(cpf, month_start, year_start, month_end, year_end)

        if (message == 'Arquivo gerado com sucesso!'):
            success = st.success(message, icon='✅')
            time.sleep(4)
            success.empty()
        else:
            error = st.error(message, icon='🚨')
            time.sleep(4)
            error.empty()
else:
    if btn_submit:
        warning = st.warning('CPF e as datas INICIAL E FINAL são obrigatórios!', icon='⚠️')
        time.sleep(4)
        warning.empty()


# if btn_submit:
#     if not cpf:
#         st.toast('Informe o CPF com pontos e traço', icon='⚠️')
#         time.sleep(1)
#         st.stop()
#
#     if not date_start:
#         st.toast('Selecione a data inicial', icon='⚠️')
#         st.stop()
#
#     if not date_end:
#         st.toast('Selecione a data final', icon='⚠️')
#         st.stop()
