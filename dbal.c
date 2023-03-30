/***********************************************************************************************************************
 *  $Header: svn://aldapp07.icgeu.com/HengProcDB/DB-abstraction-Layer/DBAL/src/dbal.c 465 2023-03-29 15:30:28Z fabian.brandauer $
 *  $Company: (c) Hengstler GmbH 2023 $
 **********************************************************************************************************************/
#define _CRT_SECURE_NO_WARNINGS (0)
#include <Windows.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <dbal_Syslog.h>
#include <dbal.h>
#include <error.h>
#include <math.h>


#pragma comment(lib, "libmysql.lib") 
#pragma comment(lib, "mysqlservices.lib") 
#pragma comment(lib, "mysqlclient.lib") 

#include <mysql.h>

#define SVCNAME TEXT("dal")

MYSQL* pmySQL = 0;
MYSQL_RES* res;
MYSQL_ROW row;
MYSQL_FIELD* field;
int status = 0;


typedef char CHAR;
typedef unsigned char byte;
typedef _Null_terminated_ CHAR* NPSTR, * LPSTR, * PSTR;
typedef LPSTR PTSTR, LPTSTR, PUTSTR, LPUTSTR;
typedef unsigned long DWORD;


void SvcReportEvent ( LPTSTR szMessage_p, byte logType_p );

void log_message ( int level_p, char* message_p )
{
#ifndef DEBUG
    SvcReportEvent ( &message_p [ 0 ], ( byte ) level_p );
#else

    printf ( "%s", message_p );
#endif
}

void SvcReportEvent ( LPTSTR szMessage_p, byte logType_p )
{
    HANDLE hEventSource;
    LPCTSTR lpszStrings [ 2 ];
    //TCHAR Buffer[80];
    DWORD status_l = 0;

    hEventSource = RegisterEventSource ( NULL, SVCNAME );

    if ( NULL != hEventSource )
    {

        switch ( logType_p )
        {
            default:
            case EVENTLOG_ERROR_TYPE:
            {
                //StringCchPrintf(Buffer, 80, TEXT("Error: %s failed with %d!"), szMessage_p, GetLastError());
                status_l = SVC_ERROR;
            }break;
            case EVENTLOG_WARNING_TYPE:
            {
                //StringCchPrintf ( Buffer, 80, TEXT ( "Warning: %s!" ), szMessage_p );
                status_l = SVC_WARNING;
            }break;
            case EVENTLOG_SUCCESS:
            {
                //StringCchPrintf ( Buffer, 80, TEXT ( "Success: %s." ), szMessage_p );
                status_l = SVC_SUCCESS;
            }break;
            case EVENTLOG_INFORMATION_TYPE:
            {
                //StringCchPrintf ( Buffer, 80, TEXT ( "Info: %s." ), szMessage_p );
                status_l = SVC_INFO;
            }break;
        }

        lpszStrings [ 0 ] = SVCNAME;
        lpszStrings [ 1 ] = szMessage_p;

        ReportEvent ( hEventSource,        // event log handle
            logType_p, //EVENTLOG_ERROR_TYPE, // event type
            0,                   // event category
            status_l, //SVC_ERROR, // event identifier
            NULL,                // no security identifier
            2,                   // size of lpszStrings array
            0,                   // no binary data
            lpszStrings,         // array of strings
            NULL );               // no binary data

        DeregisterEventSource ( hEventSource );
    }
}
/****function to connect with database(struct pointer )
pdbconf : pointer to database configurations****/

int db_init ( db_conf_t* pdb_conf )
{
    //!<\initialize connection with database.
    pmySQL = mysql_init ( NULL );
    mysql_real_connect ( pmySQL, pdb_conf->server, pdb_conf->user, pdb_conf->psswd, pdb_conf->db_name, 0, NULL, 0 );

    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    else
    {
        printf ( "Connection is sucessfull with database: '%s' \n", pdb_conf->db_name );
    }
    log_message ( EVENTLOG_SUCCESS, "Ready for operation." );
    return SUCCESS;
    //!<\returns success.
}

