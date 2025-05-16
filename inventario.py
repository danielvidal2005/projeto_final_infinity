import sqlite3
from PIL import Image
import io
import base64


def criar_tabela_inventario():
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,   
                imagem BLOB     
            )
        ''')
        conn.commit()


def obter_itens_com_imagem():
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, item, tipo, quantidade, imagem FROM inventario')
        itens = []

        for id_item, item, tipo, qtd, imagem_blob in cursor.fetchall():
            imagem_base64 = None
            if imagem_blob:
                imagem_base64 = base64.b64encode(imagem_blob).decode('utf-8')
            itens.append((id_item, item, tipo, qtd, imagem_base64))
        
        return itens


def ler_imagem(caminho_imagem):
    with open(caminho_imagem, 'rb') as file:
        blob = file.read()
    return blob


def inserir_item(item, quantidade, caminho_imagem):
    imagem_blob = ler_imagem(caminho_imagem)

    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventario
            (item, tipo, quantidade, caminho_imagem)
            VALUES (?, ?, ?, ?)
        ''', (item, quantidade, imagem_blob))
        conn.commit()

def obter_itens():
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, item, tipo, quantidade FROM inventario')
        return cursor.fetchall()



def visualizar_itens():
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, item, quantidade, imagem FROM inventario')
        itens = cursor.fetchall()

        for item in itens:
            id_item, nome, quantidade, imagem_blob = item 
            print(f'\nID: {id_item}\nItem: {nome}\nQuantidade: {quantidade}')
            
            if imagem_blob:
                try:
                    imagem = Image.open(io.BytesIO(imagem_blob))
                    imagem.show(title=f'Item: {nome}')
                except Exception as e:
                    print('Erro ao exibir imagem:', e)    
            else:
                print('Este item não possui imagem.')


def atualizar_item(id_item, novo_item=None, nova_quantidade=None, novo_caminho_imagem=None):
    campos =[]
    valores =[]

    if novo_item is not None:
        campos.append('item = ?')
        valores.append(novo_item)
    
    if nova_quantidade is not None:
        campos.append('quantidade = ?')
        valores.append(nova_quantidade)

    if novo_caminho_imagem is not None:
        nova_imagem_blob = ler_imagem(novo_caminho_imagem)
        campos.append('imagem = ?')
        valores.append(nova_imagem_blob)

    if not campos:
        print('Nada a atualizar.')
        return
    
    valores.append(id_item)

    query = f'''
        UPDATE inventario
        SET {', '.join(campos)}
        WHERE id = ?
    '''

    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, valores)
        conn.commit()


def excluir_item(id_item):
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM inventario WHERE id = ?', (id_item,))
        conn.commit()
        print(f'Item com id {id_item} foi excluído com sucesso.')

