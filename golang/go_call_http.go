package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "strings"
)

func main(){
    fmt.Println(callHttp("https://www.baidu.com", nil, "GET"))
}

func callHttp(requestUrl string, requestData map[string]interface{}, method string) interface{}{
    method = strings.ToUpper(method)
    var resp *http.Response
    var err error
    if method == "GET" {
        resp, err = http.Get(requestUrl)
    } else if method == "POST" {
        bytesData, _ := json.Marshal(requestData)
        requestBody := strings.NewReader(string(bytesData))
        resp, err = http.Post(requestUrl, "application/json", requestBody)
    } else {
        os.Exit(1)
    }
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var res interface{}
    _ = json.Unmarshal(body, &res)
    return res
}