int DBAL_announce_product ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql [ 100 ] = "call ANNOUNCE(";
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, ",'" );
    strcat ( sql, pdb_attr->barcode );
    strcat ( sql, "')" );
    printf ( " %s\n", sql );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "%s \n", row [ 0 ] );
        if ( sscanf ( row [ 0 ], "%s", pdb_attr->store_upid ) != 1 ) // UPID is not a string, it is an byte array(20) not character
        {
            printf ( "\n" );
        };
    }
    printf ( "Stored UPID is %s\n", pdb_attr->store_upid );
    mysql_free_result ( res );
    return 0;


}

int DBAL_double_submit ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql [ 100 ] = "call SUBMIT_DOUBLE ('";
    strcat ( sql, pdb_attr->store_upid );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->attr_id );
    strcat ( sql, "," );
    //strcat ( sql, round ( ( rand () * 200.0 ) + 1000.0 ) ); //FB: this won't work.... //KK: generating fake values is up to dalTest.c
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "%s \n", row [ 0 ] );
        if ( sscanf ( row [ 0 ], "%s", pdb_attr->last_idx ) != 1 )
        {
            printf ( "\n" );
        };
    }
    printf ( "Last index is %s\n", pdb_attr->last_idx );
    mysql_free_result ( res );
    return 0;
}

int DBAL_check_limits ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql [ 100 ] = "call GET_LAST_DOUBLE_ATTR ('";
    strcat ( sql, pdb_attr->store_upid );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->attr_id );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->last_idx );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }

    do
    {
        res = mysql_store_result ( pmySQL );
        if ( res == NULL )
        {
            return -1;
        }
        int num_fields = mysql_num_fields ( res );
        while ( ( row = mysql_fetch_row ( res ) ) != NULL )
        {
            for ( int i = 0; i < num_fields; i++ )
            {
                if ( sscanf ( row [ 0 ], "%s", pdb_attr->attr_value_double ) != 1 )
                {
                    printf ( "\n" );
                };
                if ( sscanf ( row [ 1 ], "%s", pdb_attr->min_value_range ) != 1 )
                {
                    printf ( "\n" );
                };
                if ( sscanf ( row [ 2 ], "%s", pdb_attr->max_value_range ) != 1 )
                {
                    printf ( "\n" );
                };

            }
            printf ( "Double value is: %s\t  ", row [ 0 ] );
            printf ( "minimum range is: %s\t", row [ 1 ] );
            printf ( "maximim range is: %s\n", row [ 2 ] );
            if ( row [ 0 ] < row [ 1 ] && row [ 0 ] > row [ 2 ] )
            {
                printf ( "Value is in range \n" );

            }
            else
            {
                return -1;
            }
        }
        mysql_free_result ( res );
        status = mysql_next_result ( pmySQL );
        if ( status > 0 )
        {
            return -1;
        }

    }
    while ( status == 0 );
    mysql_free_result ( res );
    return 0;

}

int DBAL_double_wrap_up ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql [ 100 ] = "call ANNOUNCE(";
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, ",'" );
    strcat ( sql, pdb_attr->store_upid );
    strcat ( sql, "')" );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    else
    {
        printf ( "wrap up successful\n" );
    }

    return 0;//Don't forget to return.
}

int DBAL_varbinary_submit ( db_attr_t* pdb_attr )
{
    char sql [ 1024 ] = "";
    char tmp_l [ 32 ] = "";

    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }

    strcpy ( sql, "call SUBMIT_VARBINARY('" );
    strcat ( sql, pdb_attr->store_upid );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->attr_id );
    strcat ( sql, "," );
    //strcat ( sql, 0xaa55 ); //FB: this won't work... strcat only accepts strings.
    sprintf ( tmp_l, "%x", 0xaa55 ); //convert to string
    strcat ( sql, tmp_l ); //concatenate strings.
    strcat ( sql, ");" );


    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "%s \n", row [ 0 ] );
        if ( sscanf ( row [ 0 ], "%s", pdb_attr->last_idx ) != 1 )
        {
            printf ( "\n" );
        };
    }
    printf ( "Last index is %s\n", pdb_attr->last_idx );
    mysql_free_result ( res );
    return 0;
}

/***function to check barcode exists(struct pointer )
takes value  pdb_attr->barcode = barcode_id****/

