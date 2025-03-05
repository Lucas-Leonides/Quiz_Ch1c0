import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "credentials.json"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)

    # Troque "Nome_da_Sua_Planilha" pelo nome real da sua planilha
    sheet = client.open("Quiz_chico").sheet1  

    # Obter os dados brutos (sem interpretar como dicionário)
    data = sheet.get_all_values()

    if data:
        print("✅ Dados da planilha:")
        for row in data:
            print(row)  # Mostra cada linha como uma lista
    else:
        print("❌ Nenhum dado encontrado na planilha.")
except gspread.SpreadsheetNotFound:
    print("❌ Erro: Planilha não encontrada. Verifique se o nome está correto e se a conta de serviço tem acesso.")
except Exception as e:
    print("❌ Erro na conexão:", e)
