import mysql.connector
from hashlib import md5
from time import time
import string
import random
import time
import calendar

from datetime import datetime


conn = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', port=3306, database='mydatabase', auth_plugin='mysql_native_password')

cursor = conn.cursor()


sql ='''CREATE TABLE IF NOT EXISTS CATEGORY_1(
    DATE_TIME BIGINT,
    CELL_ID INT,
    STATION_ID INT NOT NULL,
    PRODUCT_ID INT,
    BARCODE_ID BIGINT(11),
    DISC_CONCENTRIC FLOAT,
    DISC_RUNOUT INT,
    AIR_GAP INT,
    LATHE_AIR_GAP_NOM INT,
    LATHE_AIR_GAP_TOL INT,
    LATHE_VAL_NOM INT,
    LATHE_VAL_ACT INT,
    LATHE_ERROR INT,
    LATHE_AMOUNT_LIFT INT,
    LATHE_ASIC_HEIGHT INT,
    LATHE_DISC_THICK INT,
    LATHE_AXIAL_PLAY INT,
    LATHE_MATERIAL_THICK INT,
    FORCE_STROKE_CONTROL_DISK_FLANGE INT,
    FORCE_STROKE_CONTROL_CROSSBAR INT,
    CURRENT_DRAIN_BISS_COLD_ST INT,
    CURRENT_DRAIN_BISS_COLD_MT INT,
    CURRENT_DRAIN_BISS_KPP_COLD_ST INT,
    CURRENT_DRAIN_BISS_KPP_COLD_MT INT,
    CURRENT_DRAIN_DQ_COLD_ST INT,
    CURRENT_DRAIN_DQ_COLD_MT INT,
    CURRENT_DRAIN_BISS_HOT_ST INT,
    CURRENT_DRAIN_BISS_HOT_MT INT,
    ALIGNMENT_DJH_DJL_DIFF INT,
    ALIGNMENT_PHASE_DIFF INT,
    ALIGN_OPT_GEAR_ST INT,
    ALIGN_OPT_GEAR_MT INT,
    MV1_OFF_VER INT,
    MV2_OFF_VER INT,
    MV3_OFF_VER INT,
    CFG_BIAS FLOAT,
    MR_PT1000_R1270 FLOAT,
    MR_PT1000_R1385 FLOAT,
    MR_PT1000_R1470 FLOAT,
    GFS_CORR_DEZ_COLD INT,
    GFC_CORR_DEZ_COLD INT,
    OFS_CORR_DEZ_COLD INT,
    OFC_CORR_DEZ_COLD INT,
    RG_AMPS_CW_COLD INT,
    RG_AMPC_CW_COLD INT,
    RG_AMP_PCO_2048_CW_COLD INT,
    RG_DC_PCO_2048_CW_COLD INT,
    RG_DARK_PCO_2048_CW_COLD INT,
    RG_CONTRAST_PCO_2048_CW_COLD INT,
    RG_AMP_PC_1024_CW_COLD INT,
    RG_AMP_NC_1024_CW_COLD INT,
    RG_DC_PC_1024_CW_COLD INT,
    RG_DC_NC_1024_CW_COLD INT,
    RG_DARK_PC_1024_CW_COLD INT,
    RG_DARK_NC_1024_CW_COLD INT,
    RG_CONTRAST_PC_1024_CW_COLD INT,
    RG_CONTRAST_NC_1024_CW_COLD INT,
    RG_CONTRAST_PC_PCO_CW_COLD INT,
    GFS_CORR_DEZ_HOT INT,
    GFC_CORR_DEZ_HOT INT,
    RG_AMPS_CW_HOT INT,
    RG_AMPC_CW_HOT INT,
    RG_AMP_PCO_2048_CW_HOT INT,
    RG_AMP_NCO_2048_CW_HOT INT,
    RG_DC_PCO_2048_CW_HOT INT,
    RG_DC_NCO_2048_CW_HOT INT,
    RG_DARK_PCO_2048_CW_HOT INT,
    RG_DARK_NCO_2048_CW_HOT INT,
    RG_CONTRAST_PCO_2048_CW_HOT FLOAT,
    RG_CONTRAST_NCO_2048_CW_HOT FLOAT,
    RG_AMP_PC_1024_CW_HOT INT,
    RG_AMP_NC_1024_CW_HOT INT,
    RG_DC_PC_1024_CW_HOT INT,
    RG_DC_NC_1024_CW_HOT INT,
    RG_DARK_PC_1024_CW_HOT INT,
    RG_DARK_NC_1024_CW_HOT INT,
    RG_CONTRAST_PC_1024_CW_HOT FLOAT,
    RG_CONTRAST_NC_1024_CW_HOT FLOAT,
    RG_CONTRAST_PC_PCO_CW_HOT FLOAT,
    GFS_CORR_DEZ_KPP_COLD INT,
    GFC_CORR_DEZ_KPP_COLD INT,
    RG_AMPS_CW_KPP_COLD INT,
    RG_AMPC_CW_KPP_COLD INT,
    RG_AMP_PCO_2048_CW_KPP_COLD INT,
    RG_AMP_NCO_2048_CW_KPP_COLD INT,
    RG_DC_PCO_2048_CW_KPP_COLD INT,
    RG_DC_NCO_2048_CW_KPP_COLD INT,
    RG_DARK_PCO_2048_CW_KPP_COLD INT,
    RG_DARK_NCO_2048_CW_KPP_COLD INT,
    RG_CONTRAST_PCO_2048_CW_KPP_COLD FLOAT,
    RG_CONTRAST_NCO_2048_CW_KPP_COLD FLOAT,
    RG_AMP_PC_1024_CW_KPP_COLD INT,
    RG_AMP_NC_1024_CW_KPP_COLD INT,
    RG_DC_PC_1024_CW_KPP_COLD INT,
    RG_DC_NC_1024_CW_KPP_COLD INT,
    RG_DARK_PC_1024_CW_KPP_COLD INT,
    RG_DARK_NC_1024_CW_KPP_COLD INT,
    RG_CONTRAST_PC_1024_CW_KPP_COLD FLOAT,
    RG_CONTRAST_NC_1024_CW_KPP_COLD FLOAT,
    RG_CONTRAST_PC_PCO_CW_KPP_COLD FLOAT,
    EXT_ONESTEP_ST_CCW_COLD VARCHAR(3),
    EXT_ONESTEP_ST_CW_COLD INT,
    RG_STATUS_SC_CCW_COLD VARBINARY(20),
    RG_STATUS_CC_CCW_COLD VARBINARY(20),
    MR_STATUS_CCW_COLD VARBINARY(20),
    RG_STATUS_SC_CW_COLD VARBINARY(20),
    RG_STATUS_CC_CW_COLD VARBINARY(20),
    MR_STATUS_CW_COLD VARBINARY(20),
    POLLUTION_2048_HIGH_MAX_COLD INT,
    POLLUTION_2048_HIGH_MIN_COLD VARCHAR(3),
    POLLUTION_2048_LOW_MAX_COLD INT,
    POLLUTION_2048_LOW_MIN_COLD VARCHAR(3),
    POLLUTION_1024_HIGH_MAX_COLD INT,
    POLLUTION_1024_HIGH_MIN_COLD VARCHAR(3),
    POLLUTION_1024_LOW_MAX_COLD INT,
    POLLUTION_1024_LOW_MIN_COLD VARCHAR(3),
    INDEX ID(CELL_ID,STATION_ID,PRODUCT_ID)
)'''
cursor.execute(sql)