int barcode_exists ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }

    char sql_statement [ 100 ] = "select check_if_barcode_exists('";
    strcat ( sql_statement, pdb_attr->barcode );
    strcat ( sql_statement, "')" );
    printf ( "Check if barcode exists :" );

    if ( mysql_query ( pmySQL, sql_statement ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "YES\n" );
        printf ( "%s \n", row [ 0 ] );
    }
    mysql_free_result ( res );
    return 0;
}

/****function to generate the upid (struct pointer ) ****/

int generate_upid ( db_attr_t* pdb_attr )
{
    char sql [ 100 ] = "select generate_upid('";
    time_t datetime;
    datetime = time ( NULL );
    sprintf ( pdb_attr->date_time, "%lld", datetime );
    /*int length = snprintf ( NULL, 0, "%d", pdb_attr->cell_no );
    int year_len = snprintf ( NULL, 0, "%d", pdb_attr->year );
    char* cell = malloc ( length + 1 );
    char* year = malloc ( year_len + 1 );*/

    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return -1;
    }

    /*if ( cell == 0 || year == 0 )
    {
        return ER_KEY_DOES_NOT_EXITS;
    }*/
    /*_itoa ( pdb_attr->cell_no, cell, 10 );
    _itoa ( pdb_attr->year, year, 10 );*/
    //sprintf(cell,length+1, "%d", pdb_attr->cell_no);
    strcat ( sql, pdb_attr->barcode );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->date_time );
    strcat ( sql, ")" );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    };
    printf ( "\nGenerated UPID is : " );
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "%s\n", row [ 0 ] );
        //sscanf(row[0], "%s", pdb_gen->upid);
        if ( sscanf ( row [ 0 ], "%s", pdb_attr->upid ) != 1 )
        {
            printf ( "\n" );
        }
    }
    mysql_free_result ( res );
    printf ( "\n" );
    /*free ( cell );
    free ( year );*/
    return 0;
}

/****function to fetch the unique product_id w.r.t given barcode(struct pointer )****/
int get_upid ( db_attr_t* pdb_attr )
{
    if ( barcode_exists == 0 )
    {
        printf ( "barcode not present and enter new barcode\n" );
        return db_close ();
    }
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql_statement [ 100 ] = "select read_upid_if_barcode_exists('";
    strcat ( sql_statement, pdb_attr->barcode );
    strcat ( sql_statement, "')" );
    printf ( "UPID corresponding to its barcode is: " );
    if ( mysql_query ( pmySQL, sql_statement ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    };
    res = mysql_store_result ( pmySQL );
    while ( ( row = mysql_fetch_row ( res ) ) != NULL )
    {
        printf ( "%s \n", row [ 0 ] );
        if ( sscanf ( row [ 0 ], "%s", pdb_attr->store_upid ) != 1 )
        {
            printf ( "\n" );
        };
    }
    printf ( "\n" );
    mysql_free_result ( res );
    return 0;
}
/****function to count number of attribute(struct pointer )****/
int count_attributes ( db_attr_t* pdb_attr )
{
    printf ( "Entering count_attributes" );
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return -1;
    }
    char sql [ 100 ] = "call count_attributes(";
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, ",'" );
    strcat ( sql, pdb_attr->active_state );
    strcat ( sql, "')" );
    printf ( "number of active attributes are:\n" );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    do
    {
        res = mysql_store_result ( pmySQL );
        if ( res == NULL )
        {
            return -1;
        }
        row = mysql_fetch_row ( res );
        printf ( "%s\n", row [ 0 ] );
        mysql_free_result ( res );
        status = mysql_next_result ( pmySQL );
        if ( status > 0 )
        {
            return -1;
        }
    }
    while ( status == 0 );

    return 0;
}

/****function to insert the attribute values (struct pointer ) ****/
int insert_attr_values ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return -1;
    }
    char sql [ 200 ] = "call insert_into_table('";
    strcat ( sql, pdb_attr->table_no );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->station_no );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->substation_id );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->attr_id );
    strcat ( sql, ",'" );
    strcat ( sql, pdb_attr->upid );
    strcat ( sql, "'," );
    strcat ( sql, pdb_attr->attr_value_bigint );
    strcat ( sql, "," );
    strcat ( sql, pdb_attr->attr_value_double );
    strcat ( sql, ",'" );
    strcat ( sql, pdb_attr->attr_value_varbinary );
    strcat ( sql, "','" );
    strcat ( sql, pdb_attr->date_time );
    strcat ( sql, "')" );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    else
    {
        printf ( "values have been inserted into table : attr_value_cat%s\n", pdb_attr->table_no );
    }
    return 0;
}

