/***********************************************************************************************************************
 *  $Header: svn://aldapp07.icgeu.com/HengProcDB/DB-abstraction-Layer/DBAL/inc/dbal.h 465 2023-03-29 15:30:28Z fabian.brandauer $
 *  $Company: (c) Hengstler GmbH 2023 $
 **********************************************************************************************************************/
#pragma once
//! \file dll.h
#ifndef _DLL_H_
#define _DLL_H_

// Check windows
#if _WIN32 || _WIN64
#if _WIN64
typedef unsigned long long ADDR_t;
#else
typedef unsigned int ADDR_t;
#endif
#endif

//! DLL path define
#ifndef DLL_PATH
#define DLL_PATH "dal.dll"
#endif


#define MAKE_PRIVATE_FUNC_PUBLIC   1

//! This is an dll example function
extern int dll_init( void ); //!< \return success of operation.

typedef struct db_gobal_struct {
//!<\ stores all the global structure variables.
    char barcode[20]; /*stores BARCODE_ID from the database*/
    char attr_id[20]; /*stores ATTRIBUTE_ID from the database*/
    char station_no[20]; /*stores STATION_ID from the database*/
    char attr_value[20]; /*stores ATTRIBUTE_VALUE*/
    char attr_station_no[20]; /* stores ATTRIBUTE_LOOKUP_STTAION_NUMBER*/
    char substation_id[20]; /* stores SUBSTATION_ID*/
    int cell_no; /* stores CELL_ID*/
    int year; /* stores last two digits of the year */
    char filename[100]; /* stores the filename*/
    char table_no[20]; /* stores the category table number */
    char upid[100]; /* stores the generated upid*/
    char store_upid[100]; /* stores the upid present in database*/
    char active_state[20]; /* stores count of active states of the ATTRIBUTES*/
    char category[20]; /*stores category of the ATTIBUTE_VALUE belongs to */
    char datatype[20]; /* stores datatype of which ATTRIBUTE_VALUE belongs to*/
    char attr_value_bigint[20]; /* stores the ATTRIBUTE_VALUE of datatype bigint*/
    char attr_value_double[20]; /* stores the ATTRIBUTE_VALUE of datatype double*/
    char attr_value_varbinary[20]; /* stores the ATTRIBUTE_VALUE of datatype varbinary*/
    char date_time[50]; /* stores the datetime in epoch format*/
    char last_idx[20];
    char min_value_range[20];
    char max_value_range[20];
}db_attr_t;

typedef struct db_conf_type {
    char db_name[100];// ref to db_init
    char psswd[20];// ref to db_init
    char server[50]; // ref to db_init
    char user[50]; // ref to db_init
} db_conf_t;

extern int db_init(db_conf_t* pdb_conf); //This function will help us to connect with database.

extern int update_attribute(db_attr_t* pdb_attr); //This is top level function which calls all the below functions.

extern int db_close(); // This function helps in closing the connection with database.

//! This is the function pointer compatible to \ref dll_init.
//typedef int( *tDll_init ) ( void );  //!< \return success of operation.

//!< This is the function pointer compatible to \ref dll_test.
typedef int(*tDll_db_init) (db_conf_t* pdb_conf); //!< \return success of operation.

typedef int(*tDll_update_attr) (db_attr_t* pdb_attr); //!< \return success of operation.

typedef int(*tDll_br_init) (db_attr_t* pdb_attr); //!< \return success of operation.

typedef int(*tDll_db_close) ();


//! Dll function pointer struct
typedef struct dll_struct_type {
    //tDll_init pDll_init;    //!< \ref dll_init.

#ifdef  MAKE_PRIVATE_FUNC_PUBLIC
    tDll_db_init pDll_db_init; //!< \ref dll_init.
    tDll_br_init pDll_br_init; //!< \ref dll_init.
    tDll_update_attr pDll_update_attr; //!< \ref dll_init.
    tDll_db_close pDll_db_close; //!< \ref dll_init.
#endif
} dll_t;

//! DLL struct initializer function.
extern int struct_init(
    dll_t* struct_p, //!< [in][out] This the strct pointer. 
    size_t structSize_p  //!< [in] This the struct size. 
); //!< \return success of operation.

//! DLL struct initializer function pointer type.
typedef int( *struct_init_t ) ( dll_t* struct_p, size_t structSize_p );

#if defined DLL_INIT
#undef DLL_INIT
//! Dll loader and initializer for WINAPI
static HINSTANCE _instance_gs = 0;
static dll_t _dllInstance_gs;

HINSTANCE dll_load( dll_t* struct_p, char* dllpath_p ) {

    _instance_gs = LoadLibrary( dllpath_p );
    if( 0 != _instance_gs ) {
        struct_init_t struct_init_p = (struct_init_t) GetProcAddress( _instance_gs, "struct_init" );

        if( struct_init_p ) {
            if( 0 != struct_init_p( struct_p, sizeof( dll_t ) ) ) {
                _instance_gs = 0;
            }
        }
        else {
            _instance_gs = 0;
        }
    }

    return  _instance_gs;
}



/* ADD ALL PRIVATE FUCNTIONS BELOW*/

#ifdef  MAKE_PRIVATE_FUNC_PUBLIC

#endif //  MAKE_PRIVATE_FUNC_PUBLIC

//int dll_init( void ) {
//    if( 0 == _instance_gs ) {
//        _instance_gs = dll_load( &_dllInstance_gs, DLL_PATH );
//    }
//
//    if( _dllInstance_gs.pDll_init ) {
//        return _dllInstance_gs.pDll_init();
//    }
//    else {
//        return -1;
//    }
//}

int db_init(db_conf_t* pdb_conf) {
    if (0 == _instance_gs) {
        _instance_gs = dll_load(&_dllInstance_gs, DLL_PATH);
    }

    if (_dllInstance_gs.pDll_db_init) {
        return _dllInstance_gs.pDll_db_init(pdb_conf);
    }
    else {
      
        return -1;
    }
}

int barcode_exists(db_attr_t* pdb_attr) {
    if (0 == _instance_gs) {
        _instance_gs = dll_load(&_dllInstance_gs, DLL_PATH);
    }

    if (_dllInstance_gs.pDll_br_init) {
        return _dllInstance_gs.pDll_br_init(pdb_attr);
    }
    else {

        return -1;
    }
}

int update_attribute(db_attr_t* pdb_attr) {
    if (0 == _instance_gs) {
        _instance_gs = dll_load(&_dllInstance_gs, DLL_PATH);
    }

    if (_dllInstance_gs.pDll_update_attr) {
        return _dllInstance_gs.pDll_update_attr(pdb_attr);
    }
    else {

        return -1;
    }
}
int db_close() {
    if (0 == _instance_gs) {
        _instance_gs = dll_load(&_dllInstance_gs, DLL_PATH);
    }

    if (_dllInstance_gs.pDll_db_close) {
        return _dllInstance_gs.pDll_db_close();
    }
    else {

        return -1;
    }
}

#endif
#endif _DLL_H_
