package main

import (
    "fmt"
    "net/smtp"
    "strconv"
    "strings"
)

const (
    host = "smtp.exmail.qq.com"
    port = 25
    user = "xxxx@xx.com"
    password = "xxxx"
    name = "XXXX"
)

func main(){
    SendEmail([]string{"aa@xx.com", "bb@xx.com"}, "subject", "content")
}

func SendEmail(receivers []string, subject string, content string) error {
    auth := smtp.PlainAuth("", user, password, host)
    message := []byte("To: " + strings.Join(receivers, ",") + "\r\n" +
        "From: " + name + "<" + user + ">" + "\r\n" +
        "Subject: " + subject + "\r\n" +
        "Content-Type: text/html;charset=UTF-8" + "\r\n\r\n" +
        content)
    err := smtp.SendMail(host + ":" + strconv.Itoa(port), auth, user, receivers, message)
    return err
}
