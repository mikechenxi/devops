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
    sendEmail([]string{"xx@xx.com", "xx@xx.com"}, "subject", "content", []string{"a.txt", "b.txt"})
}

func sendEmail(receivers []string, subject string, content string, attachments []string) error {
    message := gomail.NewMessage()
    message.SetHeader("From", message.FormatAddress(user, name))
    message.SetHeader("To", receivers...)
    message.SetHeader("Subject", subject)
    message.SetBody("text/html", content)
    if attachments != nil && len(attachments) > 0 {
        for _, attachment := range attachments {
            message.Attach(attachment)
        }
    }
    dialer := gomail.NewDialer(host, port, user, password)
    err := dialer.DialAndSend(message)
    return err
}
