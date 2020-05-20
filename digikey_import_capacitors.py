import csv

def formatCap(cap_string):
    num_val_str = cap_string[:-2]
    num_val = float(num_val_str)
    # first step: add nF range
    if ((cap_string.find("pF")>=0) and (num_val >= 1000.0)):
        cap_string = '{0:g}'.format(num_val/1000.0) + "nF"
    if ((cap_string.find("uF")>=0) and (num_val < 1.0)):
        cap_string = '{0:g}'.format(num_val*1000.0) + "nF"
    # second step: if there is a decimal, shift the SI prefix over to its position
    # Nevermind - this looked ugly in the library
    #if (cap_string.find(".")>=0):
    #    # extract SI prefix
    #    prefix = cap_string[-2:-1]
    #    # remove prefix from string
    #    cap_string = cap_string.replace(prefix, "")
    #    # replace period with prefix
    #    cap_string = cap_string.replace(".", prefix)
    return cap_string
    
def formatTempco(temp_string):
    if((temp_string.find("C0G, NP0")>=0)):
        return "C0G_NP0"
    else:
        return temp_string
        
def formatTolerance(tol_string):
    if((tol_string.find("%")>=0)):
        return tol_string
    else:
        return tol_string + "_TOL"
        
def formatFeatureString(feature_string):
    if(feature_string.find("AEC-Q200")>=0):
        return "-Automotive"
    elif(feature_string.find("COTS")>=0):
        return "-HiRel"
    else:
        return ""
        
def fixhttp(url_string):
    if(url_string[:5] != 'http:'):
        url_string = "http:" + url_string
    return url_string

lib_template_string = """#
# {0}
#
DEF ~{0} C 0 0 N N 1 F N
F0 "C" 75 40 60 H V L CNN
F1 "{0}" 10 210 60 H I C CNN
F2 "" 60 -100 60 H I C CNN
F3 "" 160 0 60 H I C CNN
F4 "{1}" 85 -45 60 H V L CNN "Capacitance"
F5 "{2}" 360 200 60 H I C CNN "Manufacturer"
F6 "{3}" 460 300 60 H I C CNN "Manufacturer Part No"
F7 "{4}" 560 400 60 H I C CNN "Supplier"
F8 "{5}" 660 500 60 H I C CNN "Supplier Part No"
$FPLIST
 C0603_IPC_Nominal
 C0603_IPC_Most
 C0603_IPC_Least
$ENDFPLIST
DRAW
P 2 0 1 0 -60 -15 60 -15 N
P 2 0 1 0 -60 15 60 15 N
X 1 1 0 100 85 D 50 50 1 1 P
X 2 2 0 -100 85 U 50 50 1 1 P
ENDDRAW
ENDDEF"""

dcm_template_string = """#
$CMP {0}
D {1}
F {2}
$ENDCMP"""

libfile = open('kemet_0603_lib.txt', 'w', encoding='utf-8')
dcmfile = open('kemet_0603_dcm.txt', 'w', encoding='utf-8')

with open('kemet_0603_caps.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        formatted_cap = formatCap(row['Capacitance'])
        tempco = formatTempco(row['Temperature Coefficient'])
        feature = formatFeatureString(row['Ratings'])
        tolerance = formatTolerance(row['Tolerance'])
        datasheet_url = fixhttp(row['Datasheets'])
        identifier="C0603-" + formatted_cap + "-" + row['Voltage - Rated'] + "-" + tolerance + '-' + tempco
        lib_string = lib_template_string.format(identifier, formatted_cap, row['Manufacturer'], row['Manufacturer Part Number'], 'Digi-Key', row['Digi-Key Part Number'])
        dcm_string = dcm_template_string.format(identifier, row['Description'], datasheet_url)
        print(lib_string)
        libfile.write(lib_string + '\n')
        print(dcm_string)
        dcmfile.write(dcm_string + '\n')

libfile.close()
dcmfile.close()