param_list=[]
date_time=[]
station_id=[]
cell_id=[]
product_id=[]
barcode_id=[]
DISC_CONCENTRIC=[]
DISC_RUNOUT=[]
AIR_GAP =[]
LATHE_AIR_GAP_NOM =[]
LATHE_AIR_GAP_TOL=[]
LATHE_VAL_NOM =[]
LATHE_VAL_ACT =[]
LATHE_ERROR =[]
LATHE_AMOUNT_LIFT =[]
LATHE_ASIC_HEIGHT=[]
LATHE_DISC_THICK =[]
LATHE_AXIAL_PLAY=[]
LATHE_MATERIAL_THICK=[]
FORCE_STROKE_CONTROL_DISK_FLANGE =[]
FORCE_STROKE_CONTROL_CROSSBAR =[]

CURRENT_DRAIN_BISS_COLD_ST =[]
CURRENT_DRAIN_BISS_COLD_MT =[]
CURRENT_DRAIN_BISS_KPP_COLD_ST =[]
CURRENT_DRAIN_BISS_KPP_COLD_MT =[]
CURRENT_DRAIN_DQ_COLD_ST =[]
CURRENT_DRAIN_DQ_COLD_MT =[]
CURRENT_DRAIN_BISS_HOT_ST =[]
CURRENT_DRAIN_BISS_HOT_MT =[]

ALIGNMENT_DJH_DJL_DIFF =[]
ALIGNMENT_PHASE_DIFF =[]

ALIGN_OPT_GEAR_ST =[]
ALIGN_OPT_GEAR_MT =[]

MV1_OFF_VER =[]
MV2_OFF_VER =[]
MV3_OFF_VER =[]
CFG_BIAS =[]
MR_PT1000_R1270 =[]
MR_PT1000_R1385 =[]
MR_PT1000_R1470 =[]

GFS_CORR_DEZ_COLD =[]
GFC_CORR_DEZ_COLD =[]
OFS_CORR_DEZ_COLD =[]
OFC_CORR_DEZ_COLD =[]
RG_AMPS_CW_COLD =[]
RG_AMPC_CW_COLD =[]
RG_AMP_PCO_2048_CW_COLD =[]
RG_DC_PCO_2048_CW_COLD =[]
RG_DARK_PCO_2048_CW_COLD =[]
RG_CONTRAST_PCO_2048_CW_COLD =[]
RG_AMP_PC_1024_CW_COLD =[]
RG_AMP_NC_1024_CW_COLD =[]
RG_DC_PC_1024_CW_COLD =[]
RG_DC_NC_1024_CW_COLD =[]
RG_DARK_PC_1024_CW_COLD =[]
RG_DARK_NC_1024_CW_COLD =[]
RG_CONTRAST_PC_1024_CW_COLD =[]
RG_CONTRAST_NC_1024_CW_COLD =[]
RG_CONTRAST_PC_PCO_CW_COLD =[]

