package main

import (
    "fmt"
    "github.com/go-ini/ini"
    "os"
)

const (
    configFILE = "config.ini"
)

func main(){
    fmt.Println(getConfig("A", "a"))
    fmt.Println(setConfig("A", "a", "aaaaa"))
    fmt.Println(getConfig("A", "a"))
}

func getConfig(section string, key string) string {
    cfg, err := ini.Load(configFILE)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    return cfg.Section(section).Key(key).String()
}

func setConfig(section, key, value string) bool {
    cfg, err := ini.Load(configFILE)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    cfg.Section(section).Key(key).SetValue(value)
    err = cfg.SaveTo(configFILE)
    if err != nil {
        fmt.Println(err)
        return false
    }
    return true
}

/*
config.ini
[A]
a=asdf
*/
