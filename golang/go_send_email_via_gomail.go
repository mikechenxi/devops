package util

import (
    "gopkg.in/gomail.v2"
)

const (
    host = "smtp.exmail.qq.com"
    port = 25
    user = "xxxx@xx.com"
    password = "xxxx"
    name = "XXXX"
)

func main(){
    SendEmail([]string{"xx@xx.com", "xx@xx.com"}, "subject", "content")
}

func SendEmail(receivers []string, subject string, content string) error {
    message := gomail.NewMessage()
    message.SetHeader("From", message.FormatAddress(user, name))
    message.SetHeader("To", receivers...)
    message.SetHeader("Subject", subject)
    message.SetBody("text/html", content)
    dialer := gomail.NewDialer(host, port, user, password)
    err := dialer.DialAndSend(message)
    return err
}