/****function to get category abd datatype of the attribute(struct pointer )****/
int get_category_and_datatype ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return -1;
    }
    char sql1 [ 100 ] = "call generate_tablename(";
    //strcat(sql1, pdb_attr->station_no);
    //strcat(sql1, ",");
    strcat ( sql1, pdb_attr->attr_id );
    strcat ( sql1, ")" );
    if ( mysql_query ( pmySQL, sql1 ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }

    do
    {
        res = mysql_store_result ( pmySQL );
        if ( res == NULL )
        {
            return -1;
        }
        int num_fields = mysql_num_fields ( res );
        while ( ( row = mysql_fetch_row ( res ) ) != NULL )
        {
            for ( int i = 0; i < num_fields; i++ )
            {
                if ( sscanf ( row [ 0 ], "%s", pdb_attr->category ) != 1 )
                {
                    printf ( "\n" );
                };
                if ( sscanf ( row [ 1 ], "%s", pdb_attr->datatype ) != 1 )
                {
                    printf ( "\n" );
                };

            }
            printf ( "category is: %s\t  ", row [ 0 ] );
            printf ( "datatype is: %s\n", row [ 1 ] );
            printf ( "\n" );
        }
        mysql_free_result ( res );
        status = mysql_next_result ( pmySQL );
        if ( status > 0 )
        {
            return -1;
        }

    }
    while ( status == 0 );
    mysql_free_result ( res );
    return 0;
}

/*****function to check the attribute value is within the given range(struct pointer )******/
int check_value_in_range ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return -1;
    }
    char sql [ 100 ] = "0";
    char sql1 [ 100 ] = { "call check_if_value_is_in_range_bigint(" };
    char sql2 [ 100 ] = { "call check_if_value_is_in_range_double(" };
    char sql3 [ 100 ] = { "call check_if_value_is_in_range_varbinary(" };
    int cmpVal = atol ( pdb_attr->datatype );
    if ( cmpVal <= 2 )
    {
        strcpy ( sql, sql1 );
        //strcat(sql, pdb_attr->station_no);
        //strcat(sql, ",");
        strcat ( sql, pdb_attr->attr_id );
        strcat ( sql, "," );
        strcat ( sql, pdb_attr->attr_value );
        strcat ( sql, ")" );
        printf ( "\ncheck attribute value '%s' is in the range : ", pdb_attr->attr_value );
        if ( mysql_query ( pmySQL, sql ) )
        {
            printf ( "failed %s\n", mysql_error ( pmySQL ) );
            return 0;
        }

        do
        {
            printf ( " YES\n" );
            res = mysql_store_result ( pmySQL );
            if ( res == NULL )
            {
                return -1;
            }
            int num_fields = mysql_num_fields ( res );
            while ( ( row = mysql_fetch_row ( res ) ) != NULL )
            {
                for ( int i = 0; i < num_fields; i++ )
                {
                    if ( i == 0 )
                    {
                        printf ( "\n" );
                    }
                    printf ( " %s,  ", row [ i ] ? row [ i ] : "NULL" );
                }
            }
            mysql_free_result ( res );
            status = mysql_next_result ( pmySQL );
            if ( status > 0 )
            {
                return -1;
            }
            printf ( "\n" );
        }
        while ( status == 0 );
        return 0;
    }
    else if ( cmpVal <= 4 )
    {
        strcpy ( sql, sql2 );
        //strcat(sql, pdb_attr->station_no);
        //strcat(sql, ",");
        strcat ( sql, pdb_attr->attr_id );
        strcat ( sql, "," );
        strcat ( sql, pdb_attr->attr_value );
        strcat ( sql, ")" );
        printf ( "\ncheck attribute value '%s' is in the range : ", pdb_attr->attr_value );
        if ( mysql_query ( pmySQL, sql ) )
        {
            printf ( "failed %s\n", mysql_error ( pmySQL ) );
            return 0;
        }

        do
        {
            printf ( " YES\n" );
            res = mysql_store_result ( pmySQL );
            if ( res == NULL )
            {
                return -1;
            }
            int num_fields = mysql_num_fields ( res );
            while ( ( row = mysql_fetch_row ( res ) ) != NULL )
            {
                for ( int i = 0; i < num_fields; i++ )
                {
                    if ( i == 0 )
                    {
                        printf ( "\n" );
                    }
                    printf ( " %s,   ", row [ i ] ? row [ i ] : "NULL" );
                }
            }
            mysql_free_result ( res );
            status = mysql_next_result ( pmySQL );
            if ( status > 0 )
            {
                return -1;
            }
            printf ( "\n" );
        }
        while ( status == 0 );
        return 0;
    }
    else
    {
        strcpy ( sql, sql3 );
        //strcat(sql, pdb_attr->station_no);
        //strcat(sql, ",");
        strcat ( sql, pdb_attr->attr_id );
        strcat ( sql, ",'" );
        strcat ( sql, pdb_attr->attr_value );
        strcat ( sql, "')" );
        printf ( "\ncheck attribute value '%s' is matching : ", pdb_attr->attr_value );
        if ( mysql_query ( pmySQL, sql ) )
        {
            printf ( "failed %s\n", mysql_error ( pmySQL ) );
            return 0;
        }
        printf ( " YES\n" );
        do
        {
            res = mysql_store_result ( pmySQL );
            if ( res == NULL )
            {
                return -1;
            }
            int num_fields = mysql_num_fields ( res );

            while ( ( row = mysql_fetch_row ( res ) ) != NULL )
            {
                for ( int i = 0; i < num_fields; i++ )
                {
                    if ( i == 0 )
                    {
                        printf ( "\n" );
                    }
                    printf ( " %s,  ", row [ i ] ? row [ i ] : "NULL" );
                }
            }
            mysql_free_result ( res );
            status = mysql_next_result ( pmySQL );
            if ( status > 0 )
            {
                return -1;
            }
            printf ( "\n" );
        }
        while ( status == 0 );
        return 0;
    }
}

