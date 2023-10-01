# this is to only handle csv files and then copy the context to a TXT file
# UPDATE 2NOV2022 : updated avoid_bse_stocks to avoid stocks which are already available in NSE
# IDEA 3NOV2022 : Got to give an option in website to select the coulmns as per users demand and alos option to select if they want BSE CODE o BSE NAME
# IDEA 3NOV2022: Would be better if i could avoid all the gaps in the last of BSE NAMES

import csv
import datetime
from datetime import timedelta
import glob,os
import shutil
import zipfile
from zipfile import ZipFile
from zipfile import BadZipFile
import requests
from io import BytesIO
import urllib.request
from selenium import webdriver
from time import sleep
from datetime import date
import streamlit as st
import pandas as pd


#st.title("EOD BHAVCOPY")
# PATHS OF THIS COMPUTER
#path_bhav = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/'
#path_csv = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/"
#path_download = 'C:/Users/sahaveer/Downloads/'

# WORKIGN ON DATE FORMATS FROM CSV STRING NAMES
mnth_dict = {'JAN':'01' , 'FEB':'02' , 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
avoid_series = ['GS','IV', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG',
                'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'P2', 'W1',
                'W3', 'Y1', 'Y2', 'Y3','Y5','Y6', 'Y7','Y8', 'YA', 'YC', 'YG', 'YH', 'YI','YJ', 'YK', 'YL', 'YN', 'YO', 'YP', 'YR', 'YS', 'YT', 'YU', 'YV', 'YW', 'YY', 'YZ',
                'Z2', 'Z3', 'Z4', 'Z7', 'Z8', 'ZA', 'ZH', 'ZJ', 'ZK',
                ' GS',' IV', ' N1', ' N2', ' N3', ' N4', ' N5', ' N6', ' N7', ' N8', ' N9', ' NA', ' NB', ' NC', ' ND', ' NE', ' NF', ' NG',
                ' NH', ' NI', ' NJ', ' NK', ' NL', ' NM', ' NN', ' NO', ' NP', ' NQ', ' NR', ' NS', ' NT', ' NU', ' NV', ' NW', ' NX', ' NY', ' P2', ' W1',
                ' W3', ' Y1', ' Y2', ' Y3',' Y5',' Y6', ' Y7',' Y8', ' YA', ' YC', ' YG', ' YH', ' YI',' YJ', ' YK', ' YL', ' YN', ' YO', ' YP', ' YR', ' YS', ' YT', ' YU', ' YV', ' YW', ' YY', ' YZ',
                ' Z2', ' Z3', ' Z4', ' Z7', ' Z8', ' ZA', ' ZH', ' ZJ', ' ZK','YX',
                ]
avoid_bse_series = ['F ', 'G ']
# avoid_bse_stocks USED cos these stocks are available in NSE as well
avoid_bse_stocks = ['20 MICRONS  ','21ST CEN.MGM','3I INFOTECH ','3M INDIA LTD','AADI INDUS L','AAREY DRUGS ','AARTI DRUGS ','AARTI INDUST',
                    'AARVEE DENIM', 'ABAN OFFSHO ', 'ABB LTD.    ','ABBOTT (I)  ','ABFRL       ','ACC LTD     ','ACRYCIL LTD.','ACTION CONST',
                    'ADANI PORTS ','ADANI POWER ','ADF FOODS LT','ADORWELDING ','ADVANI HOTEL','AEGIS LOGIS ','AGAR IND COR','AGRI TECH   ','AHLUWALIA CO',
                    'AIAENGINEER ','AJANTA PHARM','AKSHAR      ','AKSHARCHEM I','ALBERT DAVID','ALEMBIC LTD.','ALKYL AMINES','ALLSEC TECH ','ALMONDZ GLO ',
                    'ALOK INDS.  ','ALPA LAB    ','ALPHAGEO (I)','ALPS INDS.  ','AMAR RAJA BA','AMBICA AGAR.','AMBIKA COTTO','AMBUJA CEME ','AMD INDUS   ',
                    'ANDHRA CEMEN','ANDHRA SUGAR','ANDREW YULE ','ANIK INDS   ','ANKIT METAL ','APAR INDUS. ','APCOTEX IND ','APL APOLLO  ','APOLLO HOSP.','APOLLOPIPES ',
                    'APOLLO TYRES','APTECH LTD  ','ARCHIES LTD ','ARCHIDPLY IN','ARIES AGRO  ','ARIHANT CAP.','ARIH SUPER  ','ARMAN FIN   ','ARO GRANITE ','ARSS INFRA  ',
                    'IOL CHEM PH ','ION EXCHANGE','IPCA LAB LTD','IPL         ','IRCON       ','IRCTC       ','IRFC        ','PANACHE     ']
avoid_stocks = ['AURUMPP','AIRTELPP','182D290922','426GS2023','619GS2034','667GS2050','676GS2061','699GS2051','719GS2060',
                '769GS2043','772GS2055','795GS2032','817GS2044','AXISNIFTY','AXISBNKETF',
                'AXISBPSETF','AXISCETF','AXISHCETF','AXISTECETF','BBETF0432','DSPN50ETF',
                'DSPNEWETF','DSPQ50ETF','EBBETF0425','EBBETF0430','EBBETF0431','IBMFNIFTY','ICICI500','ICICIALPLV',
                'ICICAUTO', 'ICICIB22','ICICIBANKN','ICICIBANKP','ICICILIQ','ICICILOVOL','ICICIM150','ICICIMCAP','ICICINF100',
                'ICICINIFTY','ICICINV20','ICICINXT50','ICICIPHARM','ICICIPRULI','ICICISENSX','ICICISILVE','ICICITECH','IDFNIFTYET',
                'KOTAKBKETF','KOTAKGOLD','KOTAKIT','KOTAKMID50','KOTAKNIFTY','KOTAKNV20','KOTAKPSUBK','LICNETFGSC','LICNETFN50',
                'LICNETFSEN','LICNFNHGP','LIQUIDETF','M17RG','MAESGETF','MAFSETF','MAMFGETF','MAN50ETF','MANXT50','MASPTOP50',
                'MOM100','MOM50','MON100','MONQ50','NCPSESDL24','NETFAUTO','NETFCONSUM','NETFDIVOPP','NETFGILT5Y','NETFIT',
                'NETFLTGILT','NETFMID150','NETFNIF100','NETFNV20','NETFPHARMA','NETFSDL26','NETFSILVER','NHBTF2014','NHBTF2023',
                'QGOLDHALF','QNIFTY','SBIETFCON','SBIETFIT','','SBIETFPB','SBIETFQLTY','SETF10GILT','SETFGOLD','SETFNIF50',
                'SETFNIFBK','SETFNN50','SETUINFRA','SGBAPR28I','SGBAUG24','SGBAUG27','SGBAUG28V','SGBAUG29V','SGBD29VIII',
                'SGBDC27VII','SGBFEB24','SGBFEB27','SGBFEB28IX','SGBFEB29XI','SGBJ28VIII','SGBJAN26','SGBJAN27','SGBJAN29IX',
                'SGBJAN29X','SGBJAN30IX','SGBJU29III','SGBJUL25','SGBJUL27','SGBJUL28IV','SGBJUL29IV','SGBJUN27','SGBJUN28',
                'SGBJUN29II','SGBMAR24','SGBMAR25','SGBMAR28X','SGBMAY25','SGBMAY26','SGBMAY28','SGBMAY29I','SGBMR29XII',
                'SGBN28VIII','SGBNOV23','SGBNOV24','SGBNOV25','SGBNOV25IX','SGBNOV25VI','SGBNV29VII','SGBOC28VII','SGBOCT25',
                'SGBOCT25IV','SGBOCT25V','SGBOCT26','SGBOCT27','SGBOCT27VI','SGBSEP24','SGBSEP27','SGBSEP28VI','SGBSEP29VI',
                'UTIBANKETF','UTINEXT50','UTINIFTETF','UTISENSETF','UTISXN50','LIQUIDBEES  ', 'KOTAKGOLDETF', 'SBI GOLD ETS',
                'QUANTUM GOLD', 'UTI GOLD ETF', 'NIFTYBEES   ', 'JUNIORBEES  ', 'BANKBEES    ', 'KOTAK PSU BK', 'PSUBNKBEES  ',
                'SHARIABEES  ', 'QNIFTY      ', 'HNGSNGBEES  ', 'MOM50       ', 'KOTAKBKETF  ', 'SETFNIFBK   ', 'SETFNIF50   ',
                'SGB2016I    ', 'SGB2016II   ', 'SGBAUG24    ', 'SGB2016IIA  ', 'SGB2016IIIA ', 'SGB2016IV   ', 'SGBMAY25    ',
                'SGBJULY25   ', 'SGBOCT25A   ', 'SGBNOV25A   ', 'SGBDEC25    ', 'SGBDEC25A   ', 'SGBDEC25B   ', 'SGBOCT26    ',
                'SGBJULY27   ', 'SGBAUG27    ', 'SGBDEC27    ', '716GOI2050  ', 'SGBAPR28    ', 'SGBMAY28    ', 'SGBJULY28   ',
                'SGBAUG28    ', 'SGBSEP28    ', 'SGBOCT28    ', 'SGBNOV28    ', 'SGBJAN29    ', 'SGBJAN29A   ', 'SGBFEB29    ',
                'SGBMAR29    ', 'SGBMAY29    ', 'SGBJUNE29   ', 'SGBJUN29A   ', 'SGBJULY29   ', 'SGBAUG29    ', 'SGBSEP29    ',
                'SGBNOV29    ', '699GOI2051  ', '695GOI2061  ', 'SGBDEC29    ', 'SGBJAN30    ', '735KARSDL40 ', '709APSDL39  ',
                '704APSDL34  ', '693KARSDL32 ', '689GUJSDL31 ', '601RAJSDL26 ', '990IFCI24F  ', '849NTPC25   ', '735PFC35    ',
                '753IRFC30   ', '76NHAI31    ', '749IREDA31  ', '753IREDA26  ', '774IREDA31  ', '768IREDA36  ', '727HUDCO26  ',
                '764HUDCO31  ', '769NHAI31   ', '729HUDCO26  ', '764NABARD31 ', '0MFL23A5    ', '88MMFSL23   ', '10EHFL26    ',
                '900MFL22A   ', '805MMFSL32  ', '9SEFL23B    ', '0SEFL23A    ', '888ERFL28   ', '925ERFL28   ', '0MFL23      ',
                '935SEFL23   ', '0SEFL23     ', '92SEFL28    ', '911JMFCSL23 ', '975JMFCSL28 ', '893STFCL23  ', '903STFCL28  ',
                '93STFCL23   ', '925EFL23    ', '943EFL28    ', '985EFL28    ', '866ICCL23   ', '9ICCL23     ', '92ICCL28    ',
                '890TCFSL23  ', '910TCFSL28  ', '912STFCL23  ', '930STFCL28  ', '10MFL23     ', 'MFL29NOV18D ', '10JMFCSL22  ',
                '0JMFCSL22   ', '967JMFCSL23 ', '995EFL24    ', '1040EFL24   ', 'EFL4JAN19A  ', '1015EFL29   ', '905MMFSL22  ',
                '93MMFSL27   ', '95MMFSL29   ', '1005SEFL24  ', '0SEFL24A    ', '1025KFSRVII ', '1041KFSVIII ', '912STFCL24  ',
                '96IFL22A    ', '10IFL29     ', '975MFL24    ', '1090DLSL22  ', '1050DLSL24  ', '11DLSL24    ', '925LTFL24   ',
                '935LTFL29   ', '898LTFL29   ', '975MFL24A   ', '975MFL22B   ', '89LTFL22    ', '9LTFL24     ', '905LTFL27   ',
                '965SCUF22   ', '975SCUF24   ', '935SCUF24   ', '95MHIL22    ', '1050SEFL22  ', '1025SEFL24A ', '1004JMFPL24 ',
                '102EFL22    ', '0EFL22      ', '995EFL24A   ', '104EFL24    ', '995EFL29    ', '85TCFS24    ', '885TCFS29   ',
                '0IFL22A     ', '0JMFPL26    ', '975MFL23    ', '0MHFL22     ', '1025MHFL24  ', '0ECL23      ', '995ECL24    ',
                '104ECL24    ', '995ECL29    ', '1071KFL25   ', '865LTFL26   ', '95MFL23A    ', '975MFL24BB  ', '0MFL24BB    ',
                '84TCHF28    ', '0EFIL23     ', '1025EFIL25  ', '97JFPL23    ', '0JFPL23     ', '0JFPL25     ', '10KFL23A    ',
                '1025KFL27A  ', '885MFL23    ', '9MFL23B     ', '0MFL23D     ', 'MFLOV24     ', 'MFLOVI25    ', '935EFSL24   ',
                '0EFSL24     ', '939EFSL26   ', '953EFSL31   ', 'MFLII26     ', 'MFLIV26     ', 'MFLVI26     ', '48PFCL24    ',
                '7PFCL31     ', '683PFCL31   ', '697PFCL36   ', '715PFCL36   ', '0KFL23A     ', '825MFL23    ', '0MFL23E     ',
                '0MFL27B     ', '825MFL23A   ', '96IFL28     ', 'MFLVI31F    ', '910EFSL24   ', '930EFSL31   ', '0MMFL23A    ',
                '82IGT31     ', '825MFCL23A  ', '0MFCL23VI   ', 'BILNCD2021  ', '85PCHFL24   ', '875PCHFL26  ', '9PCHFL31A   ',
                '0IHFL28     ', '91EFSL24    ', '915EFSL26   ', 'EFS10SEP21  ', '875MMFL23   ', '10MMFL27    ', '820JMFPL26  ',
                '0IIFL23     ', '925IML22    ', '12IML26     ', '825MFL24    ', '1003UCL24   ', '875EFSL23   ', '875EFSL24A  ',
                '91EFSL24A   ', 'EFSL281221A ', '955EFSL26B  ', 'EFSL281221B ', '97EFSL31A   ', '85MMFL23    ', '820IHFL27   ',
                '843IHFL29   ', '866IHFL25   ', '8MFL24      ', '875MFL28    ', '9MFL30      ', 'ZCMFL24     ', '1015UPPCL27 ',
                '1015UPPCL28 ', 'RCL310718   ', '1025STFCL24 ', '1025STFL24  ', '1175SIBL29  ', 'EFIL261219A ', '1375SIBLPER ',
                '741PFCL30   ', '85BOBPERP   ', '774SBIPER   ', 'PFCBS4      ', '830NHAI27   ', 'HUDCO050327 ', '870LTFL22A  ',
                '870LTFL22B  ', '89SEFL17B   ', '793REC22    ', '738REC27TF  ', '719IIFCL23  ', '734IRFC2028 ', '708IIFCL33  ',
                '801REC23    ', '839HUDCO23  ', '879NHPC28   ', '879PFC28    ', '883HUDCO29  ', '866IIFCL24C ', '891IIFCL34  ',
                '875NHAI29   ', '880IREDA29  ', '861KPL24    ', '900KPL29    ', '888REC29    ', '880IIFCL29  ', 'HDFCW3      ',
                'MOLDTKWARR  ', 'IFCI010811D ', 'IFCI150212D ', 'IFCI310312A ', 'IFCI310312C ', '990IFCI27B  ', '990IFCI32C  ',
                '893PTCIF22A ', '675PCHFL31  ', '1050MSFL22  ', 'KOTAK SENSEX', 'BSE  INFRA  ', 'UTISXN50    ', 'ICICISENSX  ',
                'BSLNIFTY    ', 'DSPN50ETF   ', 'MONQ50      ', 'DSPNEWETF   ', 'ICICICONSU  ', 'MASPTOP50   ', 'AXISCETF    ',
                'AXISTECETF  ', 'AXISHETF    ', 'ICICIFMCG   ', 'MAFSETF     ', 'ICICIPHARM  ', 'INFRABEES   ', 'MAESGETF    ',
                'ICICIBANKN', 'UTIBANKETF  ', 'ICICITECH   ', 'EBBETF0425  ', 'EBBETF0431  ', '07GPG       ', '09GPG       ', '08MPD       ',
                '08GPG       ', '10ARD       ', '10GPG       ', '11DPR       ', '11GPG       ', '11MPD       ', '11MPR       ', '11QPD       ',
                '11AGG       ', '11AMD       ', '11DPD       ', 'ICICIM150   ', 'MANXT50ETF  ', 'EBBETF0430  ', 'ABSLBANETF  ', 'ICICIBANKP  ',
                'ICICIBANKN  ', 'NETFSNX150  ', 'ABSLNN50ET  ', 'MAN50ETF    ', 'SETFSN50    ', 'ICICILIQ    ', 'IPRU3168    ', 'IPRU3169    ',
                'ICICINXT50  ', 'ICICI500    ', 'LIQUIDETF   ', 'AXISCBDPD   ', 'AXISCBGPG   ', 'ICICIB22    ', 'UTINEXT50   ', '7NR         ',
                'ICICILOVOL  ', 'IDFSENSEXE  ', 'ICICIMCAP   ', 'ICICINV20   ', 'UTISXN50', 'NCPSESDL24', 'MAMFGETF', 'NETFSILVER', 'LIQUIDETF',
                'UTISXN50', 'MAMFGETF', 'HBANKETF', 'NHBTF2014', 'HDFCMFGETF', '824GS2027', 'NIFTYBEES', 'MAMFGETF', 'UTISXN50', 'ICICIGOLD',
                'BSLGOLDETF', 'LIQUIDETF', 'AXISGOLD', 'IDBIGOLD', 'ICICINIFTY', 'ICICINF100', 'NETFNIF100  ', 'KOTAKNIFTY', 'CPSE ETF    ',
                'MAESGETF', 'NETFSDL26', 'NETFSENSEX  ', 'SETFBSE100  ', 'SETF10GILT', 'UTISENSETF', 'UTINIFTETF', 'LICNETFN50', 'LICNETFSEN',
                'HDFCNIFETF', 'SXETF       ', 'LICNFNHGP', 'UTISENSETF  ', 'UTINIFTETF  ', 'ICICIBANKP', 'ICICICONSU', 'ICICIFMCG',
                'ICICILIQ', 'ICICILOVOL', 'ICICIM150', 'ICICIMCAP', 'ICICINF100', 'ICICINIFTY', 'ICICINV20', 'ICICINXT50', 'ICICIPHARM', 'ICICI500',
                'ICICIALPLV', 'ICICIAUTO', 'ICICIB22', 'ICICISENSX', 'ICICISILVE', 'ICICITECH', 'KOTAKNIFTY  ', 'LICNETFN50  ', 'LICNETFSEN  ',
                'HDFCNIFETF  ', 'LICNFNHGP   ', 'NIESSPJ     ', 'NIESSPC     ', 'NIEHSPI     ', 'NIESSPE     ', 'NIEHSPD     ', 'NIEHSPE     ',
                'NIEHSPG     ', 'NIEHSPH     ', 'NIEHSPL     ', 'NIESSPL     ', 'NIESSPM     ', 'ABCRSPRG    ', 'ABCRSPDG    ', 'ABMTSPRG    ',
                '667GS2050', '676GS2061', '699GS2051', '737GS2023', '813GS2045', '824GS2027', 'ABSLBANETF', 'ABSLNN50ET', 'AXISBNKETF', 'AXISBPSETF',
                'AXISCETF', 'AXISGOLD', 'AXISHCETF', 'AXISNIFTY', 'AXISTECETF', 'BBETF0432', 'BSLGOLDETF', 'BSLNIFTY', 'BSLSENETFG', 'CPSEETF',
                'DSPN50ETF', 'DSPNEWETF', 'DSPQ50ETF', 'HDFCMFGETF', 'HDFCNIFETF', 'HDFCSENETF', 'IBMFNIFTY', 'IDBIGOLD', 'IDFNIFTYET', 'IVZINGOLD',
                'IVZINNIFTY', 'KOTAKBKETF', 'KOTAKGOLD', 'KOTAKMID50', 'KOTAKNIFTY', 'KOTAKNV20', 'KOTAKPSUBK', 'LICNETFGSC', 'LICNETFN50', 'LICNETFSEN',
                'LICNFNHGP', 'LIQUIDBEES', 'LIQUIDETF', 'MAESGETF', 'MAFSETF', 'MAMFGETF', 'MAN50ETF', 'MANXT50', 'MASPTOP50', 'MC1RG', 'MC2RD', 'MC2RG',
                'MOM100', 'MOM50', 'MON100', 'MONQ50', 'NCPSESDL24', 'NETF', 'NETFAUTO', 'NETFCONSUM', 'NETFDIVOPP', 'NETFGILT5Y', 'NETFIT', 'NETFLTGILT',
                'NETFMID150', 'NETFNIF100', 'NETFNV20', 'NETFPHARMA', 'NETFSDL26', 'NETFSILVER', 'QGOLDHALF', 'QNIFTY', 'SBIETFCON', 'SBIETFIT', 'SBIETFPB',
                'SBIETFQLTY', 'SETFNIF50', 'SETFNIFBK', 'SETFNN50', 'SETUINFRA', 'SGBAPR28I', 'SGBAUG24', 'SGBAUG27', 'SGBAUG28V', 'SGBAUG29V', 'SGBD29VIII',
                'SGBDC27VII', 'SGBDEC25', 'SGBDEC2513', 'SGBDEC25XI', 'SGBFEB24', 'SGBFEB27', 'SGBFEB28IX', 'SGBFEB29XI', 'SGBJ28VIII', 'SGBJAN26', 'SGBJAN27',
                'SGBJAN29IX', 'SGBJAN29X', 'SGBJAN30IX', 'SGBJU29III', 'SGBJUL25', 'SGBJUL27', 'SGBJUL28IV', 'SGBJUL29IV', 'SGBJUN27', 'SGBJUN28',
                'SGBJUN29II', 'SGBMAR24', 'SGBMAR25', 'SGBMAR28X', 'SGBMAY25', 'SGBMAY26', 'SGBMAY28', 'SGBMAY29I', 'SGBMR29XII', 'SGBN28VIII', 'SGBNOV23',
                'SGBNOV24', 'SGBNOV25', 'SGBNOV258', 'SGBNOV25VI', 'SGBNOV26', 'SGBNV29VII', 'SGBOC28VII', 'SGBOCT25', 'SGBOCT25IV', 'SGBOCT26', 'SGBOCT27',
                'SGBOCT27VI', 'SGBSEP24', 'SGBSEP27', 'SGBSEP28VI', 'SGBSEP29VI', 'UTIBANKETF', 'UTINEXT50', 'UTINIFTETF', 'UTISENSETF', 'UTISXN50', 'ESSEN-RE    ', 'SGBOCT25    ', 'SGBMAR28    ', 'SGBJUN28    ', '676GOI2061  ', '664GOI35    ', 'SGBMARCH30  ', '805GUJ2028  ', 'AIRTELPP    ', 'PATINTPP    ', 'WARDWIZPP   ', 'TILAKPP     ', 'PRISMXPP    ', 'ASMTECPP    ', '0IFCI24G    ', '760PFC35    ', '743REC35    ', '732IRFC25   ', '739NHAI31A  ', '764IRFC31   ', '729NABARD26 ', 'MMFSL26A    ', '0MFL25      ', '925SEFL22   ', '0SEFL27     ', '9MFL23      ', '94STFCL28   ', '0STFCL23    ', '0EFL23      ', '965EFL23    ', '925AHFL23   ', '970STFCL28  ', 'MFL29NOV18C ', '101JMFCSL23 ', '915MMFSL24  ', '1015MFL24   ', '0MFL26      ', '0DLSL24     ', '10MFL24     ', '975MHIL24   ', '0EFL24      ', '975MFL24AA  ', '10MFL24A    ', '10KFL22AA   ', '0KFL23AA    ', '922STF24    ', '0STF23      ', '102JMFPL22  ', '985SCUF24   ', '945SCUF24   ', 'BILNCD      ', '10MFL22A    ', '95MFL23     ', '975MFL24B   ', '0MFL23A     ', '0MFL27      ', '0MHFL26     ', '102ECL23    ', '0ECL24      ', '845LTFL22   ', '0LTFL22BB   ', '815LTFL22   ', '801TCH25    ', '875STFCL27  ', '885STFCL23  ', '0STFCL23A   ', '10EFIL23    ', '975MVAFL25  ', '115KLM23    ', '0MFL23C     ', 'MFLIII24    ', 'MFLV24      ', '10KFL24C    ', '85MFL24A    ', 'MFLI24A     ', 'MFLV26E     ', '955EFSL26   ', '0MMFL25B    ', '1025MMFL26A ', 'KLM30JUL21  ', 'EFSL10SEP21 ', '9MMFL23     ', '0KSFL23     ', '842IIFL26   ', 'MFL291021   ', '93EFSL31A   ', 'ZCMMFL27    ', '850MFL27    ', 'ZCMFL30     ', '850EHFL24   ', 'EHFL29422   ', '870EHFL25   ', '915EHFL27   ', '970EHFL32   ', '1015UCL24   ', '1040UCL25   ', '1049DLSL22  ', '872PFC22A   ', '872PFC22    ', '1015UPPCL26 ', 'ELLD2J801A  ', '945SBIPER   ', '855HDFC29   ', 'KFL17DEC20  ', '722REC22TF  ', '875IIFCL33  ', '843PFC23    ', '892PFC33    ', '866NTPC23   ', '901HUDCO34  ', '852NHAI24   ', '848IRFC24   ', '865IRFC29   ', '898HUDCO29  ', '762NTPC35F  ', 'IFCI010811B ', 'IFCI150212C ', 'UCL200721   ', '970UPC29    ', '970UPPC30   ', '97UPPCL26   ', '97UPPCL27   ', '970UPCL31   ', '970UPCL32   ', 'sgbdec26' ,
                '09AGG       ','0MFCL24VII  ','0MHFL24     ','0STFCL24    ','1013DLSL24  ','10KAFL24    ','10KFL22C    ','10KSFL25    ','687MAHSDL33 ',
                '736PFC25    ','750IRFC35   ','795LTFHL22A ','812REC27    ','83TCHF25    ','854PFC28    ','871REC28    ','875SBIPERA  ','876HUDCO24  ',
                '876HUDCO28  ','888IRFC29   ','8MMFL23     ','905EHFL25   ','915EFSL26A  ','915RHFL27B  ','91TMFLPERP  ','935AHFL28   ','95MMFL23    ','95STFCL24   ','96IHFL28    ',
                '975MFL29    ','975MHFL22   ','975MMFL26   ','98EFIL25    ','98EFIL30    ','98EFSL26    ','9IBHFL26B   ', '0KFL25D     ','0KFL25D     ', '0MFL23CC    ', '0MFL23VI    ','0MFL25D     ', '1015HLFL25  ', '1025JFCSL28 ', '10KFIL27    ','1170IOB28   ','703HUDCO23  ','715NTPC25   ','735NHAI31   ','754NHAI30   ','775MFL23    ','830PFC2027  ','845TCFS22   ','846REC28    ','848IIFCL29A ',
                '850SBIPER   ','86LTFL24    ','875MFL23    ','875MFL26A   ','87BOBPER    ','915SEFL17B  ','925KFL24    ','93SCUF22    ','95MFL25     ','96STF24     ','975HLFL26A  ','975UPPCL25  ','990IFCI37D  ','9MFL27      ','9STFCL25    ',
                '08GPG       ','08MPD       ','11AGG       ','11AMD       ','11DPD       ','11DPR       ','11GPG       ','11MPD       ','11MPR       ','11QPD       ']

replace_index = {'Nifty 50':'NSENIFTY','Nifty 100':'NSE100' , 'Nifty 200':'NIFTY200','Nifty 500':'NSE500','Nifty Midcap 50':'NIFTYMIDCAP50',
                 'NIFTY Smallcap 100':'NSESMLCAP100', 'Nifty Auto' : 'NIFTYAUTO','Nifty Bank':'BANKNIFTY','Nifty Energy':'NIFTYENERGY',
                 'Nifty Financial Services':'NIFTYFINSERVICE','Nifty FMCG':'NIFTYFMGC','Nifty IT':'NSEIT','Nifty Media':'NIFTYMEDIA','Nifty Metal':'NIFTYMETAL',
                'Nifty MNC':'NIFTYMNC','Nifty Pharma':'NIFTYPHARMA','Nifty PSU Bank':'NIFTYPSUBANK','Nifty Realty':'NIFTYREALTY','Nifty India Consumption':'NIFTYCONSUMPTION',
                 'Nifty Commodities':'NIFTYCOMMODITIES','Nifty Infrastructure':'NIFTYINFRA','Nifty PSE':'NIFTYPSE','Nifty Services Sector':'NIFTYSERVSECTOR',
                 'Nifty CPSE':'NIFTYCPSE','Nifty Smallcap 50':'NIFTYSMALLCAP50','Nifty Smallcap 250':'NIFTYSMALLCAP250','Nifty Private Bank':'NIFTYPVTBANK'}    #'Nifty Consumer Durables'
def driver_get(url):
    driver.get(url)

def eod_extract(file):
    if (just_filename[:2] == 'EQ'):  # BSE STOCKS
        # st.success("Working on BSE Data : " + just_filename)
        date_bse = str(file[-10:-8])
        mnth_bse = str(file[-8:-6])
        yr_bse = str(file[-6:-4])
        yyyymmdd = str(20) + yr_bse + mnth_bse + date_bse
        with open(file, 'r') as reading:
            file1 = csv.DictReader(reading)
            # file_list = list(file1)
            # st.write(type(file_list[0]['TIMESTAMP']))
            bse_filename = str(file[-10:-4])
            # amibroker_date_format = input()
            with open(path_bhav + 'bse' + bse_filename + '.txt', 'w') as txt:
                for line in file1:
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                            txt.write(
                                line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        #shutil.move(file, path_csv)
        st.success('DONE BSE ' + file)

    elif (just_filename[:2] == 'cm'):  # if(file[-19:-17]=="cm"):                      # NSE STOCKS
        # st.write("Working on NSE Data : " + just_filename)
        date_nse = str(file[-17:-15])
        mnth_format = str(file[-15:-12])
        mnth_nse = mnth_dict[mnth_format]
        yr_nse = str(file[-12:-8])
        yyyymmdd = yr_nse + mnth_nse + date_nse
        with open(file, 'r') as reading:
            file1 = csv.DictReader(reading)
            nse_filename = str(file[-17:-8])
            # amibroker_date_format = input()
            with open(path_bhav + 'nse' + nse_filename + '.txt', 'w') as txt:
                for line in file1:
                    if line['SERIES'] not in avoid_series:
                        if line['SYMBOL'] not in avoid_stocks:
                            txt.write(
                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['TOTTRDQTY'] + "\n")
            # st.write(f'files saved as nse' + nse_filename)
        #shutil.move(file, path_csv)
        st.success('DONE NSE ' + file)

    elif (just_filename[:3] == 'ind'):  # if(file[-19:-17]=="cm"):                      # NSE STOCKS
        only_filename = just_filename.split('.')[0]
        # st.write("Working on INDEX Data : " + only_filename)
        dd = str(only_filename[-8:-6])
        mm = str(only_filename[-6:-4])
        yyyy = str(only_filename[-4:])
        yyyymmdd = yyyy + mm + dd
        with open(file, 'r') as reading:
            index_file = csv.DictReader(reading)
            index_filename = just_filename
            with open(path_bhav + 'nse' + index_filename + '.txt', 'w') as txt:
                for line in index_file:
                    # txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                    if line['Index Name'] in replace_index.keys():
                        txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line[
                            'Open Index Value'] + "," + line[
                                      'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                      'Closing Index Value'] + "," + line['Volume'] + "\n")
                    else:
                        txt.write(
                            line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                'Closing Index Value'] + "," + line['Volume'] + "\n")

def nse_list(path_bhav,path_csv):               #NOT BEING USED NOW
    last_cm = max(glob.glob(path_csv + 'cm' + '*.csv'), key=os.path.getctime)
    cm_file = last_cm.replace("\\", "/")
    with open(cm_file, 'r') as reading:
        file1 = csv.DictReader(reading)
        with open(path_bhav + 'nselist' + '.txt', 'w') as txt:
            for line in file1:
                if line['SERIES'] not in avoid_series:
                    if line['SYMBOL'] not in avoid_stocks:
                        txt.write(line['SYMBOL'] + "\n")
    st.success('DONE NSE List')

#this writes BSE NAMES AS CODE NUMBERS
def bse_list(path_bhav,path_csv):               # NOT BEING USED NOW
    last_cm = max(glob.glob(path_csv + 'EQ' + '*.csv'), key=os.path.getctime)
    cm_file = last_cm.replace("\\", "/")
    with open(cm_file, 'r') as reading:
        file1 = csv.DictReader(reading)
        with open(path_bhav + 'bselist' + '.txt', 'w') as txt:
            for line in file1:
                if line['SC_GROUP'] not in avoid_bse_series :
                    if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                        txt.write(line['SC_CODE'] + "\n")
    st.success('DONE BSE List')

def eod_existing_files(path_bhav,path_csv):
    #st.success(" ok boss, let me work on the existing CSV files now")
    #for filepath in glob.glob("./bhavcopy/*.csv",recursive=False):
    for filepath in glob.glob(r"{}*.csv".format(path_bhav), recursive=False):
        file = filepath.replace("\\","/")
        just_filename = file.split('/')[-1]
        if (os.path.isfile(path_csv + just_filename)):
            st.warning(f'file ' + just_filename + ' already exists')
            pass
        else:
            if (just_filename[:2] == 'EQ'):  # BSE STOCKS
                #st.write("Working on BSE Data : " + file)
                date_bse = str(file[-10:-8])
                mnth_bse = str(file[-8:-6])
                yr_bse = str(file[-6:-4])
                yyyymmdd = str(20) + yr_bse + mnth_bse + date_bse
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    # file_list = list(file1)
                    # st.write(type(file_list[0]['TIMESTAMP']))
                    #bse_filename = path_bhav + '/' + just_filename.split('.CSV')[0] + '.txt'    #str(file[-10:-4])
                    bse_filename = path_bhav + '/' + yyyymmdd + "_" + "BSE.txt"
                    #st.write(bse_filename)
                    with open(bse_filename , 'w') as txt:
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            if line['SC_GROUP'] not in avoid_bse_series :
                                if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                                    txt.write(
                                        line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                        line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    #bse_filename1 = path_bhav + '/' + just_filename.split('.CSV')[0] + 'Code.txt'  # str(file[-10:-4])
                    bse_filename1 = path_bhav + '/' + yyyymmdd + "_" + "BSE_code.txt"
                    with open(bse_filename1, 'w') as txt:
                        txt.write("TICKERCODE, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            txt.write(
                                line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")

                shutil.move(file, path_csv)
                st.success('DONE BSE ' + file)

            elif (just_filename[:2] == 'cm'):  #if(file[-19:-17]=="cm"):                      # NSE STOCKS
                #st.write("Working on NSE Data : " + just_filename)
                date_nse = str(file[-17:-15])
                mnth_format = str(file[-15:-12])
                mnth_nse = mnth_dict[mnth_format]
                yr_nse = str(file[-12:-8])
                yyyymmdd = yr_nse+mnth_nse+date_nse
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    nse_filename = str(file[-17:-8])
                    #amibroker_date_format = input()
                    with open(path_bhav+'nse'+nse_filename+'.txt','w') as txt :
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            if line['SERIES'] not in avoid_series:
                                if line['SYMBOL'] not in avoid_stocks:
                                    txt.write(line['SYMBOL'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['TOTTRDQTY'] + "\n")
                    #st.write(f'files saved as nse' + nse_filename)
                shutil.move(file, path_csv)
                st.success('DONE NSE ' + file)

            elif (just_filename[:3] == 'ind'):  #if(file[-19:-17]=="cm"):                      # NSE STOCKS
                only_filename = just_filename.split('.')[0]
                #st.write("Working on INDEX Data : " + only_filename)
                dd = str(only_filename[-8:-6])
                mm = str(only_filename[-6:-4])
                yyyy = str(only_filename[-4:])
                yyyymmdd = yyyy+mm+dd
                with open(file,'r') as reading:
                    index_file = csv.DictReader(reading)
                    index_filename = just_filename
                    st.write(path_bhav + 'nse' + index_filename + '.txt')
                    with open(path_bhav+'nse'+index_filename+'.txt','w') as txt:
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in index_file:
                            #txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                            if line['Index Name'] in replace_index.keys():
                                txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                    'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                    'Closing Index Value'] + "," + line['Volume'] + "\n" )
                            else :
                                txt.write(line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                    'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                              'Closing Index Value'] + "," + line['Volume'] + "\n")
                shutil.move(file, path_csv)
                st.success('DONE INDICES ' + file)
            elif (just_filename[:3] == 'sec'):
                try:
                    st.write(just_filename)
                    date_nse = str(just_filename[18:20])
                    mnth_nse = str(just_filename[20:22])
                    yr_nse = str(just_filename[22:26])
                    yyyymmdd = yr_nse + mnth_nse + date_nse
                    st.write(yyyymmdd)
                    txt1_name = path_bhav + just_filename.split('.csv')[0] + '.txt'
                    st.write(txt1_name)
                    first_lines = pd.read_csv(file, nrows=10)
                    print(first_lines)
                    for i in range(len(first_lines[' DATE1'])):
                        print("Reading the date now")
                        save_cell_temp = str(first_lines[' DATE1'][i]).strip()
                        date_nse_cell = save_cell_temp[0:2]
                        print(date_nse_cell)
                        mnth_format_cell = save_cell_temp[3:6]
                        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
                        print(mnth_format_cell)
                        print(mnth_nse_cell)
                        yr_nse_cell = str(save_cell_temp[7:])
                        print(yr_nse_cell)
                        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
                        st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
                        '''
                        date_nse_cell = first_lines[' DATE1'][i][0:2]
                        print(date_nse_cell)
                        mnth_format_cell = first_lines[' DATE1'][i][3:6]
                        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
                        print(mnth_format_cell)
                        print(mnth_nse_cell)
                        yr_nse_cell = str(20) + str(first_lines[' DATE1'][i][7:])
                        print(yr_nse_cell)
                        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
                        st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)'''
                    if yyyymmdd == yyyymmdd_cell:
                        with open(file, 'r') as reading:
                            nse_full_file = csv.DictReader(reading)
                            print("Read csv file")
                            with open(txt1_name, 'a') as txt:
                                txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                                print("STARTED WERITING TEXT FILE")
                                for line in nse_full_file:
                                    if line[' SERIES'] not in avoid_series:
                                        if line['SYMBOL'] not in avoid_stocks:
                                            txt.write(
                                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                                line[
                                                    ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                                    ' CLOSE_PRICE'] + "," + line[
                                                    ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
                        st.success("Created file in " + txt1_name)
                    else:
                        st.error("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
                    shutil.move(file, path_csv)
                    st.success('DONE FULLBHAV ' + file)

                except:
                    pass

# this will download files locally in the local computer.
def download_all_data(driver,indexlink, bselink, nselink,path_bhav,path_csv,path_download,nse_full_link,possible_fullbhav_name):
    # DOWNLOAD INDEX FILE and MOVE TO BHAVCOPY LOCATION
    try:
        index_d = driver.get(indexlink)
        sleep(2)
        last_created_file = max(glob.glob(path_download + '*.csv'), key=os.path.getctime)
        shutil.move(last_created_file, path_bhav)
    except:
        st.warning('unable to download Index file')
    # DOWNLOAD BSE FILE and MOVE TO BHAVCOPY LOCATION
    try:
        bse_d = driver.get(bselink)
        # bse_zip = ZipFile(BytesIO(bse_d.content))
        # bse_zip.extractall(r'{}'.format(path_bhav))
        sleep(2)
        last_created_file = max(glob.glob(path_download + '*.zip'), key=os.path.getctime)
        shutil.move(last_created_file, path_bhav)
        last_zip = max(glob.glob(path_bhav + '*.zip'), key=os.path.getctime)
        try:
            with ZipFile(last_zip, 'r') as zip:
                # list all the contents of the zip file
                #st.write(f'{zip.infolist()}')
                zip.extractall(path_bhav)
        except:
            st.warning('Couldnt Extract bse file')
    except:
        st.warning('Couldnt Download bse file')

    # DOWNLOAD NSE FILE THROUGH REQUESTS
    try:
        nse_d = requests.get(nselink)
        nse_zip = ZipFile(BytesIO(nse_d.content))
        nse_zip.extractall(r'{}'.format(path_bhav))
    except:
        st.warning("Couldnt download nse file")
    try:
        with urllib.request.urlopen(nse_full_link) as test_nse_file, open(f'' + path_bhav + '/' + possible_fullbhav_name, 'w',
                                                                          newline="") as f:
            f.write(test_nse_file.read().decode())
        date_nse = str(possible_fullbhav_name[18:20])
        # st.write(date_nse)
        mnth_nse = str(possible_fullbhav_name[20:22])
        # st.write(mnth_nse)
        yr_nse = str(possible_fullbhav_name[22:26])
        # st.write(yr_nse)
        yyyymmdd = yr_nse + mnth_nse + date_nse
        txt1_name = possible_fullbhav_name.split('.csv')[0] + '.txt'
        first_lines = pd.read_csv(f'' + path_bhav + '/' +possible_fullbhav_name, nrows=10)
        for i in range(len(first_lines[' DATE1'])):
            date_nse_cell = first_lines[' DATE1'][i][1:3]
            mnth_format_cell = first_lines[' DATE1'][i][4:7]
            mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
            yr_nse_cell = str(first_lines[' DATE1'][i][8:])
            yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
            # st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
        if yyyymmdd == yyyymmdd_cell:
            with open(f'' + path_bhav + '/' +possible_fullbhav_name, 'r') as reading:
                nse_full_file = csv.DictReader(reading)
                with open(f'' + path_bhav + '/' + txt1_name, 'a') as txt:
                    txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                    for line in nse_full_file:
                        if line[' SERIES'] not in avoid_series:
                            if line['SYMBOL'] not in avoid_stocks:
                                txt.write(
                                    line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                    line[
                                        ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                        ' CLOSE_PRICE'] + "," + line[
                                        ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
            st.write("DONE FULL BHAVCOPY:   " + yyyymmdd)
            shutil.move(path_bhav + '/' + possible_fullbhav_name, path_csv)
        else:
            st.error("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
    except:
        pass

# This EODDATE function requires other functions viz., download_all_data, eod_existing_files.
def eod_date(driver,ddmmmyyyy,path_bhav,path_csv,path_download):
    # downloads links from nse and bse
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
    bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
    indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    st.write(f'NSE link is : ' + nselink)
    st.write(f'BSE link is : ' + bselink)
    st.write(f'Index link is : ' + indexlink)
    try:
        download_all_data(driver,indexlink, bselink, nselink,path_bhav,path_csv,path_download,nse_full_link,possible_fullbhav_name)
        #st.success("Done downloading, lets try extracting now")
        eod_existing_files(path_bhav,path_csv)
    except BadZipFile:
        pass

def main():
    #driver = webdriver.Edge(r"./msedgedriver.exe")
    #driver.minimize_window()
    with st.sidebar:
        # PATHS OF THIS COMPUTER
        st.info("pls mention here your computer paths")
        path_bhav = st.text_input("path_bhav", value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/')  # './bhavcopy/')
        path_csv = st.text_input("path_csv",
                                 value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')  # './bhavcopy/csv')
        path_download = st.text_input("path_download", value='C:/Users/sahaveer/Downloads/')

    my_date = st.date_input("Select date", value=date.today(),
                            min_value=datetime.date(1990, 1, 1))
    ddmmmyyyy = my_date.strftime("%d%b%Y")
    #if st.button("Download"):
    #    eod_date(driver, ddmmmyyyy, path_bhav, path_csv, path_download)
    #st.write("___")
    if st.button("Existing"):
        eod_existing_files(path_bhav, path_csv)
        st.write("done EXISTing files")
    st.write("___")
    col1, col2 = st.columns([1, 1])
    with col1:
        my1_date = st.date_input("FROM", value=date.today(),
                                 min_value=datetime.date(1990, 1, 1))
    with col2:
        if my1_date is not date.today():
            my2_date = st.date_input("TILL", value=min(my1_date + timedelta(60), date.today()),
                                     min_value=datetime.date(1990, 1, 1))
        else:
            my2_date = st.date_input("TILL", value=date.today(),
                                     min_value=datetime.date(1990, 1, 1))
    if st.button("GENERATE BHAVCOPIES"):
        try:
            download_bhav(my1_date, my2_date)
            # download_bhav(nselink,bselink, indexlink, possible_index_name)
            # st.success("Done downloading, lets try extracting now")
            # eod_existing_files(path_bhav, path_csv)
        except BadZipFile:
            st.error("BadZipFile")
            pass

def index_file(indexlink,possible_index_name,txt1_name):
    # INDEX FILE
    with urllib.request.urlopen(indexlink) as testfile, open(f'./bhavfiles/' + possible_index_name + '.csv',
                                                             'w',
                                                             newline="") as f:
        f.write(testfile.read().decode())
    dd = str(possible_index_name[-8:-6])
    mm = str(possible_index_name[-6:-4])
    yyyy = str(possible_index_name[-4:])
    yyyymmdd = yyyy + mm + dd
    with open(f'./bhavfiles/' + possible_index_name + '.csv', 'r') as reading:
        index_file = csv.DictReader(reading)
        with open(txt1_name, 'a') as txt:
            txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
            for line in index_file:
                # txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                if line['Index Name'] in replace_index.keys():
                    txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line[
                        'Open Index Value'] + "," + line[
                                  'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                  'Closing Index Value'] + "," + line['Volume'] + "\n")
                else:
                    txt.write(
                        line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                            'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                            'Closing Index Value'] + "," + line['Volume'] + "\n")

def bse_file(bselink,yyyymmdd):
    bse_file_name = './bhavfiles/bse_temp_file.zip'
    # Add a User-Agent header to the request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    # Download the file
    urllib.request.urlretrieve(bselink, bse_file_name)
    # OPENS DOWNLOADED ZIP FILE AND EXTRACTS CSV FILE
    with ZipFile(bse_file_name, 'r') as zip:
        # list all the contents of the zip file
        for zipinfo in zip.infolist():
            with zip.open(zipinfo) as file:
                file2 = str(zipinfo.filename)
                print(file2)
        zip.extractall('./bhavfiles/')
        # print("Extracted succesfully")
    txt3_name = './bhavfiles/' + file2.split('.CSV')[0] + '.txt'

    with open(f'./bhavfiles/' + file2, 'r') as reading:
        bse_full_file = csv.DictReader(reading)
        with open(txt3_name, 'a') as txt:
            txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
            for line in bse_full_file:
                # print(line)
                if line['SC_GROUP'] not in avoid_bse_series:
                    if line['SC_NAME'] not in avoid_bse_stocks and line['SC_NAME'] not in avoid_stocks:
                        txt.write(line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line[
                            'HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
    return txt3_name

def nse_file(nse_full_link,possible_fullbhav_name,txt2_name):

    with urllib.request.urlopen(nse_full_link) as test_nse_file, open(f'' + possible_fullbhav_name, 'w',
                                                                      newline="") as f:
        f.write(test_nse_file.read().decode())
    st.info("downloaded nse file")
    #               NSE WHOLE BHAVCOPY
    # st.write("getting yyyymmdd from file name")
    # sec_bhavdata_full_23082022.csv
    # st.write(possible_fullbhav_name)
    date_nse = str(possible_fullbhav_name[18:20])
    #st.write(date_nse)
    mnth_nse = str(possible_fullbhav_name[20:22])
    #st.write(mnth_nse)
    yr_nse = str(possible_fullbhav_name[22:26])
    #st.write(yr_nse)
    yyyymmdd = yr_nse + mnth_nse + date_nse
    txt1_name = possible_fullbhav_name.split('.csv')[0] + '.txt'
    first_lines = pd.read_csv(possible_fullbhav_name, nrows=10)
    for i in range(len(first_lines[' DATE1'])):
        date_nse_cell = first_lines[' DATE1'][i][1:3]
        mnth_format_cell = first_lines[' DATE1'][i][4:7]
        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
        yr_nse_cell = str(first_lines[' DATE1'][i][8:])
        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
        # st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
    if yyyymmdd == yyyymmdd_cell:
        print("bOTH DATES ARE SAME")
        with open(possible_fullbhav_name, 'r') as reading:
            nse_full_file = csv.DictReader(reading)
            with open(txt2_name, 'a') as txt:
                txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                for line in nse_full_file:
                    if line[' SERIES'] not in avoid_series:
                        if line['SYMBOL'] not in avoid_stocks:
                            txt.write(
                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                line[
                                    ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                    ' CLOSE_PRICE'] + "," + line[
                                    ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
        return "success"
    else:
        st.info("Both dates are not same")
        return "fail"

def download_bhav(my1_date,my2_date):              #nselink,bselink,indexlink,possible_index_name):
    ddmmmyyyy1 = my1_date.strftime("%d%b%Y")
    ddmmmyyyy2 = my2_date.strftime("%d%b%Y")
    created_zip = ZipFile("EOD.zip", "w")
    created_zip.close()
    mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    delta = timedelta(days=1)
    files_list = []
    ddmmmyyyy = ddmmmyyyy1
    while my1_date <= my2_date:
        #st.write(my1_date)
        #st.success("started loop")
        ddmmmyyyy = my1_date.strftime("%d%b%Y")
        weekday_num = datetime.datetime.strptime(ddmmmyyyy, '%d%b%Y').weekday()
        if weekday_num == 5 or weekday_num == 6:
            my1_date += timedelta(1)
            pass
        else :
            mmm_to_d = str(ddmmmyyyy[2:5].upper())
            mm_to_d = str(mnth_dict[mmm_to_d])
            dd_to_d = str(ddmmmyyyy[0:2])
            yy_to_d = str(ddmmmyyyy[-2:])
            yyyy_to_d = str(ddmmmyyyy[-4:])
            yyyymmdd = yyyy_to_d + mm_to_d + dd_to_d
            #https://archives.nseindia.com/products/content/sec_bhavdata_full_30122022.csv
            #https://www1.nseindia.com/content/indices/ind_close_all_30122022.csv
            #TEMPORARILY, NOT USING NSELINK
            nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
            # possible_nse_name = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'full.csv'
            bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
            indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
            # NSEFULLLINK GIVES DELIVERY DATA AS WELL
            nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_"+ dd_to_d + mm_to_d + yyyy_to_d + ".csv"
            possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
            possible_index_name = 'ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d
            txt1_name = './bhavfiles/' + possible_index_name + '.txt'
            txt2_name = './bhavfiles/' + possible_fullbhav_name.split('.csv')[0] + '.txt'

            # INDEX FILE, FULL BHAVCOPY,
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading INDEX FILE: " + ddmmmyyyy)
                index_file(indexlink,possible_index_name,txt1_name)
                with col2:
                    st.write("DONE INDEX BHAVCOPY:    " + yyyymmdd)
                # write the text file into a zipped file
                with ZipFile("EOD.zip", "a") as m_zip:
                    m_zip.write(txt1_name)
            except:
                #st.info("Could not download index file. Try downloading using this link :")
                st.write(indexlink)

            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading BSE FILE: " + ddmmmyyyy)
                txt3_name = bse_file(bselink,yyyymmdd)
                with col2:
                    st.write("DONE BSE BHAVCOPY:    " + yyyymmdd)
                # write the text file into a zipped file
                with ZipFile("EOD.zip", "a") as m_zip:
                    m_zip.write(txt3_name)
            except:
                #st.info("Could not download BSE file. Try downloading using this link :")
                st.write(bselink)
            # NSE FILE
            try:
                result = ""
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading NSE FULL BHAV FILE: " + ddmmmyyyy)

                result = nse_file(nse_full_link,possible_fullbhav_name,txt2_name)
                st.info("Returned from nse_file function")
                print(result)
                if result == "success":
                    with col2:
                        st.write("DONE FULL BHAVCOPY:   " + yyyymmdd)
                    with ZipFile("EOD.zip", "a") as m_zip:
                        m_zip.write(txt2_name)
                elif result == "fail":
                    st.info("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
            except:
                #st.info("Could not download NSE file. Try downloading using this link :")
                st.write(nse_full_link)
            # LOOP and get into the next date
            my1_date += timedelta(1)

    # PROVIDE THE UPDATED ZIP FILE AS DOWNLOADABLE CONTENT
    with open("EOD.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="EOD.zip",
            mime="application/octet-stream"
        )

    st.markdown("____")
    st.markdown("**Download your copy and PLS spread YOUR LOVE by sharing BHAVCOPY to NEAR and DEAR one\'s**")

    st.markdown("____")
    #with open(txt_name) as f:
    #    st.download_button('DOWNLOAD BHAVCOPY', f, file_name=txt_name)  # Defaults to 'text/plain'

    '''
    try:
        bse_d = urllib.request.urlopen(bselink.content()
        with ZipFile(BytesIO(bse_d)) as my_zip_file:
            for file in my_zip_file.namelist():
                st.info(file)
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    #       PRINTS WHOLE DATA AS DISCTIONARY
                    for line in file1:
                        print(line)
        #index_zip = ZipFile(BytesIO(bse_d.content))
        # bse_zip.extractall(r'{}'.format(path_bhav))
    except:
        st.warning('unable to download Index file')
    '''

if __name__ == '__main__':
    main()
