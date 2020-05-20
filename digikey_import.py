import csv

def formatRes(resistance_string):
    if ((resistance_string.find("k")>=0) or (resistance_string.find("M")>=0)):
        # case 1: contains "k" or "M"
        if(resistance_string.find(".")>=0):
            # subcase 1: contains a decimal
            rep_char = resistance_string[-1]
            resistance_string = resistance_string[:-1]
            return resistance_string.replace(".", rep_char)
        else:
            # subcase 2: no decimal
            return resistance_string
    elif (resistance_string.find(".")>=0):
        # case 2: contains a decimal
        return resistance_string.replace(".", "R")
    else:
        # case 3: does not contain a decimal or k/M
        return (resistance_string + 'R')
        

lib_template_string = """#
# {0}
#
DEF ~{0} R 0 0 N N 1 F N
F0 "R" 30 30 60 H V L CNN
F1 "{0}" 0 -300 60 H I C CNN
F2 "" -20 -70 60 H I C CNN
F3 "" 0 0 60 H I C CNN
F4 "{1}" 30 -50 60 H V L CNN "Resistance"
F5 "{2}" 280 230 60 H I C CNN "Manufacturer"
F6 "{3}" 380 330 60 H I C CNN "Manufacturer Part No"
F7 "{4}" 480 430 60 H I C CNN "Supplier"
F8 "{5}" 580 530 60 H I C CNN "Supplier Part No"
$FPLIST
 R0603_IPC_Nominal
 R0603_IPC_Most
 R0603_IPC_Least
$ENDFPLIST
DRAW
P 8 0 1 0 0 -60 20 -50 -20 -30 20 -10 -20 10 20 30 -20 50 0 60 N
X 1 1 0 -100 40 U 50 50 1 1 I
X 2 2 0 100 40 D 50 50 1 1 I
ENDDRAW
ENDDEF"""

dcm_template_string = """#
$CMP {0}
D {1}
F {2}
$ENDCMP"""

libfile = open('pana_lib.txt', 'w', encoding='utf-8')
dcmfile = open('pana_dcm.txt', 'w', encoding='utf-8')

with open('panasonic_erj_res_0603.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        formatted_res = formatRes(row['Resistance (Ohms)'])
        identifier="R0603-" + formatted_res + "-1%"
        lib_string = lib_template_string.format(identifier, row['Resistance (Ohms)'] + 'Ω', row['Manufacturer'], row['Manufacturer Part Number'], 'Digi-Key', row['Digi-Key Part Number'])
        dcm_string = dcm_template_string.format(identifier, row['Description'], row['Datasheets'])
        print(lib_string)
        libfile.write(lib_string + '\n')
        print(dcm_string)
        dcmfile.write(dcm_string + '\n')

libfile.close()
dcmfile.close()