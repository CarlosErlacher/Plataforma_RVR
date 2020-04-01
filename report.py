import os
import pandas as pd

class LoaderCDR:
    def __init__(self, df_file_name):
        self.df = pd.read_csv(df_file_name, sep=';', header=None)
    
    def data_clean(self):
        self.df = self.df[[0,1,2,3,5,6,7,10,11]].copy()
        self.df.columns = ['Destino','Data','Usuario', 'Did', 'Duracao', 'Conta_Voip', 'Tronco', 'Compra', 'Venda']
        self.df.Data = pd.to_datetime(self.df.Data)
        self.df['Tipo_Ligacao'] = self.df.Tronco.apply(self.__from_tronco_to_tp_ligacao)
    
    def __from_tronco_to_tp_ligacao(self, s_tronco):
        lst = s_tronco.split('_')
        if len(lst) < 3:
            return 'Entrada'
        if lst[2] == 'Fixo':
            return 'Fixo'
        if lst[2] == 'Cel':
            return 'Celular'
        if lst[2] == 'DDI':
            return 'DDI'
        if lst[2] == 'TDM':
            return 'Especial'
        else:
            return "Outro"

class Client:
    def __init__(self, nm_client, df):
        self.df = df[df.Usuario==nm_client].copy()
        self.nm_client = nm_client
    
    def print_report(self):
        _df = self.df
        venda = _df.Venda.sum()
        custo = _df.Compra.sum()
        lucro = venda - custo
        print ('''
        ==============================================
        Segue abaixo os valores selecionados:
        Cliente : {}
        --> Venda - R$ {:.2f} 
        --> Custo - R$ {:.2f}
        --> Lucro - R$ {:.2f}
        ===============================================
        
        '''.format(self.nm_client, venda, custo, lucro))


cdr = LoaderCDR('cdr.csv')
cdr.data_clean()

cliente_escritorio = Client(
    nm_client = 'Escritorio',
    df = cdr.df
)
cliente_escritorio.print_report()

sorted(list(cdr.df.Usuario.unique()))

cliente_brshield = Client(
    nm_client = 'brshield',
    df = cdr.df
)
cliente_brshield.print_report()

lst_clients = ['Tronco_Telium', 'Tronco_Telium2', 'Tronco_TelleGroup_DID_2', 'Tronco_TelleGroup_Fixo', 'Tronco_Voitel', 'Unknown', 'Vale_do_sol1', 'Vale_do_sol2', 'Vale_do_sol3', 'Vale_do_sol4', 'Vastima', 'VictorValentino', 'Villa_Frati', 'Villa_Fratti', 'VivianeDeJesus', 'Vult_Itaqua', 'Vult_Itaqua01', 'Vult_Itaqua02', 'Vult_Itaqua03']
for cliente in lst_clients:
    cl = Client(cliente, cdr.df)
    cl.print_report()