/******function to reduce the attribute station's count after the changes have been updated(struct pointer ) *****/
int reduce_mf_attr_cnt ( db_attr_t* pdb_attr )
{
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char sql [ 100 ] = "call reduce_mf_status(";
    //strcat(sql, pdb_attr->attr_station_no);
    strcat ( sql, "'" );
    strcat ( sql, pdb_attr->store_upid );
    strcat ( sql, "')" );
    if ( mysql_query ( pmySQL, sql ) )
    {
        printf ( "failed %s\n", mysql_error ( pmySQL ) );
        return 0;
    }
    else
    {
        printf ( "\nmf_status has been updated for UPID %s: ", pdb_attr->store_upid );
        char sql1 [ 200 ] = { "select mf_status" };
        //strcat(sql1, pdb_attr->attr_station_no);
        strcat ( sql1, " from production_status where product_uid ='" );
        strcat ( sql1, pdb_attr->store_upid );
        strcat ( sql1, "'" );
        if ( mysql_query ( pmySQL, sql1 ) )
        {
            printf ( "failed %s\n", mysql_error ( pmySQL ) );
            return 0;
        }
        res = mysql_store_result ( pmySQL );
        while ( ( row = mysql_fetch_row ( res ) ) != NULL )
        {
            printf ( "%s \n", row [ 0 ] );
        }
        mysql_free_result ( res );
    }
    return 0;
}

