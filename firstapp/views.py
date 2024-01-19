# Файл views.py
import psycopg2
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from .models import DataTable3
import datetime as dt
from openpyxl.utils import get_column_letter
from django.views.decorators.csrf import csrf_exempt
import openpyxl
from io import BytesIO, StringIO
from django.http import HttpResponse, FileResponse
DAYDELTA = dt.timedelta(days=1,
                           seconds=0,
                           microseconds=0,
                           milliseconds=0,
                           minutes=0,
                           hours=0,
                           weeks=0)

def connection():
    s = 'localhost'
    d = 'postgres'
    u = 'admin'
    p = 'root'
    conn = psycopg2.connect(host=s, user=u, password=p, database=d, port='6101')
    return conn

@login_required(login_url='')
def home(request):
    #В данном случае ID админа 2, но рекомендуется использовать 1, и первым пользователем создавать именно админа.
    if request.user.id != 2:
        if request.method == 'POST':
            file = request.FILES.get('file')
            if file is not None:
                if file.name.endswith('.xlsx'):
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    try:
                        # Чтение xlsx файла
                        df = pd.read_excel(fs.path(filename))
                        # Игнорирование первых трёх строк
                        df = df.iloc[2:]
                        # Преобразование DataFrame в списки столбцов (В дальнейшем для новых столбцов таблицы создавать новые поля в таблице БД, а также добавлять ниже в переменные)
                        ImportIn = df.iloc[:, 0].tolist()                     # в т.ч. импорт Прибыло
                        ImportOut = df.iloc[:, 1].tolist()                    # в т.ч. импорт Убыло
                        ExportIn = df.iloc[:, 2].tolist()                     # в т.ч. экспорт Прибыло
                        ExportOut = df.iloc[:, 3].tolist()                    # в т.ч. экспорт Убыло
                        TransitIn = df.iloc[:, 4].tolist()                    # в т.ч. транзит Прибыло
                        TransitOut = df.iloc[:, 5].tolist()                   # в т.ч. транзит Убыло
                        ExportEmpty = df.iloc[:, 6].tolist()                  # в т.ч. экспорт порожние
                        OtherEmpty = df.iloc[:, 7].tolist()                   # в т.ч. прочие порожние
                        UnloadReid = df.iloc[:, 8].tolist()                   # На рейде в ожидании Выгрузки
                        LoadingReid = df.iloc[:, 9].tolist()                  # На рейде в ожидании Погрузки
                        UnloadPort = df.iloc[:, 10].tolist()                  # На подходах к порту для Выгрузки
                        LoadingPort = df.iloc[:, 11].tolist()                 # На подходах к порту для Погрузки
                        fs.delete(filename)

                        # Дальнейшая обработка данных
                        request.session['parameters'] = {
                                                            'ImportIn': ImportIn,
                                                            'ImportOut': ImportOut,
                                                            'ExportIn': ExportIn,
                                                            'ExportOut': ExportOut,
                                                            'TransitIn': TransitIn,
                                                            'TransitOut': TransitOut,
                                                            'ExportEmpty': ExportEmpty,
                                                            'OtherEmpty': OtherEmpty,
                                                            'UnloadReid': UnloadReid,
                                                            'LoadingReid': LoadingReid,
                                                            'UnloadPort': UnloadPort,
                                                            'LoadingPort': LoadingPort
                                                            }
                        # Сохраните сессию, чтобы сгенерировать сессионный ключ
                        request.session.save()

                        # Получить текущий session ID
                        session_id = request.session.session_key
                        # Создайте URL-адрес перенаправления с этим session ID
                        redirect_url = f'/confirm/?session_id={session_id}'
                        return redirect(redirect_url)
                    except:
                        fs.delete(filename)
                        return render(request, 'error.html', {'ErrorText' : 'Ошибка выгрузки данных'})
                else:
                    return render(request, 'error.html', {'ErrorText' : 'Неверный формат файла'})
            else:
                return redirect('confirm')
        return render(request, 'home.html')
    else:
        return render(request, 'admin.html')

def register(request):
    if request.user.id == 2:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']

                # Создание нового пользователя
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')
            except:
                return render(request, 'register.html')
        return render(request, 'register.html')
    else:
        return redirect('login')
    ####

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверка введенных данных
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    # Выход пользователя
    logout(request)
    return redirect('home')

