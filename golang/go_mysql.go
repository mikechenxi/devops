package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "os"
)

const (
    dbIp = "xx.xx.xx.xx"
    dbPort = 3306
    dbNetwork  = "tcp"
    dbUserName = "xxxx"
    dbPassword = "xxxx"
    dbName = "xxxx"
)

var db *sql.DB
var err error

func main(){
    fmt.Println(QueryMysql("select name from tablename where id = ?", 1))
    fmt.Println(ExecMysql("update tablename set name = ? where id = ?", "aaaa", 1))
    fmt.Println(QueryMysql("select name from tablename where id = ?", 1))
}

func InitDb(){
    ds := fmt.Sprintf("%s:%s@%s(%s:%d)/%s", dbUserName, dbPassword, dbNetwork, dbIp, dbPort, dbName)
    db, err = sql.Open("mysql", ds)
    if err := db.Ping(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}

func QueryMysql(sqlStatement string, params ...interface{}) []map[string]string {
    var result []map[string]string
    InitDb()
    defer db.Close()
    rows, err := db.Query(sqlStatement, params...)
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

func ExecMysql(sqlStatement string, params ...interface{}) (int64, error) {
    InitDb()
    defer db.Close()
    result, err := db.Exec(sqlStatement, params...)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    return result.RowsAffected()
}
