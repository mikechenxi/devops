package main

import (
    "encoding/json"
    "fmt"
    "io"
    "io/ioutil"
    "net/http"
    "net/url"
    "os"
    "strings"
)

func CallHttp(requestUrl string, requestData map[string]interface{}, method string, useProxy bool) interface{}{
    var client http.Client
    if useProxy == true {
        proxyUrl := "http://xx.xx.xx.xx:xx"
        urlUrl := url.URL{}
        urlProxy, _ := urlUrl.Parse(proxyUrl)
        client = http.Client{
            Transport: &http.Transport{
                Proxy: http.ProxyURL(urlProxy),
            },
        }
    } else {
        client = http.Client{}
    }
    var requestBody io.Reader
    if requestData != nil {
        bytesData, _ := json.Marshal(requestData)
        requestBody = strings.NewReader(string(bytesData))
    } else {
        requestBody = nil
    }
    method = strings.ToUpper(method)
    request, err := http.NewRequest(method, requestUrl, requestBody)
    if err != nil{
        fmt.Println(err)
        os.Exit(1)
    }
    request.Header.Add("content-type", "application/json")
    resp, err := client.Do(request)
    if err != nil{
        fmt.Println(err)
        os.Exit(1)
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var res interface{}
    _ = json.Unmarshal(body, &res)
    return res
}

func CallHttp2(requestUrl string, requestData map[string]interface{}, method string) interface{}{
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