@login_required(login_url='')
def confirm(request):
    session_id = request.GET.get('session_id')
    if session_id:
        # Используйте session_id, чтобы вручную загрузить сеанс
        request.session = SessionStore(session_key=session_id)
        params = request.session.get('parameters',{})
        ImportIn = params.get('ImportIn')
        ImportOut = params.get('ImportOut')
        ExportIn = params.get('ExportIn')
        ExportOut = params.get('ExportOut')
        TransitIn = params.get('TransitIn')
        TransitOut = params.get('TransitOut')
        ExportEmpty = params.get('ExportEmpty')
        OtherEmpty = params.get('OtherEmpty')
        UnloadReid = params.get('UnloadReid')
        LoadingReid = params.get('LoadingReid')
        UnloadPort = params.get('UnloadPort')
        LoadingPort = params.get('LoadingPort')
        if request.method == 'POST':
            ImportIn = [request.POST['ImportIn']]
            ImportOut = [request.POST['ImportOut']]
            ExportIn = [request.POST['ExportIn']]
            ExportOut = [request.POST['ExportOut']]
            TransitIn = [request.POST['TransitIn']]
            TransitOut = [request.POST['TransitOut']]
            ExportEmpty = [request.POST['ExportEmpty']]
            OtherEmpty = [request.POST['OtherEmpty']]
            UnloadReid = [request.POST['UnloadReid']]
            LoadingReid = [request.POST['LoadingReid']]
            UnloadPort = [request.POST['UnloadPort']]
            LoadingPort = [request.POST['LoadingPort']]
            request.session['parameters'] = {
                'ImportIn': ImportIn,
                'ImportOut': ImportOut,
                'ExportIn': ExportIn,
                'ExportOut': ExportOut,
                'TransitIn': TransitIn,
                'TransitOut': TransitOut,
                'ExportEmpty': ExportEmpty,
                'OtherEmpty': OtherEmpty,
                'UnloadReid': UnloadReid,
                'LoadingReid': LoadingReid,
                'UnloadPort': UnloadPort,
                'LoadingPort': LoadingPort
            }
            redirect_url = f'/success/?session_id={session_id}'
            return redirect(redirect_url)
        return render(request, 'confirm.html', {
                                                        'ImportIn': ImportIn[0],
                                                        'ImportOut': ImportOut[0],
                                                        'ExportIn': ExportIn[0],
                                                        'ExportOut': ExportOut[0],
                                                        'TransitIn': TransitIn[0],
                                                        'TransitOut': TransitOut[0],
                                                        'ExportEmpty': ExportEmpty[0],
                                                        'OtherEmpty': OtherEmpty[0],
                                                        'UnloadReid': UnloadReid[0],
                                                        'LoadingReid': LoadingReid[0],
                                                        'UnloadPort': UnloadPort[0],
                                                        'LoadingPort': LoadingPort[0],
        })
    else:
        if request.method == 'POST':
            ImportIn = [request.POST['ImportIn']]
            ImportOut = [request.POST['ImportOut']]
            ExportIn = [request.POST['ExportIn']]
            ExportOut = [request.POST['ExportOut']]
            TransitIn = [request.POST['TransitIn']]
            TransitOut = [request.POST['TransitOut']]
            ExportEmpty = [request.POST['ExportEmpty']]
            OtherEmpty = [request.POST['OtherEmpty']]
            UnloadReid = [request.POST['UnloadReid']]
            LoadingReid = [request.POST['LoadingReid']]
            UnloadPort = [request.POST['UnloadPort']]
            LoadingPort = [request.POST['LoadingPort']]
            request.session['parameters'] = {
                'ImportIn': ImportIn,
                'ImportOut': ImportOut,
                'ExportIn': ExportIn,
                'ExportOut': ExportOut,
                'TransitIn': TransitIn,
                'TransitOut': TransitOut,
                'ExportEmpty': ExportEmpty,
                'OtherEmpty': OtherEmpty,
                'UnloadReid': UnloadReid,
                'LoadingReid': LoadingReid,
                'UnloadPort': UnloadPort,
                'LoadingPort': LoadingPort
            }
            # Сохраните сессию, чтобы сгенерировать сессионный ключ
            request.session.save()

            # Получить текущий session ID
            session_id = request.session.session_key
            # Создайте URL-адрес перенаправления с этим session ID
            redirect_url = f'/success/?session_id={session_id}'
            return redirect(redirect_url)
        return render(request, 'confirm.html', {
            'ImportIn': 0,
            'ImportOut': 0,
            'ExportIn': 0,
            'ExportOut': 0,
            'TransitIn': 0,
            'TransitOut': 0,
            'ExportEmpty': 0,
            'OtherEmpty': 0,
            'UnloadReid': 0,
            'LoadingReid': 0,
            'UnloadPort': 0,
            'LoadingPort': 0,
        })


