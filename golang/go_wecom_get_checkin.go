package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
    "io/ioutil"
    "net/http"
    "sort"
    "time"
)

const (
    TIME_LAYOUT = "2006-01-02 15:04:05"
)

func main(){
    sysTime := time.Now()
    startTime := sysTime.Add(-time.Minute * 60).Format(TIME_LAYOUT)
    endTime := sysTime.Format(TIME_LAYOUT)
    userListMap := getWecomUserList()
    //startTime = "2021-07-26 12:00:00"
    //endTime = "2021-07-26 17:00:00"
    //userListMap = map[string]string{"01": "张三"}
    checkinData := getWecomCheckinData(startTime, endTime, userListMap)
    fmt.Println(checkinData)
}

func getWecomUserList() map[string]string {
    var userListMap = make(map[string]string)
    token := getWecomToken("org")
    url := fmt.Sprintf("https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=%s&department_id=%s&fetch_child=1", token, "1")
    resp, err := http.Get(url)
    if err != nil {
        return userListMap
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var res map[string]interface{}
    _ = json.Unmarshal([]byte(body), &res)
    userList := res["userlist"].([]interface{})
    for _, value := range userList {
        user := value.(map[string]interface{})
        userID := user["userid"].(string)
        if userID[1:2] == "0" || userID[1:2] == "6" || userID[1:2] == "9" {
            userListMap[userID] = user["name"].(string)
        }
    }
    return userListMap
}

func getWecomCheckinData(startTime string, endTime string, userListMap map[string]string) []interface{} {
    var ret []interface{}
    loc, _ := time.LoadLocation("Local")
    startTimeTmp, _ := time.ParseInLocation(TIME_LAYOUT, startTime, loc)
    startTimeUnix := startTimeTmp.Unix()
    endTimeTmp, _ := time.ParseInLocation(TIME_LAYOUT, endTime, loc)
    endTimeUnix := endTimeTmp.Unix()
    token := getWecomToken("checkin")
    url := fmt.Sprintf("https://qyapi.weixin.qq.com/cgi-bin/checkin/getcheckindata?access_token=%s", token)
    var data = map[string]interface{} {
        "opencheckindatatype": "1",
        "starttime": startTimeUnix,
        "endtime": endTimeUnix,
    }
    var userIDList []string
    for key := range userListMap {
        userIDList = append(userIDList, key)
    }
    sort.Strings(userIDList)
    for i := 0; i < len(userIDList) / 100 + 1; i++ {
        if i < len(userIDList) / 100 {
            data["useridlist"] = userIDList[i * 100: (i + 1) * 100]
        } else {
            data["useridlist"] = userIDList[i * 100: ]
        }
        bytesData, _ := json.Marshal(data)
        resp, err := http.Post(url, "application/json", bytes.NewReader(bytesData))
        if err != nil {
            continue
        }
        defer resp.Body.Close()
        body, _ := ioutil.ReadAll(resp.Body)
        var res map[string]interface{}
        _ = json.Unmarshal([]byte(body), &res)
        checkinData := res["checkindata"].([]interface{})
        for i := 0; i < len(checkinData); i++ {
            checkin := checkinData[i].(map[string]interface{})
            checkin["checkin_time"] = time.Unix(int64(checkin["checkin_time"].(float64)), 0).Format(TIME_LAYOUT)
            checkin["name"] = userListMap[checkin["userid"].(string)]
            ret = append(ret, checkin)
        }
    }
    return ret
}


func getWecomToken(source string) string{
    corpID := "xxxx"
    corpSecret := ""
    if source == "checkin" {
        corpSecret = "xxxx"
    } else if source == "org" {
        corpSecret = "xxxx"
    } else {

    }
    url := fmt.Sprintf("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s", corpID, corpSecret)
    resp, err := http.Get(url)
    if err != nil {
        return ""
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    var res map[string]interface{}
    _ = json.Unmarshal([]byte(body), &res)
    token := res["access_token"].(string)
    return token
}
