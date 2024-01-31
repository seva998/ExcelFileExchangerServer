import openpyxl


def set_border(ws, cell_range):
    thin = openpyxl.styles.Side(border_style="thin", color="000000")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = openpyxl.styles.Border(top=thin, left=thin, right=thin, bottom=thin)


def AllQtyPercent(top,bot,signs):
    # For persents with signs after , 0 if no signs
    if (top != None and bot != None and bot!= 0):
        return int(round((top/bot*100),signs))
    else:
        return 0


def TransportPercent(top,bot,signs):
    # For persents with signs after , 0 if no signs
    if (top != None and bot != None and bot!=0):
        return round(((top/bot-1)*100),signs)
    else:
        return 0


def AllQtyCalculator(UserInfo,TranzitInfo):
    if (UserInfo[0][0] != None
            and UserInfo[0][1] != None
            and UserInfo[0][2] != None
            and UserInfo[0][3] != None):
                if TranzitInfo[0][0] != None :
                    return (UserInfo[0][0] - UserInfo[0][1] + UserInfo[0][2] - UserInfo[0][3] + TranzitInfo[0][0])
                else:
                    return (UserInfo[0][0] - UserInfo[0][1] + UserInfo[0][2] - UserInfo[0][3])
    else:
        return 0


def TransportCalculator(TransportInfo):
    if ((NanCheck(TransportInfo[0][4])
        +NanCheck(TransportInfo[0][5])
         +NanCheck(TransportInfo[0][6])
         +NanCheck(TransportInfo[0][7])) > (NanCheck(TransportInfo[0][0])
        +NanCheck(TransportInfo[0][1])
         +NanCheck(TransportInfo[0][2])
         +NanCheck(TransportInfo[0][3]))):
        result = f'+{(NanCheck(TransportInfo[0][4])+ NanCheck(TransportInfo[0][5])+ NanCheck(TransportInfo[0][6])+ NanCheck(TransportInfo[0][7]))- NanCheck(TransportInfo[0][0])- NanCheck(TransportInfo[0][1])- NanCheck(TransportInfo[0][2])- NanCheck(TransportInfo[0][3])}'
    else:
        result = (NanCheck(TransportInfo[0][4])
        +NanCheck(TransportInfo[0][5])
        +NanCheck(TransportInfo[0][6])
        +NanCheck(TransportInfo[0][7])
        -NanCheck(TransportInfo[0][0])
        - NanCheck(TransportInfo[0][1])
        - NanCheck(TransportInfo[0][2])
        - NanCheck(TransportInfo[0][3]))
    return result


def ReidAllStr(Reid_info):
    if ((NanCheck(Reid_info[0][0])+NanCheck(Reid_info[0][1])) > (NanCheck(Reid_info[0][2])+NanCheck(Reid_info[0][3]))):
        return f'+{(NanCheck(Reid_info[0][0])+NanCheck(Reid_info[0][1]))-(NanCheck(Reid_info[0][2])+NanCheck(Reid_info[0][3]))}'
    else:
        return (NanCheck(Reid_info[0][2])+NanCheck(Reid_info[0][3]))-(NanCheck(Reid_info[0][0])+NanCheck(Reid_info[0][1]))


def PortAllStr(Reid_info):
    if ((NanCheck(Reid_info[0][4])+NanCheck(Reid_info[0][5])) > (NanCheck(Reid_info[0][6])+NanCheck(Reid_info[0][7]))):
        return f'+{(NanCheck(Reid_info[0][4])+NanCheck(Reid_info[0][5]))-(NanCheck(Reid_info[0][6])+NanCheck(Reid_info[0][7]))}'
    else:
        return (NanCheck(Reid_info[0][6])+NanCheck(Reid_info[0][7]))-(NanCheck(Reid_info[0][4])+NanCheck(Reid_info[0][5]))


def AutoCalculator(TransportInfo):
    if NanCheck(TransportInfo[0][6])>NanCheck(TransportInfo[0][2]):
        return f'+{NanCheck(TransportInfo[0][6]) - NanCheck(TransportInfo[0][2])}'
    else:
        return (NanCheck(TransportInfo[0][6])- NanCheck(TransportInfo[0][2]))


def is_stevedor(user):
    return user.groups.filter(name='stevedors').exists()


def NanCheck(i):
    try:
        int(i)
        if str(i) == 'nan' or str(i) =='' or i == None:
            i = 0
        return i
    except:
        i = 0
    return i