def success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        # Используйте session_id, чтобы вручную загрузить сеанс
        request.session = SessionStore(session_key=session_id)
        params = request.session.get('parameters',{})
        ImportIn = params.get('ImportIn')
        ImportOut = params.get('ImportOut')
        ExportIn = params.get('ExportIn')
        ExportOut = params.get('ExportOut')
        TransitIn = params.get('TransitIn')
        TransitOut = params.get('TransitOut')
        ExportEmpty = params.get('ExportEmpty')
        OtherEmpty = params.get('OtherEmpty')
        UnloadReid = params.get('UnloadReid')
        LoadingReid = params.get('LoadingReid')
        UnloadPort = params.get('UnloadPort')
        LoadingPort = params.get('LoadingPort')
        ImportIn[0] = NanCheck(ImportIn[0])
        ImportOut[0] = NanCheck(ImportOut[0])
        ExportIn[0] = NanCheck(ExportIn[0])
        ExportOut[0] = NanCheck(ExportOut[0])
        TransitIn[0] = NanCheck(TransitIn[0])
        TransitOut[0] = NanCheck(TransitOut[0])
        ExportEmpty[0] = NanCheck(ExportEmpty[0])
        OtherEmpty[0] = NanCheck(OtherEmpty[0])
        UnloadReid[0] = NanCheck(UnloadReid[0])
        LoadingReid[0] = NanCheck(LoadingReid[0])
        UnloadPort[0] = NanCheck(UnloadPort[0])
        LoadingPort[0] = NanCheck(LoadingPort[0])
        # Перезапись данных за предыдущий день, при совпадении даты и ID пользователя.
        DataItem = DataTable3.objects.filter(date = dt.datetime.now()-DAYDELTA, db_userid = request.user.id).update(
                db_importin=float(ImportIn[0]),
                db_importout=float(ImportOut[0]),
                db_exportin=float(ExportIn[0]),
                db_exportout=float(ExportOut[0]),
                db_transitin=float(TransitIn[0]),
                db_transitout=float(TransitOut[0]),
                db_exportempty=float(ExportEmpty[0]),
                db_otherempty=float(OtherEmpty[0]),
                db_unloadreid=float(UnloadReid[0]),
                db_loadingreid=float(LoadingReid[0]),
                db_lunloadport=float(UnloadPort[0]),
                db_loadingport=float(LoadingPort[0])
            )
        # Запись новых данных, если ID пользователя и дата не совпадают.
        if DataItem == 0:
            DataTable3.objects.create(date = dt.datetime.now()-DAYDELTA,
                                          db_userid = request.user.id,
                                          db_importin= float(ImportIn[0]),
                                          db_importout = float(ImportOut[0]),
                                          db_exportin = float(ExportIn[0]),
                                          db_exportout = float(ExportOut[0]),
                                          db_transitin = float(TransitIn[0]),
                                          db_transitout = float(TransitOut[0]),
                                          db_exportempty = float(ExportEmpty[0]),
                                          db_otherempty = float(OtherEmpty[0]),
                                          db_unloadreid = float(UnloadReid[0]),
                                          db_loadingreid = float(LoadingReid[0]),
                                          db_lunloadport = float(UnloadPort[0]),
                                          db_loadingport = float(LoadingPort[0])
                                          )

        return render(request, 'success.html', {
                                                'ImportIn': ImportIn[0],
                                                'ImportOut': ImportOut[0],
                                                'ExportIn': ExportIn[0],
                                                'ExportOut': ExportOut[0],
                                                'TransitIn': TransitIn[0],
                                                'TransitOut': TransitOut[0],
                                                'ExportEmpty': ExportEmpty[0],
                                                'OtherEmpty': OtherEmpty[0],
                                                'UnloadReid': UnloadReid[0],
                                                'LoadingReid': LoadingReid[0],
                                                'UnloadPort': UnloadPort[0],
                                                'LoadingPort': LoadingPort[0],
                                                'user': request.user})