int insert_file_into_database ( db_attr_t* pdb_attr )
{

    FILE* fp = fopen ( pdb_attr->filename, "r+" );
    if ( fp == NULL )
    {
/* File not created hence exit */
        printf ( "Unable to create file.\n" );
        exit ( EXIT_FAILURE );
    }
    fseek ( fp, 0, SEEK_END );
    if ( ferror ( fp ) )
    {
        fprintf ( stderr, "fseek() failed\n" );
        int r = fclose ( fp );
        if ( r == EOF )
        {
            fprintf ( stderr, "cannot close file handler\n" );
        }
        return ER_CANT_OPEN_FILE;
    }
    int flen = ftell ( fp );
    if ( flen == -1 )
    {
        perror ( "error occurred" );
        int r = fclose ( fp );
        if ( r == EOF )
        {
            fprintf ( stderr, "cannot close file handler\n" );
        }
        return ER_CANT_OPEN_FILE;
    }
    fseek ( fp, 0, SEEK_SET );
    if ( ferror ( fp ) )
    {
        fprintf ( stderr, "fseek() failed\n" );
        int r = fclose ( fp );
        if ( r == EOF )
        {
            fprintf ( stderr, "cannot close file handler\n" );
        }
        return ER_CANT_OPEN_FILE;
    }
    char* fp_data = ( char* ) malloc ( flen + 1 );
    if ( fp_data == 0 )
    {
        return ER_ERROR_ON_CLOSE;
    }
    size_t data_size = fread ( fp_data, 1, flen, fp );
    if ( ferror ( fp ) )
    {
        printf ( "fread() failed\n" );
        int r = fclose ( fp );
        if ( r == EOF )
        {
            printf ( "cannot close file handler\n" );
        }
        return ER_CANT_OPEN_FILE;
    }
    int r = fclose ( fp );
    if ( r == EOF )
    {
        printf ( "cannot close file handler\n" );
    }
    if ( !pmySQL )
    {
        printf ( "Connection failed\n" );
        return ER_DB_CONNECT_FAILED;
    }
    char* chunk = ( char* ) malloc ( 2 * data_size + 1 );
    mysql_real_escape_string ( pmySQL, chunk, fp_data, ( unsigned long ) data_size );
    free ( fp_data );
    char* st = "INSERT INTO blobdata(id, blobfile) VALUES(4, '%s')";
    size_t st_len = strlen ( st );
    char* query = ( char* ) malloc ( st_len + 2 * data_size + 1 );
    int len = snprintf ( query, st_len + 2 * data_size + 1, st, chunk );
    free ( chunk );
    if ( mysql_real_query ( pmySQL, query, len ) )
    {
        printf ( "value not inserted\n" );
        return ER_DB_QUERY_FAILED;
    }
    free ( query );
    return 0;
}

