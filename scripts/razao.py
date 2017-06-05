#!/usr/bin/env python

import sys, csv, re, locale

rowCount = 0
TITULO = 1
CONTA = 3

DEB1  = 9
DEB2  = 10
CRED1 = 11
CRED2 = 12

def debug(msg):
    return False
    # print msg

def processHeader(reader, row, nrow):
    if len(row[0].strip()) == 0                              and len(row[1].strip()) != 0 and len(row[2].strip()) == 0:
        # "","GUILHERME JOAO REIJERS (Rural) (00524)","","","","","","","","","","","","","","Goncalves Contabilidade S/S Ltda. - ME",""
        # "","CNPJ: 079.564.908-80","","","","","","","","","","","","","","",""
        # "","Empresas Consolidadas: 00524,00530,00225","","","","","","","","","","","","","","",""
        # "","Razzo Consolidado de 01/01/2017 ate 24/05/2017","","","","","","","","","","Livro :7","","","","Folha: 367",""
        debug("(header type1): " + str(row))
        return True
    elif len(row[0].strip()) != 0 and row[0].strip() == "Data" and len(row[1].strip()) == 0 and len(row[2].strip()) != 0:
        # "Data","","Historico","C/P","Documento","","","Lote","","","Debito","","","Credito ","","","S a l d o"
        debug("(header type2): " + str(row))
        return True
    elif len(row[0].strip()) != 0 and row[0].strip() != "Data" and len(row[1].strip()) == 0 and len(row[2].strip()) == 0:
        # "Caixa Economica Federal   (10206)   1.1.1.02.006","","","","","","","","","","","","","","","",""
        debug("(header type3): " + str(row))
        m = re.search('([^\(]+)\s\(([0-9]+)\)\s+([0-9\.]+)', row[0])
        nrow['conta'] = m.group(2).strip()
        nrow['contabil'] = m.group(3).strip().translate(None, '.')
        nrow['titulo'] = m.group(1).strip()
        return True
    # elif
    elif not isRow(reader, row, nrow):
        # "","","","","","","","","","Saldo Anterior:","","","","","","","        47.121,53D"
        debug("(header type4): " + str(row))
        # if len(row) == 17 and len(row[16].strip()) != 0:
        #     nrow['saldoIni'] = row[16].strip()
        return True
    return False

def processHeaders(reader, row, nrow):
    while processHeader(reader, row, nrow):
        row = next(reader)
    return row

def processFooters(reader, row, nrow):
    return row

def isRowExtra(reader, row, nrow):
    return len(row[0].strip()) == 0 and len(row[1].strip()) == 0 and len(row[2].strip()) != 0 and len(row[16].strip()) == 0

def processRows(reader, row, nrow):
    while processRow(reader, row, nrow):
        row = next(reader)
        while processRowExtra(reader, row, nrow):
            row = next(reader)
        printRow(nrow)
    return row

def isRow(reader, row, nrow):
    return len(row[0].strip()) != 0 and row[0].strip() != "Data" and len(row[1].strip()) == 0 and len(row[1].strip()) == 0 and len(row[2].strip()) != 0 and len(row[8].strip()) != 0

def processRow(reader, row, nrow):
    if isRow(reader, row, nrow):
        # "05/01/2017","","Valor creditado no Banco CEF ","","30102","","","","00032","","425,76","","","","","","156.397,51C"
        debug("(row): " + str(row))
        nrow['id']    = nrow['id'] + 1
        nrow['data']  = row[0].strip()
        nrow['hist']  = row[2].strip()
        nrow['doc']   = row[4].strip()
        nrow['lote']  = row[8].strip()
        if len(row[10].strip()) == 0:
            nrow['deb'] = row[DEB1].strip()
        else:
            nrow['deb'] = row[DEB2].strip()
        if len(row[12].strip()) == 0:
            nrow['cred']  = row[CRED1].strip()
        else:
            nrow['cred']  = row[CRED2].strip()
        # nrow['saldo'] = ''#row[16].strip()
        return True
    return False

def processRowExtra(reader, row, nrow):
    if len(row[0].strip()) == 0 and len(row[1].strip()) == 0 and len(row[2].strip()) != 0:
        # "","","ref. recebimento de vendas a ","","","","","","","","","","","","","",""
        # "","","Cooperflora de 20 a 26/11/2016","","","","","","","","","","","","","",""
        debug("(row): " + str(row))
        nrow['hist'] = nrow['hist'].strip() + " " + row[2].strip()
        return True
    return False

def printRow(nrow):
    # original
    print '"' + str(nrow['id']) \
        + '","' + nrow['conta'] \
        + '","' + nrow['data'] \
        + '","' + nrow['doc'] \
        + '","' + nrow['lote'] \
        + '","' + nrow['hist'] \
        + '","' + nrow['deb'] \
        + '","' + nrow['cred'] \
        + '"'
    # espelho
    nrow['id']    = nrow['id'] + 1
    print '"' + str(nrow['id']) \
        + '","' + nrow['doc'] \
        + '","' + nrow['data'] \
        + '","' + nrow['conta'] \
        + '","' + nrow['lote'] \
        + '","' + nrow['hist'] \
        + '","' + nrow['cred'] \
        + '","' + nrow['deb'] \
        + '"'


locale.setlocale(locale.LC_ALL, 'pt_BR')
print '"' + "id" \
    + '","' + "Conta" \
    + '","' + "Data" \
    + '","' + "Documento" \
    + '","' + "Lote" \
    + '","' + "Historico" \
    + '","' + "Debito" \
    + '","' + "Credito" \
    + '"'
    # + "," + "Saldo Inicial" \
    # + "," + "Saldo"
with sys.stdin as f:
    reader = csv.reader(f)
    started = False
    nrow = {'id':0}

    try:
        row = next(reader)
        while True:
            row = processHeaders(reader, row, nrow)
            row = processRows(reader, row, nrow)
            row = processFooters(reader, row, nrow)
    except StopIteration:
        pass