GFS_CORR_DEZ_HOT =[]
GFC_CORR_DEZ_HOT =[]
RG_AMPS_CW_HOT =[]
RG_AMPC_CW_HOT =[]
RG_AMP_PCO_2048_CW_HOT =[]
RG_AMP_NCO_2048_CW_HOT =[]
RG_DC_PCO_2048_CW_HOT =[]
RG_DC_NCO_2048_CW_HOT =[]
RG_DARK_PCO_2048_CW_HOT =[]
RG_DARK_NCO_2048_CW_HOT =[]
RG_CONTRAST_PCO_2048_CW_HOT =[]
RG_CONTRAST_NCO_2048_CW_HOT =[]
RG_AMP_PC_1024_CW_HOT =[]
RG_AMP_NC_1024_CW_HOT =[]
RG_DC_PC_1024_CW_HOT =[]
RG_DC_NC_1024_CW_HOT =[]
RG_DARK_PC_1024_CW_HOT =[]
RG_DARK_NC_1024_CW_HOT =[]
RG_CONTRAST_PC_1024_CW_HOT =[]
RG_CONTRAST_NC_1024_CW_HOT =[]
RG_CONTRAST_PC_PCO_CW_HOT =[]

GFS_CORR_DEZ_KPP_COLD =[]
GFC_CORR_DEZ_KPP_COLD =[]
RG_AMPS_CW_KPP_COLD =[]
RG_AMPC_CW_KPP_COLD =[]
RG_AMP_PCO_2048_CW_KPP_COLD =[]
RG_AMP_NCO_2048_CW_KPP_COLD =[]
RG_DC_PCO_2048_CW_KPP_COLD =[]
RG_DC_NCO_2048_CW_KPP_COLD =[]
RG_DARK_PCO_2048_CW_KPP_COLD =[]
RG_DARK_NCO_2048_CW_KPP_COLD =[]
RG_CONTRAST_PCO_2048_CW_KPP_COLD =[]
RG_CONTRAST_NCO_2048_CW_KPP_COLD =[]
RG_AMP_PC_1024_CW_KPP_COLD =[]
RG_AMP_NC_1024_CW_KPP_COLD =[]
RG_DC_PC_1024_CW_KPP_COLD =[]
RG_DC_NC_1024_CW_KPP_COLD =[]
RG_DARK_PC_1024_CW_KPP_COLD =[]
RG_DARK_NC_1024_CW_KPP_COLD =[]
RG_CONTRAST_PC_1024_CW_KPP_COLD =[]
RG_CONTRAST_NC_1024_CW_KPP_COLD =[]
RG_CONTRAST_PC_PCO_CW_KPP_COLD =[]

EXT_ONESTEP_ST_CCW_COLD=[]
EXT_ONESTEP_ST_CW_COLD =[]
RG_STATUS_SC_CCW_COLD =[]
RG_STATUS_CC_CCW_COLD =[]
MR_STATUS_CCW_COLD =[]
RG_STATUS_SC_CW_COLD =[]
RG_STATUS_CC_CW_COLD =[]
MR_STATUS_CW_COLD =[]
POLLUTION_2048_HIGH_MAX_COLD =[]
POLLUTION_2048_HIGH_MIN_COLD =[]
POLLUTION_2048_LOW_MAX_COLD =[]
POLLUTION_2048_LOW_MIN_COLD =[]
POLLUTION_1024_HIGH_MAX_COLD =[]
POLLUTION_1024_HIGH_MIN_COLD =[]
POLLUTION_1024_LOW_MAX_COLD =[]
POLLUTION_1024_LOW_MIN_COLD =[]

