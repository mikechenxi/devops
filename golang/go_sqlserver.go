package main

import (
    "database/sql"
    "fmt"
    _ "github.com/denisenkom/go-mssqldb"
    "os"
)

const (
    dbIp = "xx.xx.xx.xx"
    dbPort = 1433
    dbUserName = "xxxx"
    dbPassword = "xxxx"
    dbName = "xxxx"
)

var sqlserverDB *sql.DB
var sqlserverErr error

func main(){
    fmt.Println(QuerySqlserver("select name from tablename where id = ?", 1))
    fmt.Println(ExecSqlserver("update tablename set name = ? where id = ?", "aaaa", 1))
    fmt.Println(QuerySqlserver("select name from tablename where id = ?", 1))
}

func initSqlserver() {
    ds := fmt.Sprintf("server=%s;port=%d;user id=%s;password=%s;database=%s;encrypt=disable", dbIp, dbPort, dbUserName, dbPassword, dbName)
    sqlserverDB, sqlserverErr = sql.Open("mssql", ds)
    fmt.Println(sqlserverDB.Ping())
    if sqlserverErr != nil {
        fmt.Println(sqlserverErr)
        os.Exit(1)
    }
}

func querySqlserver(sqlStatement string, params ...interface{}) []map[string]string {
    var result []map[string]string
    initSqlserver()
    defer sqlserverDB.Close()
    rows, err := sqlserverDB.Query(sqlStatement, params...)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    columns, _ := rows.Columns()
    values := make([]sql.RawBytes, len(columns))
    scanArgs := make([]interface{}, len(values))
    for i := range values {
        scanArgs[i] = &values[i]
    }
    for rows.Next() {
        res := make(map[string]string)
        rows.Scan(scanArgs...)
        for i, col := range values {
            res[columns[i]] = string(col)
        }
        result = append(result, res)
    }
    rows.Close()
    return result
}

func execSqlserver(sqlStatement string, params ...interface{}) (int64, error) {
    initSqlserver()
    defer sqlserverDB.Close()
    result, err := sqlserverDB.Exec(sqlStatement, params...)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    return result.RowsAffected()
}