def NanCheck(i):
    try:
        float(i)
        if str(i) == 'nan' or str(i) =='':
            i = 0
        return i
    except:
        i = 0
    return i

###File download realization
@csrf_exempt
def download(request):
    if request.user.id == 2:
        wb = openpyxl.Workbook()
        ws = wb.active
        params = request.session.get('parameters', {})
        date = params.get('date1')
        columns = ['Дата',
                   'Имя пользователя',
                   'в т.ч. импорт Прибыло',
                   'в т.ч. импорт Убыло',
                   'в т.ч. экспорт Прибыло',
                   'в т.ч. экспорт Убыло',
                   'в т.ч. транзит Прибыло',
                   'в т.ч. транзит Убыло',
                   'в т.ч. экспорт порожние',
                   'в т.ч. прочие порожние',
                   'На рейде в ожидании Выгрузки',
                   'На рейде в ожидании Погрузки',
                   'На подходах к порту для Выгрузки',
                   'На подходах к порту для Погрузки']
        for i, column in enumerate(columns):
            ws[f'{get_column_letter(i + 1)}1'] = column
            ws[f'{get_column_letter(i + 1)}1'].fill  = openpyxl.styles.PatternFill('solid', fgColor='000066CC')
            if i == 0:
                ws.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width = len(column) + 8
            else:
                ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = len(column) + 1
        try:
            conn = connection()
            cursor = conn.cursor()
            #admin_id = 2

            #
            # TestUser1
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                            f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 1")
            User1data = cursor.fetchall()
            if User1data == []:
                User1data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]

            ws[f'A2'] = date
            ws[f'B2'] = 'TestUser1'
            ws[f'C2'] = User1data[0][3]
            ws[f'D2'] = User1data[0][4]
            ws[f'E2'] = User1data[0][5]
            ws[f'F2'] = User1data[0][6]
            ws[f'G2'] = User1data[0][7]
            ws[f'H2'] = User1data[0][8]
            ws[f'I2'] = User1data[0][9]
            ws[f'J2'] = User1data[0][10]
            ws[f'K2'] = User1data[0][11]
            ws[f'L2'] = User1data[0][12]
            ws[f'M2'] = User1data[0][13]
            ws[f'N2'] = User1data[0][14]

            #
            # TestUser2
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                            f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 3")
            User2data = cursor.fetchall()
            if User2data == []:
                User2data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]
            ws[f'A3'] = date
            ws[f'B3'] = 'TestUser2'
            ws[f'C3'] = User2data[0][3]
            ws[f'D3'] = User2data[0][4]
            ws[f'E3'] = User2data[0][5]
            ws[f'F3'] = User2data[0][6]
            ws[f'G3'] = User2data[0][7]
            ws[f'H3'] = User2data[0][8]
            ws[f'I3'] = User2data[0][9]
            ws[f'J3'] = User2data[0][10]
            ws[f'K3'] = User2data[0][11]
            ws[f'L3'] = User2data[0][12]
            ws[f'M3'] = User2data[0][13]
            ws[f'N3'] = User2data[0][14]

            #
            # TestUser3 massive query
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                            f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 7")
            User3data = cursor.fetchall()
            if User3data == []:
                User3data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]
            ws[f'A4'] = date
            ws[f'B4'] = 'TestUser3'
            ws[f'C4'] = User3data[0][3]
            ws[f'D4'] = User3data[0][4]
            ws[f'E4'] = User3data[0][5]
            ws[f'F4'] = User3data[0][6]
            ws[f'G4'] = User3data[0][7]
            ws[f'H4'] = User3data[0][8]
            ws[f'I4'] = User3data[0][9]
            ws[f'J4'] = User3data[0][10]
            ws[f'K4'] = User3data[0][11]
            ws[f'L4'] = User3data[0][12]
            ws[f'M4'] = User3data[0][13]
            ws[f'N4'] = User3data[0][14]

            #
            # Сумма по всем пользователям за дату
            #

            cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                            f"SUM(db_importout) AS importoutsum,"
                            f"SUM(db_exportin) AS exportinsum,"
                            f"SUM(db_exportout) AS exportoutsum,"
                            f"SUM(db_transitin) AS transitinsum,"
                            f"SUM(db_transitout) AS transitoutsum,"
                            f"SUM(db_exportempty) AS exportemptysum,"
                            f"SUM(db_otherempty) AS otheremptysum,"
                            f"SUM(db_unloadreid) AS unloadreidsum,"
                            f"SUM(db_loadingreid) AS loadingreidsum,"
                            f"SUM(db_lunloadport) AS lunloadportsum,"
                            f"SUM(db_loadingport) AS loadingportsum "
                            f"FROM firstapp_datatable3 "
                            f"WHERE date = '{dt.datetime.strptime(date,'%Y-%m-%d').strftime('%Y%m%d')}'",)
            UserAlldatafordate = cursor.fetchall()
            ws[f'A5'] = date
            ws[f'B5'] = 'DAYSUMM'
            ws[f'C5'] = UserAlldatafordate[0][0]
            ws[f'D5'] = UserAlldatafordate[0][1]
            ws[f'E5'] = UserAlldatafordate[0][2]
            ws[f'F5'] = UserAlldatafordate[0][3]
            ws[f'G5'] = UserAlldatafordate[0][4]
            ws[f'H5'] = UserAlldatafordate[0][5]
            ws[f'I5'] = UserAlldatafordate[0][6]
            ws[f'J5'] = UserAlldatafordate[0][7]
            ws[f'K5'] = UserAlldatafordate[0][8]
            ws[f'L5'] = UserAlldatafordate[0][9]
            ws[f'M5'] = UserAlldatafordate[0][10]
            ws[f'N5'] = UserAlldatafordate[0][11]
            #
            # Сумма по всем пользователям за всё время
            #

            cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                            f"SUM(db_importout) AS importoutsum,"
                            f"SUM(db_exportin) AS exportinsum,"
                            f"SUM(db_exportout) AS exportoutsum,"
                            f"SUM(db_transitin) AS transitinsum,"
                            f"SUM(db_transitout) AS transitoutsum,"
                            f"SUM(db_exportempty) AS exportemptysum,"
                            f"SUM(db_otherempty) AS otheremptysum,"
                            f"SUM(db_unloadreid) AS unloadreidsum,"
                            f"SUM(db_loadingreid) AS loadingreidsum,"
                            f"SUM(db_lunloadport) AS lunloadportsum,"
                            f"SUM(db_loadingport) AS loadingportsum "
                            f"FROM firstapp_datatable3 ",)
            UserAlldata = cursor.fetchall()
            ws[f'A6'] = date
            ws[f'B6'] = 'ALLSUMM'
            ws[f'C6'] = UserAlldata[0][0]
            ws[f'D6'] = UserAlldata[0][1]
            ws[f'E6'] = UserAlldata[0][2]
            ws[f'F6'] = UserAlldata[0][3]
            ws[f'G6'] = UserAlldata[0][4]
            ws[f'H6'] = UserAlldata[0][5]
            ws[f'I6'] = UserAlldata[0][6]
            ws[f'J6'] = UserAlldata[0][7]
            ws[f'K6'] = UserAlldata[0][8]
            ws[f'L6'] = UserAlldata[0][9]
            ws[f'M6'] = UserAlldata[0][10]
            ws[f'N6'] = UserAlldata[0][11]

            conn.close()
        except:
            pass

        # for i, j in enumerate(DataTable3.objects.filter(date= params.get('date1'))):
        #     ws[f'A{i + 2}'] = j.date
        #
        #     #GET USERNAME FOR TABLE
        #     if j.db_userid == 1:
        #         ws[f'B{i + 2}'] = 'TestUser1'
        #     elif j.db_userid == 2:
        #         ws[f'B{i + 2}'] = 'admin'
        #     elif j.db_userid == 3:
        #         ws[f'B{i + 2}'] = 'TestUser2'
        #     elif j.db_userid == 7:
        #         ws[f'B{i + 2}'] = 'TestUser7'
        #     ws[f'C{i + 2}'] = j.db_importin
        #     ws[f'D{i + 2}'] = j.db_importout
        #     ws[f'E{i + 2}'] = j.db_exportin
        #     ws[f'F{i + 2}'] = j.db_exportout
        #     ws[f'G{i + 2}'] = j.db_transitin
        #     ws[f'H{i + 2}'] = j.db_transitout
        #     ws[f'I{i + 2}'] = j.db_exportempty
        #     ws[f'J{i + 2}'] = j.db_otherempty
        #     ws[f'K{i + 2}'] = j.db_unloadreid
        #     ws[f'L{i + 2}'] = j.db_loadingreid
        #     ws[f'M{i + 2}'] = j.db_lunloadport
        #     ws[f'N{i + 2}'] = j.db_loadingport
        set_border(ws, 'A1:N6')
        bytes_io = BytesIO()
        wb.save(bytes_io)
        bytes_io.seek(0)
        return FileResponse(bytes_io, as_attachment=True, filename=(date +'.xslx'))
    else:
        return redirect('home')