start_time = int(time.time())
end_time = start_time + 5184000
for j in range(50):
    for i in range(0,20000):
        cell_id.append(str(random.randint(1,5)))
        station_id.append(str(random.randint(1,20)))
        product_id.append(str(random.randint(1,200)))
        barcode_id.append(str(''.join(random.choices(string.digits, k=10))))
        date_time.append(str(random.randint(start_time, end_time)))
        DISC_CONCENTRIC.append(str('.'.join(random.choices(string.digits, k=2))))
        DISC_RUNOUT.append(str(random.randint(1,5)))
        AIR_GAP .append(str(random.randint(100,110)))
        LATHE_AIR_GAP_NOM.append(str(random.randint(100,150)))
        LATHE_AIR_GAP_TOL.append(str(random.randint(1,10)))
        LATHE_VAL_NOM.append(str(random.randint(2100,2500)))
        LATHE_VAL_ACT.append("-"+str(random.randint(2100,2500)))
        LATHE_ERROR.append(str(random.randint(0,1)))
        LATHE_AMOUNT_LIFT.append(str(random.randint(600,700)))
        LATHE_ASIC_HEIGHT.append(str(random.randint(1000,1100)))
        LATHE_DISC_THICK.append(str(random.randint(1100,1200)))
        LATHE_AXIAL_PLAY.append("-"+str(random.randint(1,4)))
        LATHE_MATERIAL_THICK.append("-"+str(random.randint(1600,1800)))
        FORCE_STROKE_CONTROL_DISK_FLANGE.append(str(random.randint(0,1)))
        FORCE_STROKE_CONTROL_CROSSBAR.append(str(random.randint(0,1))),

        CURRENT_DRAIN_BISS_COLD_ST.append(str(random.randint(30,50)))
        CURRENT_DRAIN_BISS_COLD_MT.append(str('.'.join(random.choices(string.digits, k=2))))
        CURRENT_DRAIN_BISS_KPP_COLD_ST.append(str(random.randint(30,50)))
        CURRENT_DRAIN_BISS_KPP_COLD_MT.append(str('.'.join(random.choices(string.digits, k=2))))
        CURRENT_DRAIN_DQ_COLD_ST.append(str(random.randint(30,50)))
        CURRENT_DRAIN_DQ_COLD_MT.append(str('.'.join(random.choices(string.digits, k=2))))
        CURRENT_DRAIN_BISS_HOT_ST.append(str(random.randint(30,50)))
        CURRENT_DRAIN_BISS_HOT_MT.append(str('.'.join(random.choices(string.digits, k=2))))

        ALIGNMENT_DJH_DJL_DIFF.append(str(random.randint(10,30)))
        ALIGNMENT_PHASE_DIFF.append(str('.'.join(random.choices(string.digits, k=2))))

        ALIGN_OPT_GEAR_ST.append(str(random.randint(0,1)))
        ALIGN_OPT_GEAR_MT.append(str(random.randint(0,1)))

        MV1_OFF_VER.append(str(random.randint(0,1)))
        MV2_OFF_VER.append(str(random.randint(0,1)))
        MV3_OFF_VER.append(str(random.randint(0,1)))
        CFG_BIAS.append("1."+''.join(random.choices(string.digits, k=3)))
        MR_PT1000_R1270.append(str(random.randint(60,80))+"."+str(random.randint(1,9)))
        MR_PT1000_R1385.append(str(random.randint(95,105))+"."+str(random.randint(0,9)))
        MR_PT1000_R1470.append(str(random.randint(120,130))+"."+str(random.randint(0,9)))

        GFS_CORR_DEZ_COLD.append("0"+''.join(random.choices(string.digits, k=2)))
        GFC_CORR_DEZ_COLD.append("0"+''.join(random.choices(string.digits, k=2)))
        OFS_CORR_DEZ_COLD.append(str(random.randint(250,260)))
        OFC_CORR_DEZ_COLD.append("00"+str(random.randint(0,1)))
        RG_AMPS_CW_COLD.append(str(random.randint(360,390)))
        RG_AMPC_CW_COLD.append(str(random.randint(360,390)))
        RG_AMP_PCO_2048_CW_COLD.append(str(random.randint(150,200)))
        RG_DC_PCO_2048_CW_COLD.append(str(random.randint(1100,1200)))
        RG_DARK_PCO_2048_CW_COLD.append(str(random.randint(800,850)))
        RG_CONTRAST_PCO_2048_CW_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_AMP_PC_1024_CW_COLD.append(str(random.randint(140,160)))
        RG_AMP_NC_1024_CW_COLD.append(str(random.randint(140,160)))
        RG_DC_PC_1024_CW_COLD.append(str(random.randint(810,850)))
        RG_DC_NC_1024_CW_COLD.append(str(random.randint(810,850)))
        RG_DARK_PC_1024_CW_COLD.append(str(random.randint(600,650)))
        RG_DARK_NC_1024_CW_COLD.append(str(random.randint(600,650)))
        RG_CONTRAST_PC_1024_CW_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_NC_1024_CW_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_PC_PCO_CW_COLD.append("1."+''.join(random.choices(string.digits, k=3)))

        GFS_CORR_DEZ_HOT.append("0"+''.join(random.choices(string.digits, k=2)))
        GFC_CORR_DEZ_HOT.append("0"+''.join(random.choices(string.digits, k=2)))
        RG_AMPS_CW_HOT.append(str(random.randint(360,400)))
        RG_AMPC_CW_HOT.append(str(random.randint(360,400)))
        RG_AMP_PCO_2048_CW_HOT.append(str(random.randint(150,200)))
        RG_AMP_NCO_2048_CW_HOT.append(str(random.randint(150,200)))
        RG_DC_PCO_2048_CW_HOT.append(str(random.randint(1010,1050)))
        RG_DC_NCO_2048_CW_HOT.append(str(random.randint(1010,1050)))
        RG_DARK_PCO_2048_CW_HOT.append(str(random.randint(750,800)))
        RG_DARK_NCO_2048_CW_HOT.append(str(random.randint(750,800)))
        RG_CONTRAST_PCO_2048_CW_HOT.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_NCO_2048_CW_HOT.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_AMP_PC_1024_CW_HOT.append(str(random.randint(150,180)))
        RG_AMP_NC_1024_CW_HOT.append(str(random.randint(150,180)))
        RG_DC_PC_1024_CW_HOT.append(str(random.randint(750,800)))
        RG_DC_NC_1024_CW_HOT.append(str(random.randint(750,800)))
        RG_DARK_PC_1024_CW_HOT.append(str(random.randint(520,570)))
        RG_DARK_NC_1024_CW_HOT.append(str(random.randint(520,570)))
        RG_CONTRAST_PC_1024_CW_HOT.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_NC_1024_CW_HOT.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_PC_PCO_CW_HOT.append("1."+''.join(random.choices(string.digits, k=3)))

        GFS_CORR_DEZ_KPP_COLD.append("0"+''.join(random.choices(string.digits, k=2)))
        GFC_CORR_DEZ_KPP_COLD.append("0"+''.join(random.choices(string.digits, k=2)))
        RG_AMPS_CW_KPP_COLD.append(str(random.randint(360,400)))
        RG_AMPC_CW_KPP_COLD.append(str(random.randint(360,400)))
        RG_AMP_PCO_2048_CW_KPP_COLD.append(str(random.randint(150,200)))
        RG_AMP_NCO_2048_CW_KPP_COLD.append(str(random.randint(150,200)))
        RG_DC_PCO_2048_CW_KPP_COLD.append(str(random.randint(1010,1050)))
        RG_DC_NCO_2048_CW_KPP_COLD.append(str(random.randint(1010,1050)))
        RG_DARK_PCO_2048_CW_KPP_COLD.append(str(random.randint(750,800)))
        RG_DARK_NCO_2048_CW_KPP_COLD.append(str(random.randint(750,800)))
        RG_CONTRAST_PCO_2048_CW_KPP_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_NCO_2048_CW_KPP_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_AMP_PC_1024_CW_KPP_COLD.append(str(random.randint(150,180)))
        RG_AMP_NC_1024_CW_KPP_COLD.append(str(random.randint(150,180)))
        RG_DC_PC_1024_CW_KPP_COLD.append(str(random.randint(750,800)))
        RG_DC_NC_1024_CW_KPP_COLD.append(str(random.randint(750,800)))
        RG_DARK_PC_1024_CW_KPP_COLD.append(str(random.randint(520,570)))
        RG_DARK_NC_1024_CW_KPP_COLD.append(str(random.randint(520,570)))
        RG_CONTRAST_PC_1024_CW_KPP_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_NC_1024_CW_KPP_COLD.append("0."+''.join(random.choices(string.digits, k=3)))
        RG_CONTRAST_PC_PCO_CW_KPP_COLD.append("1."+''.join(random.choices(string.digits, k=3)))

        EXT_ONESTEP_ST_CCW_COLD.append("-"+str(random.randint(1,4)))
        EXT_ONESTEP_ST_CW_COLD.append(str(random.randint(0,1)))
        RG_STATUS_SC_CCW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        RG_STATUS_CC_CCW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        MR_STATUS_CCW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        RG_STATUS_SC_CW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        RG_STATUS_CC_CW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        MR_STATUS_CW_COLD.append(''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2))+" "+''.join(random.choices(string.digits, k=2)))
        POLLUTION_2048_HIGH_MAX_COLD.append(str(random.randint(1,4)))
        POLLUTION_2048_HIGH_MIN_COLD.append("-"+str(random.randint(1,4)))
        POLLUTION_2048_LOW_MAX_COLD.append(str(random.randint(1,4)))
        POLLUTION_2048_LOW_MIN_COLD.append("-"+str(random.randint(1,3)))
        POLLUTION_1024_HIGH_MAX_COLD.append(str(random.randint(1,2)))
        POLLUTION_1024_HIGH_MIN_COLD.append("-"+str(random.randint(1,2)))
        POLLUTION_1024_LOW_MAX_COLD.append(str(random.randint(1,2)))
        POLLUTION_1024_LOW_MIN_COLD.append("-"+str(random.randint(1,2)))
        param_list.append(''.join(date_time+station_id+cell_id+product_id+barcode_id+DISC_CONCENTRIC+DISC_RUNOUT+AIR_GAP+LATHE_AIR_GAP_NOM+LATHE_AIR_GAP_TOL+LATHE_VAL_NOM+
                                  LATHE_VAL_ACT+LATHE_ERROR+LATHE_AMOUNT_LIFT+LATHE_ASIC_HEIGHT+LATHE_DISC_THICK+LATHE_AXIAL_PLAY+LATHE_MATERIAL_THICK+FORCE_STROKE_CONTROL_DISK_FLANGE+
                                  FORCE_STROKE_CONTROL_CROSSBAR+CURRENT_DRAIN_BISS_COLD_ST+CURRENT_DRAIN_BISS_COLD_MT+CURRENT_DRAIN_BISS_KPP_COLD_ST+CURRENT_DRAIN_BISS_KPP_COLD_MT+
                                  CURRENT_DRAIN_DQ_COLD_ST+CURRENT_DRAIN_DQ_COLD_MT+CURRENT_DRAIN_BISS_HOT_ST+CURRENT_DRAIN_BISS_HOT_MT+ALIGNMENT_DJH_DJL_DIFF+ALIGNMENT_PHASE_DIFF+
                                  ALIGN_OPT_GEAR_ST+ALIGN_OPT_GEAR_MT+MV1_OFF_VER+MV2_OFF_VER+MV3_OFF_VER+CFG_BIAS+MR_PT1000_R1270+MR_PT1000_R1385+MR_PT1000_R1470+GFS_CORR_DEZ_COLD+
                                  GFC_CORR_DEZ_COLD+OFS_CORR_DEZ_COLD+OFC_CORR_DEZ_COLD+RG_AMPS_CW_COLD+RG_AMPC_CW_COLD+RG_AMP_PCO_2048_CW_COLD+RG_DC_PCO_2048_CW_COLD+
                                  RG_DARK_PCO_2048_CW_COLD+RG_CONTRAST_PCO_2048_CW_COLD+RG_AMP_PC_1024_CW_COLD+RG_AMP_NC_1024_CW_COLD+RG_DC_PC_1024_CW_COLD+RG_DC_NC_1024_CW_COLD+
                                  RG_DARK_PC_1024_CW_COLD+RG_DARK_NC_1024_CW_COLD+RG_CONTRAST_PC_1024_CW_COLD+RG_CONTRAST_NC_1024_CW_COLD+RG_CONTRAST_PC_PCO_CW_COLD+GFS_CORR_DEZ_HOT+
                                  GFC_CORR_DEZ_HOT+RG_AMPS_CW_HOT+RG_AMPC_CW_HOT+RG_AMP_PCO_2048_CW_HOT+RG_AMP_NCO_2048_CW_HOT+RG_DC_PCO_2048_CW_HOT+RG_DC_NCO_2048_CW_HOT+
                                  RG_DARK_PCO_2048_CW_HOT+RG_DARK_NCO_2048_CW_HOT+RG_CONTRAST_PCO_2048_CW_HOT+RG_CONTRAST_NCO_2048_CW_HOT+RG_AMP_PC_1024_CW_HOT+RG_AMP_NC_1024_CW_HOT+
                                  RG_DC_PC_1024_CW_HOT +RG_DC_NC_1024_CW_HOT +RG_DARK_PC_1024_CW_HOT +RG_DARK_NC_1024_CW_HOT +RG_CONTRAST_PC_1024_CW_HOT +RG_CONTRAST_NC_1024_CW_HOT +
                                  RG_CONTRAST_PC_PCO_CW_HOT +GFS_CORR_DEZ_KPP_COLD +GFC_CORR_DEZ_KPP_COLD +RG_AMPS_CW_KPP_COLD +RG_AMPC_CW_KPP_COLD +RG_AMP_PCO_2048_CW_KPP_COLD +
                                  RG_AMP_NCO_2048_CW_KPP_COLD +RG_DC_PCO_2048_CW_KPP_COLD +RG_DC_NCO_2048_CW_KPP_COLD +RG_DARK_PCO_2048_CW_KPP_COLD +RG_DARK_NCO_2048_CW_KPP_COLD +
                                  RG_CONTRAST_PCO_2048_CW_KPP_COLD +RG_CONTRAST_NCO_2048_CW_KPP_COLD +RG_AMP_PC_1024_CW_KPP_COLD +RG_AMP_NC_1024_CW_KPP_COLD +RG_DC_PC_1024_CW_KPP_COLD+
                                  RG_DC_NC_1024_CW_KPP_COLD +RG_DARK_PC_1024_CW_KPP_COLD +RG_DARK_NC_1024_CW_KPP_COLD +RG_CONTRAST_PC_1024_CW_KPP_COLD +RG_CONTRAST_NC_1024_CW_KPP_COLD+
                                  RG_CONTRAST_PC_PCO_CW_KPP_COLD +EXT_ONESTEP_ST_CCW_COLD+EXT_ONESTEP_ST_CW_COLD+RG_STATUS_SC_CCW_COLD+RG_STATUS_CC_CCW_COLD +MR_STATUS_CCW_COLD +
                                  RG_STATUS_SC_CW_COLD +RG_STATUS_CC_CW_COLD +MR_STATUS_CW_COLD +POLLUTION_2048_HIGH_MAX_COLD +POLLUTION_2048_HIGH_MIN_COLD +POLLUTION_2048_LOW_MAX_COLD+
                                  POLLUTION_2048_LOW_MIN_COLD +POLLUTION_1024_HIGH_MAX_COLD +POLLUTION_1024_HIGH_MIN_COLD +POLLUTION_1024_LOW_MAX_COLD +POLLUTION_1024_LOW_MIN_COLD))
        sql = "INSERT INTO CATEGORY_1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cnt=0
        for param in param_list:
            values =(date_time[cnt],cell_id[cnt],station_id[cnt],product_id[cnt],barcode_id[cnt],DISC_CONCENTRIC[cnt],DISC_RUNOUT[cnt],AIR_GAP[cnt],LATHE_AIR_GAP_NOM[cnt],LATHE_AIR_GAP_TOL[cnt],LATHE_VAL_NOM[cnt],LATHE_VAL_ACT[cnt],LATHE_ERROR[cnt],LATHE_AMOUNT_LIFT[cnt],LATHE_ASIC_HEIGHT[cnt],LATHE_DISC_THICK[cnt],LATHE_AXIAL_PLAY[cnt],LATHE_MATERIAL_THICK[cnt],FORCE_STROKE_CONTROL_DISK_FLANGE[cnt],FORCE_STROKE_CONTROL_CROSSBAR[cnt],CURRENT_DRAIN_BISS_COLD_ST[cnt],CURRENT_DRAIN_BISS_COLD_MT [cnt],CURRENT_DRAIN_BISS_KPP_COLD_ST [cnt],CURRENT_DRAIN_BISS_KPP_COLD_MT [cnt],CURRENT_DRAIN_DQ_COLD_ST [cnt],CURRENT_DRAIN_DQ_COLD_MT [cnt],CURRENT_DRAIN_BISS_HOT_ST [cnt],CURRENT_DRAIN_BISS_HOT_MT [cnt],ALIGNMENT_DJH_DJL_DIFF [cnt],ALIGNMENT_PHASE_DIFF [cnt],ALIGN_OPT_GEAR_ST [cnt],ALIGN_OPT_GEAR_MT [cnt],MV1_OFF_VER [cnt],MV2_OFF_VER [cnt],MV3_OFF_VER [cnt],CFG_BIAS [cnt],MR_PT1000_R1270 [cnt],MR_PT1000_R1385 [cnt],MR_PT1000_R1470[cnt], GFS_CORR_DEZ_COLD [cnt],GFC_CORR_DEZ_COLD [cnt],OFS_CORR_DEZ_COLD [cnt],OFC_CORR_DEZ_COLD [cnt],RG_AMPS_CW_COLD[cnt],RG_AMPC_CW_COLD [cnt],RG_AMP_PCO_2048_CW_COLD [cnt],RG_DC_PCO_2048_CW_COLD [cnt],RG_DARK_PCO_2048_CW_COLD [cnt],RG_CONTRAST_PCO_2048_CW_COLD [cnt],RG_AMP_PC_1024_CW_COLD [cnt],RG_AMP_NC_1024_CW_COLD [cnt],RG_DC_PC_1024_CW_COLD [cnt],RG_DC_NC_1024_CW_COLD [cnt],RG_DARK_PC_1024_CW_COLD [cnt],RG_DARK_NC_1024_CW_COLD [cnt],RG_CONTRAST_PC_1024_CW_COLD [cnt],RG_CONTRAST_NC_1024_CW_COLD [cnt],RG_CONTRAST_PC_PCO_CW_COLD [cnt],GFS_CORR_DEZ_HOT [cnt],GFC_CORR_DEZ_HOT [cnt],RG_AMPS_CW_HOT [cnt],RG_AMPC_CW_HOT [cnt],RG_AMP_PCO_2048_CW_HOT [cnt],RG_AMP_NCO_2048_CW_HOT [cnt],RG_DC_PCO_2048_CW_HOT [cnt],RG_DC_NCO_2048_CW_HOT [cnt],RG_DARK_PCO_2048_CW_HOT [cnt],RG_DARK_NCO_2048_CW_HOT [cnt],RG_CONTRAST_PCO_2048_CW_HOT [cnt],RG_CONTRAST_NCO_2048_CW_HOT [cnt],RG_AMP_PC_1024_CW_HOT [cnt],RG_AMP_NC_1024_CW_HOT [cnt],RG_DC_PC_1024_CW_HOT [cnt],RG_DC_NC_1024_CW_HOT [cnt],RG_DARK_PC_1024_CW_HOT [cnt],RG_DARK_NC_1024_CW_HOT [cnt],RG_CONTRAST_PC_1024_CW_HOT [cnt],RG_CONTRAST_NC_1024_CW_HOT [cnt],RG_CONTRAST_PC_PCO_CW_HOT [cnt],GFS_CORR_DEZ_KPP_COLD [cnt],GFC_CORR_DEZ_KPP_COLD[cnt],RG_AMPS_CW_KPP_COLD [cnt],RG_AMPC_CW_KPP_COLD [cnt],RG_AMP_PCO_2048_CW_KPP_COLD [cnt],RG_AMP_NCO_2048_CW_KPP_COLD [cnt],RG_DC_PCO_2048_CW_KPP_COLD [cnt],RG_DC_NCO_2048_CW_KPP_COLD[cnt],RG_DARK_PCO_2048_CW_KPP_COLD [cnt],RG_DARK_NCO_2048_CW_KPP_COLD [cnt],RG_CONTRAST_PCO_2048_CW_KPP_COLD [cnt],RG_CONTRAST_NCO_2048_CW_KPP_COLD [cnt],RG_AMP_PC_1024_CW_KPP_COLD [cnt],RG_AMP_NC_1024_CW_KPP_COLD [cnt],RG_DC_PC_1024_CW_KPP_COLD [cnt],RG_DC_NC_1024_CW_KPP_COLD [cnt],RG_DARK_PC_1024_CW_KPP_COLD [cnt],RG_DARK_NC_1024_CW_KPP_COLD [cnt],RG_CONTRAST_PC_1024_CW_KPP_COLD [cnt],RG_CONTRAST_NC_1024_CW_KPP_COLD [cnt],RG_CONTRAST_PC_PCO_CW_KPP_COLD [cnt],EXT_ONESTEP_ST_CCW_COLD[cnt],EXT_ONESTEP_ST_CW_COLD[cnt],RG_STATUS_SC_CCW_COLD [cnt],RG_STATUS_CC_CCW_COLD [cnt],MR_STATUS_CCW_COLD [cnt],RG_STATUS_SC_CW_COLD [cnt],RG_STATUS_CC_CW_COLD [cnt],MR_STATUS_CW_COLD [cnt],POLLUTION_2048_HIGH_MAX_COLD [cnt],POLLUTION_2048_HIGH_MIN_COLD [cnt],POLLUTION_2048_LOW_MAX_COLD [cnt],POLLUTION_2048_LOW_MIN_COLD [cnt],POLLUTION_1024_HIGH_MAX_COLD [cnt],POLLUTION_1024_HIGH_MIN_COLD [cnt],POLLUTION_1024_LOW_MAX_COLD [cnt],POLLUTION_1024_LOW_MIN_COLD[cnt]) 
            cursor.execute(sql, values)
            cnt+=1
    conn.commit()
    del date_time[:],cell_id[:],station_id[:],product_id[:],barcode_id[:],DISC_CONCENTRIC[:],DISC_RUNOUT[:],AIR_GAP[:],LATHE_AIR_GAP_NOM[:],LATHE_AIR_GAP_TOL[:],LATHE_VAL_NOM[:],LATHE_VAL_ACT[:],LATHE_ERROR[:],LATHE_AMOUNT_LIFT[:],LATHE_ASIC_HEIGHT[:],LATHE_DISC_THICK[:],LATHE_AXIAL_PLAY[:],LATHE_MATERIAL_THICK[:],FORCE_STROKE_CONTROL_DISK_FLANGE[:],FORCE_STROKE_CONTROL_CROSSBAR[:],CURRENT_DRAIN_BISS_COLD_ST[:],CURRENT_DRAIN_BISS_COLD_MT [:],CURRENT_DRAIN_BISS_KPP_COLD_ST [:],CURRENT_DRAIN_BISS_KPP_COLD_MT [:],CURRENT_DRAIN_DQ_COLD_ST [:],CURRENT_DRAIN_DQ_COLD_MT [:],CURRENT_DRAIN_BISS_HOT_ST [:],CURRENT_DRAIN_BISS_HOT_MT [:],ALIGNMENT_DJH_DJL_DIFF [:],ALIGNMENT_PHASE_DIFF [:],ALIGN_OPT_GEAR_ST [:],ALIGN_OPT_GEAR_MT [:],MV1_OFF_VER [:],MV2_OFF_VER [:],MV3_OFF_VER [:],CFG_BIAS [:],MR_PT1000_R1270 [:],MR_PT1000_R1385 [:],MR_PT1000_R1470[:], GFS_CORR_DEZ_COLD [:],GFC_CORR_DEZ_COLD [:],OFS_CORR_DEZ_COLD [:],OFC_CORR_DEZ_COLD [:],RG_AMPS_CW_COLD[:],RG_AMPC_CW_COLD [:],RG_AMP_PCO_2048_CW_COLD [:],RG_DC_PCO_2048_CW_COLD [:],RG_DARK_PCO_2048_CW_COLD [:],RG_CONTRAST_PCO_2048_CW_COLD [:],RG_AMP_PC_1024_CW_COLD [:],RG_AMP_NC_1024_CW_COLD [:],RG_DC_PC_1024_CW_COLD [:],RG_DC_NC_1024_CW_COLD [:],RG_DARK_PC_1024_CW_COLD [:],RG_DARK_NC_1024_CW_COLD [:],RG_CONTRAST_PC_1024_CW_COLD [:],RG_CONTRAST_NC_1024_CW_COLD [:],RG_CONTRAST_PC_PCO_CW_COLD [:],GFS_CORR_DEZ_HOT [:],GFC_CORR_DEZ_HOT [:],RG_AMPS_CW_HOT [:],RG_AMPC_CW_HOT [:],RG_AMP_PCO_2048_CW_HOT [:],RG_AMP_NCO_2048_CW_HOT [:],RG_DC_PCO_2048_CW_HOT [:],RG_DC_NCO_2048_CW_HOT [:],RG_DARK_PCO_2048_CW_HOT [:],RG_DARK_NCO_2048_CW_HOT [:],RG_CONTRAST_PCO_2048_CW_HOT [:],RG_CONTRAST_NCO_2048_CW_HOT [:],RG_AMP_PC_1024_CW_HOT [:],RG_AMP_NC_1024_CW_HOT [:],RG_DC_PC_1024_CW_HOT [:],RG_DC_NC_1024_CW_HOT [:],RG_DARK_PC_1024_CW_HOT [:],RG_DARK_NC_1024_CW_HOT [:],RG_CONTRAST_PC_1024_CW_HOT [:],RG_CONTRAST_NC_1024_CW_HOT [:],RG_CONTRAST_PC_PCO_CW_HOT [:],GFS_CORR_DEZ_KPP_COLD [:],GFC_CORR_DEZ_KPP_COLD[:],RG_AMPS_CW_KPP_COLD [:],RG_AMPC_CW_KPP_COLD [:],RG_AMP_PCO_2048_CW_KPP_COLD [:],RG_AMP_NCO_2048_CW_KPP_COLD [:],RG_DC_PCO_2048_CW_KPP_COLD [:],RG_DC_NCO_2048_CW_KPP_COLD[:],RG_DARK_PCO_2048_CW_KPP_COLD [:],RG_DARK_NCO_2048_CW_KPP_COLD [:],RG_CONTRAST_PCO_2048_CW_KPP_COLD [:],RG_CONTRAST_NCO_2048_CW_KPP_COLD [:],RG_AMP_PC_1024_CW_KPP_COLD [:],RG_AMP_NC_1024_CW_KPP_COLD [:],RG_DC_PC_1024_CW_KPP_COLD [:],RG_DC_NC_1024_CW_KPP_COLD [:],RG_DARK_PC_1024_CW_KPP_COLD [:],RG_DARK_NC_1024_CW_KPP_COLD [:],RG_CONTRAST_PC_1024_CW_KPP_COLD [:],RG_CONTRAST_NC_1024_CW_KPP_COLD [:],RG_CONTRAST_PC_PCO_CW_KPP_COLD [:],EXT_ONESTEP_ST_CCW_COLD[:],EXT_ONESTEP_ST_CW_COLD[:],RG_STATUS_SC_CCW_COLD [:],RG_STATUS_CC_CCW_COLD [:],MR_STATUS_CCW_COLD [:],RG_STATUS_SC_CW_COLD [:],RG_STATUS_CC_CW_COLD [:],MR_STATUS_CW_COLD [:],POLLUTION_2048_HIGH_MAX_COLD [:],POLLUTION_2048_HIGH_MIN_COLD [:],POLLUTION_2048_LOW_MAX_COLD [:],POLLUTION_2048_LOW_MIN_COLD [:],POLLUTION_1024_HIGH_MAX_COLD [:],POLLUTION_1024_HIGH_MIN_COLD [:],POLLUTION_1024_LOW_MAX_COLD [:],POLLUTION_1024_LOW_MIN_COLD[:],param_list[:]
        #print(len(param_list))
    


conn.close()