/*****Top level function which calls all the above functions(struct pointer)****/
int update_attribute ( db_attr_t* up_attr )
{
    log_message ( EVENTLOG_SUCCESS, "Ready for operation." );

    DBAL_announce_product ( up_attr );

    DBAL_double_submit ( up_attr );

    if ( DBAL_check_limits ( up_attr ) == -1 )
    {
        printf ( "process failed to execute\n" );
    }
    else
    {
        DBAL_double_wrap_up ( up_attr );
    }

    /*if (barcode_exists(up_attr->barcode) == 0)
    {*/
    db_attr_t gen_upid;
    /*strncpy(gen_upid.barcode, up_attr->barcode, sizeof(up_attr->barcode) - 1);
    strncpy(gen_upid.cell_no, up_attr->cell_no, sizeof(up_attr->cell_no) - 1);
    strncpy(gen_upid.year, up_attr->year, sizeof(up_attr->year) - 1);*/

    generate_upid ( up_attr );
    //generate_upid(&gen_upid);

    int upid = 0;
    db_attr_t pass_barcode;
    strncpy ( pass_barcode.barcode, up_attr->barcode, sizeof ( up_attr->barcode ) - 1 );
    upid = get_upid ( &pass_barcode );

    if ( atol ( gen_upid.upid ) == atol ( pass_barcode.store_upid ) )
    {
        printf ( "UPID belongs to the latest barcode\n " );
        printf ( "\n" );
    }

    if ( upid == -1 )
    {
        return ER_KEY_DOES_NOT_EXITS;
    }
    else
    {
    //db_attr_t data;
    /*strncpy(data.station_no, up_attr->station_no, sizeof(up_attr->station_no) - 1);
    strncpy(data.attr_id, up_attr->attr_id, sizeof(up_attr->attr_id) - 1);*/
        get_category_and_datatype ( up_attr );
        //get_category_and_datatype(&data);

        db_attr_t insert_values;
        char val_double [ 10 ] = { "0" };
        char val_varbinary [ 10 ] = { "0" };
        char val_bigint [ 10 ] = { "0" };
        strncpy ( insert_values.table_no, up_attr->category, sizeof ( up_attr->category ) - 1 );
        if ( atol ( up_attr->datatype ) == 2 )
        {

            strncpy ( insert_values.attr_value_bigint, up_attr->attr_value, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_double, val_double, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_varbinary, val_varbinary, sizeof ( up_attr->attr_value ) - 1 );

        }
        else if ( atol ( up_attr->datatype ) == 3 )
        {
            strncpy ( insert_values.attr_value_double, up_attr->attr_value, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_bigint, val_bigint, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_varbinary, val_varbinary, sizeof ( up_attr->attr_value ) - 1 );

        }
        else
        {
            strncpy ( insert_values.attr_value_varbinary, up_attr->attr_value, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_double, val_double, sizeof ( up_attr->attr_value ) - 1 );
            strncpy ( insert_values.attr_value_bigint, val_bigint, sizeof ( up_attr->attr_value ) - 1 );
        }
        strncpy ( insert_values.station_no, up_attr->station_no, sizeof ( up_attr->station_no ) - 1 );
        strncpy ( insert_values.attr_id, up_attr->attr_id, sizeof ( up_attr->attr_id ) - 1 );
        strncpy ( insert_values.upid, pass_barcode.store_upid, sizeof ( pass_barcode.store_upid ) - 1 );
        strncpy ( insert_values.substation_id, up_attr->substation_id, sizeof ( up_attr->substation_id ) - 1 );

        time_t datetime;
        datetime = time ( NULL );
        sprintf ( insert_values.date_time, "%lld", datetime );
        insert_attr_values ( &insert_values );

        db_attr_t attr_values;
        strncpy ( attr_values.datatype, up_attr->datatype, sizeof ( up_attr->datatype ) - 1 );
        //strncpy(attr_values.station_no, up_attr->station_no, sizeof(up_attr->station_no) - 1);
        strncpy ( attr_values.attr_id, up_attr->attr_id, sizeof ( up_attr->attr_id ) - 1 );
        strncpy ( attr_values.attr_value, up_attr->attr_value, sizeof ( up_attr->attr_value ) - 1 );
        //printf("%s\n", attr_values.attr_value);
        int attr = check_value_in_range ( &attr_values );

        if ( attr == 0 )
        {
            return ER_DB_QUERY_FAILED;
        }
        else
        {
            db_attr_t reduce_cnt;
            strncpy ( reduce_cnt.attr_station_no, up_attr->attr_station_no, sizeof ( up_attr->attr_station_no ) - 1 );
            strncpy ( reduce_cnt.store_upid, pass_barcode.store_upid, sizeof ( pass_barcode.store_upid ) - 1 );
            printf ( "reduce cnt upid %s\n", reduce_cnt.store_upid );
            reduce_mf_attr_cnt ( &reduce_cnt );
            db_attr_t file_data;
            strncpy ( file_data.filename, up_attr->filename, sizeof ( up_attr->filename ) - 1 );
            insert_file_into_database ( &file_data );
            log_message ( EVENTLOG_WARNING_TYPE, "Shutting down." );
            return 0;

        }
    }

}


int db_close ()
{
    mysql_close ( pmySQL );
    return SUCCESS;
}

//int dll_init( void ) {
//    printf("dll_init\n");
//    return 1;
//}

int struct_init ( dll_t* struct_p, size_t size_p )
{
    int retVal_l = -1;
    size_t size_l = sizeof ( dll_t ), count_l = 0;;
    ADDR_t* testPtr_l = ( ADDR_t* ) struct_p;

    //Pointer gültig ?
    if ( struct_p )
    {
//Größenvergleich
        if ( size_l == size_p )
        {

//Funktionspointer in der struct funktion zuweisen (Typ-prüfung !).

//struct_p->pDll_init = dll_init;   
            struct_p->pDll_db_init = db_init;
            struct_p->pDll_br_init = barcode_exists;
            struct_p->pDll_update_attr = update_attribute;
            struct_p->pDll_db_close = db_close;

            retVal_l = 0;

            for ( count_l = 0; count_l < ( size_l / sizeof ( ADDR_t ) ); count_l = count_l++ )
            {
                if ( 0 == testPtr_l [ count_l ] )
                {
                    retVal_l = -1;
                    break;
                }
            }
        }
    }
    return retVal_l;
}