def dataset(request):
    if request.user.id == 2:
        params = request.session.get('parameters', {})
        date = params.get('date1')
        print(date)
        try:
            conn = connection()
            cursor = conn.cursor()
            #admin_id = 2

            #
            # TestUser1
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                           f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 1")
            User1data = cursor.fetchall()
            if User1data == []:
                User1data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]

            #
            # TestUser2
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                           f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 3")
            User2data = cursor.fetchall()
            if User2data == []:
                User2data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]

            #
            # TestUser3 massive query
            #

            cursor.execute(f"SELECT * FROM firstapp_datatable3 "
                           f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = 7")
            User3data = cursor.fetchall()
            if User3data == []:
                User3data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]

            #
            # Сумма по всем пользователям за дату
            #

            cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                            f"SUM(db_importout) AS importoutsum,"
                            f"SUM(db_exportin) AS exportinsum,"
                            f"SUM(db_exportout) AS exportoutsum,"
                            f"SUM(db_transitin) AS transitinsum,"
                            f"SUM(db_transitout) AS transitoutsum,"
                            f"SUM(db_exportempty) AS exportemptysum,"
                            f"SUM(db_otherempty) AS otheremptysum,"
                            f"SUM(db_unloadreid) AS unloadreidsum,"
                            f"SUM(db_loadingreid) AS loadingreidsum,"
                            f"SUM(db_lunloadport) AS lunloadportsum,"
                            f"SUM(db_loadingport) AS loadingportsum "
                            f"FROM firstapp_datatable3 "
                           f"WHERE date = '{dt.datetime.strptime(date,'%Y-%m-%d').strftime('%Y%m%d')}'",)
            UserAlldatafordate = cursor.fetchall()

            #
            # Сумма по всем пользователям за всё время
            #

            cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                            f"SUM(db_importout) AS importoutsum,"
                            f"SUM(db_exportin) AS exportinsum,"
                            f"SUM(db_exportout) AS exportoutsum,"
                            f"SUM(db_transitin) AS transitinsum,"
                            f"SUM(db_transitout) AS transitoutsum,"
                            f"SUM(db_exportempty) AS exportemptysum,"
                            f"SUM(db_otherempty) AS otheremptysum,"
                            f"SUM(db_unloadreid) AS unloadreidsum,"
                            f"SUM(db_loadingreid) AS loadingreidsum,"
                            f"SUM(db_lunloadport) AS lunloadportsum,"
                            f"SUM(db_loadingport) AS loadingportsum "
                            f"FROM firstapp_datatable3 "
                           f"WHERE date <= '{dt.datetime.strptime(date,'%Y-%m-%d').strftime('%Y%m%d')}'",)
            UserAlldata = cursor.fetchall()

            conn.close()
        except:
            return render(request, 'error.html', {'ErrorText' : 'Ошибка отображения данных'})
        return render(request, 'dataset.html', {
                                                    'date' : (dt.datetime.strptime(date,'%Y-%m-%d').strftime('%d.%m.%Y.')),
                                                    'ImportIn': UserAlldatafordate[0][0],
                                                    'ImportOut': UserAlldatafordate[0][1],
                                                    'ExportIn': UserAlldatafordate[0][2],
                                                    'ExportOut': UserAlldatafordate[0][3],
                                                    'TransitIn': UserAlldatafordate[0][4],
                                                    'TransitOut': UserAlldatafordate[0][5],
                                                    'ExportEmpty': UserAlldatafordate[0][6],
                                                    'OtherEmpty': UserAlldatafordate[0][7],
                                                    'UnloadReid': UserAlldatafordate[0][8],
                                                    'LoadingReid': UserAlldatafordate[0][9],
                                                    'UnloadPort': UserAlldatafordate[0][10],
                                                    'LoadingPort': UserAlldatafordate[0][11],

                                                    'ImportIn1': User1data[0][3],
                                                    'ImportOut1': User1data[0][4],
                                                    'ExportIn1': User1data[0][5],
                                                    'ExportOut1': User1data[0][6],
                                                    'TransitIn1': User1data[0][7],
                                                    'TransitOut1': User1data[0][8],
                                                    'ExportEmpty1': User1data[0][9],
                                                    'OtherEmpty1': User1data[0][10],
                                                    'UnloadReid1': User1data[0][11],
                                                    'LoadingReid1': User1data[0][12],
                                                    'UnloadPort1': User1data[0][13],
                                                    'LoadingPort1': User1data[0][14],

                                                    'ImportIn2': User2data[0][3],
                                                    'ImportOut2': User2data[0][4],
                                                    'ExportIn2': User2data[0][5],
                                                    'ExportOut2': User2data[0][6],
                                                    'TransitIn2': User2data[0][7],
                                                    'TransitOut2': User2data[0][8],
                                                    'ExportEmpty2': User2data[0][9],
                                                    'OtherEmpty2': User2data[0][10],
                                                    'UnloadReid2': User2data[0][11],
                                                    'LoadingReid2': User2data[0][12],
                                                    'UnloadPort2': User2data[0][13],
                                                    'LoadingPort2': User2data[0][14],

                                                    'ImportIn3': User3data[0][3],
                                                    'ImportOut3': User3data[0][4],
                                                    'ExportIn3': User3data[0][5],
                                                    'ExportOut3': User3data[0][6],
                                                    'TransitIn3': User3data[0][7],
                                                    'TransitOut3': User3data[0][8],
                                                    'ExportEmpty3': User3data[0][9],
                                                    'OtherEmpty3': User3data[0][10],
                                                    'UnloadReid3': User3data[0][11],
                                                    'LoadingReid3': User3data[0][12],
                                                    'UnloadPort3': User3data[0][13],
                                                    'LoadingPort3': User3data[0][14],

                                                    'ImportInAllTime': UserAlldata[0][0],
                                                    'ImportOutAllTime': UserAlldata[0][1],
                                                    'ExportInAllTime': UserAlldata[0][2],
                                                    'ExportOutAllTime': UserAlldata[0][3],
                                                    'TransitInAllTime': UserAlldata[0][4],
                                                    'TransitOutAllTime': UserAlldata[0][5],
                                                    'ExportEmptyAllTime': UserAlldata[0][6],
                                                    'OtherEmptyAllTime': UserAlldata[0][7],
                                                    'UnloadReidAllTime': UserAlldata[0][8],
                                                    'LoadingReidAllTime': UserAlldata[0][9],
                                                    'UnloadPortAllTime': UserAlldata[0][10],
                                                    'LoadingPortAllTime': UserAlldata[0][11],

                                                    'user': request.user})
    else:
        return redirect('home')

def datepick(request):
    if request.user.id == 2:
        if request.method == 'POST':
            date1 = request.POST['date1']
            request.session['parameters'] = {'date1': date1}
            return redirect(dataset)
        print(dt.datetime.now().strftime('%Y-%m-%d'))
        return render(request, 'datepick.html' , {'currentdate':(dt.datetime.now()-DAYDELTA).strftime('%Y-%m-%d')})
    else:
        return redirect('home')


def set_border(ws, cell_range):
    thin = openpyxl.styles.Side(border_style="thin", color="000000")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = openpyxl.styles.Border(top=thin, left=thin, right=thin, bottom=thin)